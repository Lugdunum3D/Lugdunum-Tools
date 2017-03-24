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

def html_img_to_image(elem, _):
    """
    Apply the translations, see module doc
    """
    # We are only interested in "raw_html" elements
    if not isinstance(elem, Para):
        return

    if not isinstance(elem.content[0], Str):
        return


    match = re.match(r':::(info|warning|danger)', elem.content[0].text)
    if match:
        if match.group(1) == 'info':
            return Para(Strong(Str('Note:')), Space, *elem.content[2:-2])
        if match.group(1) == 'warning':
            return Para(Strong(Str('Warning:')), Space, *elem.content[2:-2])
        if match.group(1) == 'danger':
            return Para(Strong(Str('Caution:')), Space, *elem.content[2:-2])



def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(html_img_to_image, doc=doc)

if __name__ == "__main__":
    main()
