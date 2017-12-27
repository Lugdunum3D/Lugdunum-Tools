#!/usr/bin/env python

"""
TODO
"""

__author__ = "Antoine Bolvy"

import re
from panflute import run_filter, Para, Str, RawInline

def alerts_to_text(elem, _):
    """
    Apply the translations, see module doc
    """
    if not isinstance(elem, Para):
        return

    if not isinstance(elem.content[0], Str):
        return

    if not isinstance(elem.content[-1], Str):
        return

    match1 = re.match(r':::(info|warning|danger|success)', elem.content[0].text)
    match2 = re.match(r':::', elem.content[-1].text)
    if match1 and match2:
        return Para(
            RawInline('\\begin{infobox' + match1.group(1).title() + '}', format='latex'),
            *elem.content[2:-2],
            RawInline('\\end{infobox' + match1.group(1).title() + '}', format='latex')
        )

def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(alerts_to_text, doc=doc)

if __name__ == "__main__":
    main()
