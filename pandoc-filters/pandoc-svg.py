#! /usr/bin/env python
"""
Pandoc filter to convert svg files to pdf as suggested at:
https://github.com/jgm/pandoc/issues/265#issuecomment-27317316

Adapted to panflute by Antoine Bolvy
"""

__author__ = "Jerome Robert, Antoine Bolvy"

import mimetypes
import subprocess
import os
import sys
from panflute import run_filter, Image
from utils import is_valid_url

FMT_OPTIONS = {
    "latex": ("--export-pdf", "pdf"),
    "beamer": ("--export-pdf", "pdf"),
    # Use PNG because EMF and WMF break transparency
    "docx": ("--export-png", "png"),
    # Because of IE
    "html": ("--export-png", "png")
}

def svg_to_any(elem, doc):
    """
    Convert a svg to supported formats
    """
    if not isinstance(elem, Image):
        return

    # We don't want urls, you have to download them first
    if is_valid_url(elem.url):
        return

    mimet, _ = mimetypes.guess_type(elem.url)
    flag, file_ext = FMT_OPTIONS.get(doc.format)
    if mimet == 'image/svg+xml' and flag:
        base_name, _ = os.path.splitext(elem.url)
        target_name = base_name + "." + file_ext
        try:
            mtime = os.path.getmtime(target_name)
        except OSError:
            mtime = -1
        if mtime < os.path.getmtime(elem.url):
            cmd_line = ['inkscape', flag, target_name, elem.url]
            sys.stderr.write("Running %s\n" % " ".join(cmd_line))
            subprocess.call(cmd_line, stdout=sys.stderr.fileno())
        elem.url = target_name

def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(svg_to_any, doc=doc)

if __name__ == "__main__":
    main()
