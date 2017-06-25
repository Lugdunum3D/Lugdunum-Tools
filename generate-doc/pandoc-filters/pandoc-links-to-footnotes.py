#!/usr/bin/env python

"""
Shift header level
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Note, Link, Para, Str, Space, RawInline
import sys
from utils import stringify

def links_to_footnotes(elem, doc):
    """
    Will shift a header level from the filter-header-shift
    metadata value (which must exist)
    """
    if isinstance(elem, Link):
        if elem.url.startswith('#'):
            return
        if elem.url.startswith('mailto:'):
            return
        return [elem, Note(Para(RawInline(stringify(elem), format='tex'), Str(':'), Space(), Link(Str(elem.url), title=elem.title, url=elem.url)))]

def main(doc=None):
    """
    Run the main fitler
    """
    return run_filter(links_to_footnotes, doc=doc)


if __name__ == "__main__":
    main()
