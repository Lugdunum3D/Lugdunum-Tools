#!/usr/bin/env python

"""
Pandoc filter to fix and normalize images tags with width/height attributes,
as you would do in a Github flavored markdown README file

e.g.

```
<img src="http://design.ubuntu.com/wp-content/uploads/logo-ubuntu_cof-orange-hex.svg" width="16">
```

is converted to a real Image with a width of 16px
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Image, BlockQuote, RawInline, Space, ListContainer
from utils import stringify

import sys

def add_caption(elem, _):
    """
    Convert Header -> LaTeX RawInline
    """
    if not isinstance(elem, Image):
        return
    if not isinstance(elem.parent.next, BlockQuote):
        return
    sys.stderr.flush()
    # print(elem.container.parent.next, file=sys.stderr)
    elem.title = 'fig:'
    info = elem.parent.next.content[0]
    print(elem.parent.next, file=sys.stderr)
    elem.content = info.content
    if hasattr(info.content[0], 'identifier'):
        elem.content.insert(0, RawInline(r'\label{' + info.content[0].identifier + r'}', format='tex'))
    elem.parent.container.remove(elem.parent.next)
    # print(elem.container.parent.next.container, file=sys.stderr)
    # del elem.container.parent.next.parent
    return elem

def main(doc=None):
    """
    Run the main fitler
    """
    return run_filter(add_caption, doc=doc)

if __name__ == "__main__":
    main()
