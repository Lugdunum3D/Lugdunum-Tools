#!/usr/bin/env python

"""
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Image, BlockQuote, RawInline, Space, ListContainer
from utils import stringify

import sys

def add_caption(elem, doc):
    """
    """
    if not isinstance(elem, Image):
        return
    if not isinstance(elem.parent.next, BlockQuote):
        return
    elem.title = 'fig:'
    info = elem.parent.next.content[0]
    elem.content = info.content
    if doc.format == 'latex' and hasattr(info.content[0], 'identifier'):
        elem.content.insert(0, RawInline(r'\label{' + info.content[0].identifier + r'}', format='tex'))
    elem.parent.container.remove(elem.parent.next)
    return elem

def main(doc=None):
    """
    Run the main fitler
    """
    return run_filter(add_caption, doc=doc)

if __name__ == "__main__":
    main()
