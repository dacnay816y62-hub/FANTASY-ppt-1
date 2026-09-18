#!/usr/bin/env python3
"""Compatibility CLI for image-only PPTX; text in images is not editable.

Uses the managed JavaScript artifact runtime. For editable decks, author native
text and separate images instead. Default contain keeps full-page copy intact.
"""
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def merge(image_dir: Path, output: Path, fit: str = "contain") -> None:
    node = os.environ.get("CODEX_PRIMARY_RUNTIME_NODE", "")
    modules = os.environ.get("CODEX_PRIMARY_RUNTIME_NODE_MODULES", "")
    if not node or not Path(node).is_absolute() or not Path(node).is_file():
        raise SystemExit("Managed CODEX_PRIMARY_RUNTIME_NODE is unavailable; no alternate runtime will be installed.")
    if not modules or not Path(modules).is_absolute() or not Path(modules).is_dir():
        raise SystemExit("Managed CODEX_PRIMARY_RUNTIME_NODE_MODULES is unavailable.")
    script = Path(__file__).with_suffix(".mjs")
    result = subprocess.run([node, str(script), str(image_dir.resolve()), str(output.resolve()), fit], check=False)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--fit", choices=("contain", "cover"), default="contain", help="contain preserves all content; cover may crop edges")
    args = parser.parse_args()
    merge(args.image_dir, args.output, args.fit)


if __name__ == "__main__":
    main()
