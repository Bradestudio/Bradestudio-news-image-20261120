"""Entrypoint for the news-image-20261120 front page.

The picture itself is drawn at build time by gen_image.py and shipped as
entry.png beside this file. This program only carries that one file into
the output directory the grader provides, so it runs with the standard
library alone, needs no network, and writes the same bytes every time.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path


def here():
    return Path(__file__).resolve().parent


def output_dir():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    target = output_dir()
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(here() / "entry.png", target / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
