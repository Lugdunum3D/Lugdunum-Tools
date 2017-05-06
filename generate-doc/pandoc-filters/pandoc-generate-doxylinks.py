#!/usr/bin/env python

"""
Pandoc filter to replace namespace in code inlines to short class names with links
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Image, Str, RawInline, CodeBlock, Code, Link
import lxml.html as html
import sys
import re

# inspired from http://stackoverflow.com/a/30490482/2367848
def doxymangle(identifier):
    """
    Converts a string to doxygen url format
    """
    substitutions = {
        '_': "__",
        '-': "-",
        ':': "_1",
        '/': "_2",
        '<': "_3",
        '>': "_4",
        '*': "_5",
        '&': "_6",
        '|': "_7",
        '.': "_8",
        '!': "_9",
        ',': "_00",
        ' ': "_01",
        '{': "_02",
        '}': "_03",
        '?': "_04",
        '^': "_05",
        '%': "_06",
        '(': "_07",
        ')': "_08",
        '+': "_09",
        '=': "_0A",
        '$': "_0B",
        '\\': "_0C",
    }
    out = ''
    for char in identifier:
        if char in substitutions:
            out += substitutions[char]
        else:
            out += char
    return out


def doxylink(elem, _):
    """
    Apply the doxylink
    """
    # We are only interested in "links" elements
    if not isinstance(elem, Link):
        return

    # https://regex101.com/r/ZS5Fu6/1
    res = re.match(r'^\#(lug(?:\:\:[\w]+)+?)(\:\:[\w]+\(\))?$', elem.url)

    if res:
        elem.url = 'https://lugdunum3d.github.io/docs/class' + doxymangle(res.group(1)) + '.html'


def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(doxylink, doc=doc)

if __name__ == "__main__":
    main()
