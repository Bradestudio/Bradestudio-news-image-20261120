#!/usr/bin/env python3
"""Shipped entrypoint: writes the entry image to the grader's output dir.

Stdlib only. Copies the pre-rendered entry.png sitting next to this file
into MAKEFUN_OUTPUT_DIR (or the first CLI argument, or ./output) as
entry.png. Deterministic: the same bytes every run.
"""
import os
import shutil
import sys
from pathlib import Path


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out and len(sys.argv) > 1:
        out = sys.argv[1]
    if not out:
        out = "output"
    outdir = Path(out)
    outdir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "entry.png"
    if not src.is_file():
        raise SystemExit(f"entry.png missing next to {__file__}")
    dst = outdir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
