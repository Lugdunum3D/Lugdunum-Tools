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

from panflute import run_filter, Image, Str, RawInline
import lxml.html as html
import tinycss

def html_img_to_image(elem, _):
    """
    Apply the translations, see module doc
    """
    # We are only interested in "raw_html" elements
    if not isinstance(elem, RawInline) or elem.format != 'html':
        return
    html_doc = html.fromstring(elem.text)

    # We only want img tags
    if html_doc.tag != 'img':
        return

    attributes = {}

    # Search sizes as xml attributes
    for attribute in ['width', 'height']:
        if attribute in html_doc.attrib:
            attr_value = html_doc.get(attribute)
            if attr_value.isnumeric():
                attr_value += 'px'
            attributes[attribute] = attr_value

    # Search sizes as inline styles
    if 'style' in html_doc.attrib:
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet('.inline {' + html_doc.get('style') + '}')
        for decl in stylesheet.rules[0].declarations:
            if decl.name in ['width', 'height']:
                attr_value = decl.value.as_css()
                if attr_value.startswith('.'):
                    attr_value = '0' + attr_value
                attributes[decl.name] = attr_value

    title = Str(html_doc.get('alt')) if 'alt' in html_doc.attrib else ''
    return Image(attributes=attributes, url=html_doc.get('src'), title=title)


def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(html_img_to_image, doc=doc)

if __name__ == "__main__":
    main()
