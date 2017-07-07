#!/usr/bin/env python

"""
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Image, Str, RawInline, Link
import sys
import re

def latex_to_md(elem, doc):
    """
    Apply the translations, see module doc
    """

    # We are only interested in RawInline elements
    if not isinstance(elem, RawInline):
        return

    if not elem.format == 'tex':
        return

    print(elem.text, file=sys.stderr)

    res = re.search(r'\\autoref\{(.+)\}', elem.text)

    print(res, file=sys.stderr)
    if res:
        return Link(Str('here'), url='#' + res.group(1))
    return []


def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(latex_to_md, doc=doc)

if __name__ == "__main__":
    main()
