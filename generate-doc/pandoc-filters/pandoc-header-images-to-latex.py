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

from panflute import run_filter, Header, Image, RawInline, RawBlock

from utils import tex_escape, stringify

def convert_px_to_in(dpi, elem):
    """
    Self descriptive
    """
    for attr_name in ['width', 'height']:
        if attr_name in elem.attributes and elem.attributes[attr_name].endswith('px'):
            elem.attributes[attr_name] = str(int(elem.attributes[attr_name][:-2]) / dpi) + 'in'

def generate_includegraphics(elem):
    """
    Generate a LaTeX includegraphics directive
    """
    out = '\\protect\\includegraphics'

    config = []
    for attr_name in ['width', 'height']:
        if attr_name in elem.attributes:
            config.append([attr_name, elem.attributes[attr_name]])

    config = ', '.join([item[0] + '=' + item[1] for item in config])

    if config:
        out += '[' + config + ']'
    out += '{%s}' % elem.url
    return out

def generate_latex_header(elem, stringified):
    """
    Generate a LaTeX header
    """

    levels = [
        'section',
        'subsection',
        'subsubsection',
        'paragraph'
    ]

    return RawBlock('\\%s[%s]{%s}\n' % (
        levels[elem.level - 1],
        stringified,
        stringify(elem)
    ), format='tex')

def header_img_to_latex(elem, doc):
    """
    Convert Header -> LaTeX RawInline
    """

    if isinstance(elem, Header):
        modified = False
        # Will contain the elements without the Images, replaced by LaTeX RawInlines
        new_content = []

        stringified = stringify(elem).strip()  # before we include the latex includegraphics

        for item in elem.content:
            if isinstance(item, Image):
                modified = True
                convert_px_to_in(96, item)
                new_content.append(RawInline(
                    '\\raisebox{-0.2\\height}{' + generate_includegraphics(item) + '}\\enspace',
                    format='tex'))
            else:
                new_content.append(item)

        if modified:
            elem.content = new_content
            return generate_latex_header(elem, stringified)

def main(doc=None):
    """
    Run the main fitler
    """
    return run_filter(header_img_to_latex, doc=doc)

if __name__ == "__main__":
    main()
