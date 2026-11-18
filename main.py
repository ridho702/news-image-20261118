#!/usr/bin/env python3
"""Entry point for the news-image-20261118 bounty.

The infographic is drawn by generate_entry.py and committed as entry.png.
This program only copies that committed image to the grader's output
directory, so both runs write byte-identical output. Standard library only.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
    sys.exit(0)
