#!/usr/bin/env python3
"""Inspect PPTX slide-local OOXML; render review is still required.

Geometry covers shape/image/table frames including grouped transforms. It does
not measure rendered text, detect text baked into images, or resolve inherited
master/layout content. Large-image flags are review cues, not screenshot proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import posixpath
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
EMU = 914400
IDENTITY = (1, 0, 0, 1, 0, 0)


def multiply(m, n):
    a, b, c, d, e, f = m
    g, h, i, j, k, l = n
    return (a*g+c*h, b*g+d*h, a*i+c*j, b*i+d*j, a*k+c*l+e, b*k+d*l+f)


def transform(m, x, y):
    a, b, c, d, e, f = m
    return a*x+c*y+e, b*x+d*y+f


def values(node, tag, first, second, defaults=(0, 0)):
    item = node.find(tag, NS) if node is not None else None
    return tuple(float(item.get(k, str(v))) for k, v in zip((first, second), defaults)) if item is not None else defaults


def xfrm_for(node):
    for key in ("p:spPr/a:xfrm", "p:xfrm", "p:grpSpPr/a:xfrm"):
        found = node.find(key, NS)
        if found is not None:
            return found
    return None


def own_transform(xfrm):
    x, y = values(xfrm, "a:off", "x", "y")
    w, h = values(xfrm, "a:ext", "cx", "cy")
    angle = math.radians(float(xfrm.get("rot", "0"))/60000)
    fx = -1 if xfrm.get("flipH") in {"1", "true"} else 1
    fy = -1 if xfrm.get("flipV") in {"1", "true"} else 1
    c, s = math.cos(angle), math.sin(angle)
    # Local frame -> rotate/flip around frame centre -> parent coordinates.
    m = multiply((1, 0, 0, 1, x+w/2, y+h/2), (c*fx, s*fx, -s*fy, c*fy, 0, 0))
    return multiply(m, (1, 0, 0, 1, -w/2, -h/2)), w, h


def records(tree, parent=IDENTITY):
    for node in tree:
        tag = node.tag.rsplit("}", 1)[-1]
        if tag not in {"sp", "pic", "graphicFrame", "cxnSp", "grpSp"}:
            continue
        xfrm = xfrm_for(node)
        if tag == "grpSp":
            if xfrm is None:
                yield from records(node, parent)
                continue
            local, w, h = own_transform(xfrm)
            ox, oy = values(xfrm, "a:chOff", "x", "y")
            cw, ch = values(xfrm, "a:chExt", "cx", "cy", (w, h))
            sx, sy = w/cw if cw else 1, h/ch if ch else 1
            yield from records(node, multiply(parent, multiply(local, (sx, 0, 0, sy, -ox*sx, -oy*sy))))
            continue
        props = node.find(".//p:cNvPr", NS)
        label = props.get("name", "") if props is not None else ""
        hidden = props is not None and props.get("hidden") in {"1", "true"}
        rect = None
        if xfrm is not None:
            local, w, h = own_transform(xfrm)
            m = multiply(parent, local)
            corners = [transform(m, x, y) for x, y in ((0, 0), (w, 0), (w, h), (0, h))]
            rect = (min(v[0] for v in corners), min(v[1] for v in corners), max(v[0] for v in corners), max(v[1] for v in corners))
        texts = [t.text or "" for t in node.findall(".//a:t", NS)]
        yield {"node": node, "kind": tag, "name": label, "hidden": hidden, "rect": rect, "texts": texts}


def intersection(rect, width, height):
    l, t, r, b = rect
    return max(0, min(r, width)-max(l, 0))*max(0, min(b, height)-max(t, 0))


def font_inventory():
    try:
        result = subprocess.run(["fc-list", "--format=%{family}\\n"], capture_output=True, text=True, timeout=10, check=True)
    except (OSError, subprocess.SubprocessError):
        return None
    return {name.strip().casefold() for line in result.stdout.splitlines() for name in line.split(",") if name.strip()}


def slide_order(zf, presentation):
    relpath = "ppt/_rels/presentation.xml.rels"
    rels = ET.fromstring(zf.read(relpath))
    targets = {r.get("Id"): posixpath.normpath(posixpath.join("ppt", r.get("Target", ""))).lstrip("/") for r in rels if r.get("TargetMode") != "External"}
    return [targets[n.get(f"{{{NS['r']}}}id")] for n in presentation.findall("p:sldIdLst/p:sldId", NS)]


def inspect(path: Path, require_editable: bool = False, check_fonts: bool = False) -> dict[str, object]:
    errors, warnings, pages, all_texts = [], [], [], []
    hashes = Counter()
    declared_fonts, theme_fonts = set(), set()
    try:
        with zipfile.ZipFile(path) as zf:
            presentation = ET.fromstring(zf.read("ppt/presentation.xml"))
            size = presentation.find("p:sldSz", NS)
            if size is None:
                raise ValueError("Missing presentation slide size")
            width, height = int(size.get("cx", "0")), int(size.get("cy", "0"))
            if width <= 0 or height <= 0:
                raise ValueError("Invalid presentation slide size")
            slide_names = slide_order(zf, presentation)
            media_names = [n for n in zf.namelist() if n.startswith("ppt/media/") and not n.endswith("/")]
            empty_media = []
            for name in media_names:
                data = zf.read(name)
                hashes[hashlib.sha256(data).hexdigest()] += 1
                if not data:
                    empty_media.append(name)
            if empty_media:
                errors.append("Empty embedded media files: " + ", ".join(empty_media))
            # Declared families are reported separately from theme references.
            for name in zf.namelist():
                if name.startswith("ppt/theme/") and name.endswith(".xml"):
                    theme = ET.fromstring(zf.read(name))
                    for node in theme.findall(".//a:fontScheme//*[@typeface]", NS):
                        if node.get("typeface"):
                            theme_fonts.add(node.get("typeface"))
            for index, name in enumerate(slide_names, 1):
                root = ET.fromstring(zf.read(name))
                tree = root.find("p:cSld/p:spTree", NS)
                if tree is None:
                    raise ValueError(f"Slide {index} missing shape tree")
                objects = list(records(tree))
                text_shapes, text_chars, image_frames = 0, 0, []
                on_canvas_texts = []
                out_of_bounds, unresolved = [], []
                page_fonts, font_sizes = set(), []
                for rec in objects:
                    node, rect = rec["node"], rec["rect"]
                    all_texts.extend(rec["texts"])
                    if rec["hidden"]:
                        continue
                    joined = "".join(rec["texts"]).strip()
                    if joined:
                        text_shapes += 1
                        # Off-canvas text does not establish editable slide copy.
                        if rect is not None and intersection(rect, width, height) > 0:
                            text_chars += len(re.sub(r"\s", "", joined))
                            on_canvas_texts.append(joined)
                        for font in node.findall(".//*[@typeface]"):
                            family = font.get("typeface")
                            if family:
                                page_fonts.add(family)
                        font_sizes.extend(float(n.get("sz"))/100 for n in node.findall(".//*[@sz]"))
                    if rect is None:
                        unresolved.append(rec["name"] or rec["kind"])
                        continue
                    l, t, r, b = rect
                    if min(l, t) < -12700 or r > width+12700 or b > height+12700:
                        out_of_bounds.append({"name": rec["name"], "kind": rec["kind"], "bounds_inches": [round(n/EMU, 3) for n in rect]})
                    if node.find(".//a:blip", NS) is not None:
                        image_frames.append({"name": rec["name"], "coverage": round(intersection(rect, width, height)/(width*height), 4)})
                # A raster background is also a flattened-image candidate.
                if root.find("p:cSld/p:bg//a:blip", NS) is not None:
                    image_frames.append({"name": "slide background", "coverage": 1.0})
                declared_fonts.update(page_fonts)
                if text_shapes and not page_fonts:
                    warnings.append(f"Slide {index}: no explicit font family on native text; inspect inherited theme/layout fonts and rendered glyphs")
                max_coverage = max((p["coverage"] for p in image_frames), default=0)
                if max_coverage >= .9:
                    warnings.append(f"Slide {index}: an image frame covers >=90% of the canvas; visually verify that required text is native (a photo background can be valid)")
                if require_editable and text_chars == 0:
                    errors.append(f"Slide {index}: no on-canvas editable text found")
                elif require_editable and max_coverage >= .9 and text_chars <= 3 and re.fullmatch(r"[0-9\s./·-]+", "".join(on_canvas_texts)):
                    errors.append(f"Slide {index}: full-slide image with only {text_chars} editable characters resembling a page number; verify required copy is native")
                if out_of_bounds:
                    errors.append(f"Slide {index}: {len(out_of_bounds)} object frame(s) extend beyond the canvas; inspect intentional bleed separately")
                if unresolved:
                    warnings.append(f"Slide {index}: {len(unresolved)} frame(s) lack local geometry; inspect inherited layout positions")
                pages.append({"slide": index, "part": name, "native_text_shapes": text_shapes, "on_canvas_editable_characters": text_chars, "image_frames": image_frames, "fonts_declared": sorted(page_fonts), "explicit_font_size_pt_range": [min(font_sizes), max(font_sizes)] if font_sizes else None, "out_of_bounds": out_of_bounds, "unresolved_frames": unresolved})
    except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError, ValueError) as exc:
        return {"path": str(path), "ok": False, "errors": [str(exc)], "warnings": warnings}

    suspicious = [t for t in all_texts if "\ufffd" in t]
    if suspicious:
        errors.append(f"Unicode replacement characters found: {suspicious[:8]}")
    if not slide_names:
        errors.append("No slide XML files referenced by presentation")
    if not all_texts:
        warnings.append("No slide-local editable text found; deck may be image-only")
    duplicate_files = sum(c-1 for c in hashes.values() if c > 1)
    if duplicate_files:
        warnings.append(f"PPTX contains {duplicate_files} duplicate media files")
    placeholders = sorted(f for f in declared_fonts if f.startswith("+"))
    missing_fonts = []
    installed = font_inventory() if check_fonts else None
    if check_fonts and installed is None:
        warnings.append("Font availability not checked: fc-list unavailable")
    if installed is not None:
        missing_fonts = sorted(f for f in declared_fonts if not f.startswith("+") and f.casefold() not in installed)
        if missing_fonts:
            warnings.append(f"Declared font families unavailable locally: {', '.join(missing_fonts)}")
    if placeholders:
        warnings.append("Theme font references require render verification: " + ", ".join(placeholders))
    return {
        "path": str(path.resolve()), "file_size_mb": round(path.stat().st_size/1024/1024, 2),
        "slides": len(slide_names), "slide_size_inches": [round(width/EMU, 3), round(height/EMU, 3)],
        "media_files": len(media_names), "empty_media_files": empty_media, "editable_text_fragments": len(all_texts),
        "duplicate_media_files": duplicate_files, "fonts_declared": sorted(declared_fonts),
        "theme_fonts_declared": sorted(theme_fonts), "fonts_missing_locally": missing_fonts,
        "per_slide": pages, "errors": errors, "warnings": warnings,
        "scope": "Slide-local frames/text; font availability is local only. Render every slide to check actual wrapping, glyph fallback, overlap, image text, and inherited master/layout content.",
        "ok": not errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--mode", choices=("editable", "image-only"), default="image-only", help="Use editable to require native copy on each slide; image-only checks structure without this requirement (legacy default).")
    parser.add_argument("--require-editable", action="store_true", help="Compatibility alias for --mode editable.")
    parser.add_argument("--check-fonts", action="store_true", help="Compare explicitly declared slide fonts to local fontconfig inventory.")
    args = parser.parse_args()
    mode = "editable" if args.require_editable else args.mode
    result = inspect(args.pptx, mode == "editable", args.check_fonts)
    result["mode"] = mode
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
