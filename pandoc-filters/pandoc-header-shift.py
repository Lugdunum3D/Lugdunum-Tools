#!/usr/bin/env python

"""
Shift header level
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Header

def shift_header_level(elem, doc):
    """
    Will shift a header level from the filter-header-shift
    metadata value (which must exist)
    """
    if isinstance(elem, Header):
        shift = int(doc.get_metadata('filter-header-shift'))
        if shift > 0 and elem.level + shift <= 6:
            elem.level += shift
        elif shift < 0 and elem.level - shift >= 1:
            elem.level -= shift
        else:
            return []


def main(doc=None):
    """
    Run the main fitler
    """
    return run_filter(shift_header_level, doc=doc)


if __name__ == "__main__":
    main()
