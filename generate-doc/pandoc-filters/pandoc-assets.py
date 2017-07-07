#!/usr/bin/env python

"""
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Image
import os
import shutil
import sys

ASSETS = 'assets/'

def links_to_footnotes(elem, doc):
    """
    Moves image to an ASSETS folder
    """
    if not isinstance(elem, Image):
        return

    try:
        os.mkdir(ASSETS)
        sys.stderr.write('Created directory ' + ASSETS + '\n')
    except OSError:
        pass

    target = os.path.join(ASSETS, os.path.basename(elem.url))

    shutil.copyfile(elem.url, target)

    elem.url = target

    return



def main(doc=None):
    """
    Run the main fitler
    """
    return run_filter(links_to_footnotes, doc=doc)


if __name__ == "__main__":
    main()
