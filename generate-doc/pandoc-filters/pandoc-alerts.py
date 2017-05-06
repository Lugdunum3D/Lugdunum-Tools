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

import re
from panflute import run_filter, Para, Str, Space, Strong

def alerts_to_text(elem, _):
    """
    Apply the translations, see module doc
    """
    if not isinstance(elem, Para):
        return

    if not isinstance(elem.content[0], Str):
        return

    match1 = re.match(r':::(info|warning|danger)', elem.content[0].text)
    match2 = re.match(r':::', elem.content[-1].text)
    if match1 and match2:
        if match1.group(1) == 'info':
            return Para(Strong(Str('Note:')), Space, *elem.content[2:-2])
        if match1.group(1) == 'warning':
            return Para(Strong(Str('Warning:')), Space, *elem.content[2:-2])
        if match1.group(1) == 'danger':
            return Para(Strong(Str('Caution:')), Space, *elem.content[2:-2])



def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(alerts_to_text, doc=doc)

if __name__ == "__main__":
    main()
