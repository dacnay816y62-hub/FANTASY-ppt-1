#!/usr/bin/env python3
"""Validate project files and exported PPTX structure; do not grade design by keywords."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from inspect_pptx import inspect

REQUIRED = ("project-truth", "analysis", "visual-dna", "outline")


def prose_file(project: Path, stem: str) -> Path | None:
    for suffix in (".txt", ".md"):  # Old project packages remain readable.
        candidate = project / (stem+suffix)
        if candidate.is_file():
            return candidate
    return None


def files_with_suffix(directory: Path, suffixes: set[str]) -> list[Path]:
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in suffixes) if directory.is_dir() else []


def validate(project: Path, stage: str, mode: str = "editable", pilot_count: int | None = None) -> dict[str, object]:
    errors, warnings, documents = [], [], {}
    for stem in REQUIRED + (("qa",) if stage == "final" else ()):
        found = prose_file(project, stem)
        if found is None:
            errors.append(f"Missing required file: {stem}.txt (legacy .md also accepted)")
            continue
        documents[stem] = found.read_text("utf-8").strip()
        if not documents[stem]:
            errors.append(f"Empty required file: {found.name}")
        if found.suffix == ".md":
            warnings.append(f"Legacy {found.name} accepted; use .txt for new project prose")
    # Both plain-text and old Markdown heading styles are accepted.
    slide_numbers = [int(n) for n in re.findall(r"^\s*(?:#{1,6}\s*)?(?:Slide\s+|第\s*)(\d+)(?:\s*页)?(?=\s|[｜|:：.—-]|$)", documents.get("outline", ""), re.M | re.I)]
    slide_count = len(slide_numbers)
    if not slide_numbers:
        errors.append("Outline has no 'Slide NN' or '第 N 页' entries")
    elif slide_numbers != list(range(1, slide_count+1)):
        errors.append(f"Outline slide numbers must appear once, in sequence from 1: {slide_numbers}")
    pilot_images = files_with_suffix(project/"pilot-preview", {".png", ".jpg", ".jpeg", ".webp"})
    slide_images = files_with_suffix(project/"slides-preview", {".png", ".jpg", ".jpeg", ".webp"})
    pptx_files = files_with_suffix(project/"exports", {".pptx"})
    pptx_reports = []
    if pilot_count is not None and (pilot_count < 1 or (slide_count and pilot_count > slide_count)):
        errors.append("pilot-count must be at least 1 and cannot exceed the outline slide count")
    required_pilots = pilot_count if pilot_count is not None else 1
    if stage in {"pilot", "final"} and len(pilot_images) < required_pilots:
        errors.append(f"pilot-preview has {len(pilot_images)} images; requires {required_pilots}")
    if stage == "final":
        if not pptx_files:
            errors.append("exports contains no PPTX")
        if slide_count and len(slide_images) < slide_count:
            errors.append(f"slides-preview has {len(slide_images)} images but outline has {slide_count} slides")
        for pptx in pptx_files:
            report = inspect(pptx, require_editable=(mode == "editable"), check_fonts=True)
            pptx_reports.append(report)
            errors.extend(f"{pptx.name}: {e}" for e in report.get("errors", []))
            warnings.extend(f"{pptx.name}: {w}" for w in report.get("warnings", []))
            if report.get("slides") is not None and report["slides"] != slide_count:
                errors.append(f"{pptx.name}: {report['slides']} slides but outline has {slide_count}")
    if (project/"elements-transparent").exists():
        warnings.append("Legacy elements-transparent directory found; use assets-generated and native PPT objects for editable decks")
    return {
        "project": str(project.resolve()), "stage": stage, "mode": mode,
        "slide_count": slide_count, "pilot_images": len(pilot_images), "required_pilots": required_pilots,
        "slide_previews": len(slide_images), "pptx_files": len(pptx_files),
        "pptx_reports": pptx_reports, "errors": errors, "warnings": warnings,
        "scope": "Checks file presence, slide sequence/count and PPTX structure. Truth classification, design logic, preview correspondence and visual quality require content/render review.",
        "ok": not errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--stage", choices=("structure", "pilot", "final"), default="structure")
    parser.add_argument("--mode", choices=("editable", "image-only"), default="editable")
    parser.add_argument("--pilot-count", type=int, help="Number of representative pages selected for this task; defaults to checking that at least one preview exists")
    args = parser.parse_args()
    try:
        result = validate(args.project_dir, args.stage, args.mode, args.pilot_count)
    except (OSError, UnicodeError) as exc:
        result = {"project": str(args.project_dir), "ok": False, "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
