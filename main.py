#!/usr/bin/env python3
"""Entry program: copy the pre-drawn front-page image to the output directory.

Standard library only. The image (entry.png) is drawn by draw.py at build
time; this program just places it where the grader reads it.
"""
import os
import shutil


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()
