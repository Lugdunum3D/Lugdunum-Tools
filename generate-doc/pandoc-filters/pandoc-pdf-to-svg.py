#! /usr/bin/env python
"""
Pandoc filter to convert pdf files to svg
"""

__author__ = "Antoine Bolvy"

import mimetypes
import subprocess
import os
import sys
from panflute import run_filter, Image
from utils import is_valid_url


def pdf_to_svg(elem, doc):
    """
    Convert a pdf to svg
    """
    if not isinstance(elem, Image):
        return

    # We don't want urls, you have to download them first
    if is_valid_url(elem.url):
        return

    mimet, _ = mimetypes.guess_type(elem.url)
    flag, file_ext = ('--export-plain-svg', 'svg')
    if mimet == 'application/pdf' and flag:
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
    return run_filter(pdf_to_svg, doc=doc)

if __name__ == "__main__":
    main()
