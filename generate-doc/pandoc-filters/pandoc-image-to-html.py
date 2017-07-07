#!/usr/bin/env python

"""
"""

__author__ = "Antoine Bolvy"

from panflute import run_filter, Image, Str, RawInline
import sys
from utils import stringify
from lxml import etree
from lxml.builder import E

def CLASS(v):
    # helper function, 'class' is a reserved word
    return {'class': v}

def html_img_to_image(elem, doc):
    """
    Apply the translations, see module doc
    """

    # We are only interested in image elements
    if not isinstance(elem, Image):
        return

    if not len(elem.content):
        return RawInline(etree.tostring(E.img(src=elem.url, **elem.attributes), encoding='utf-8', xml_declaration=False, pretty_print=False).decode('utf-8'), format='html')
    html = E("figure",
        E.img(CLASS("figure"), src=elem.url, **elem.attributes),
        E("figcaption", CLASS("caption"), stringify(elem)),
    )
    if hasattr(elem.content[0], 'identifier'):
        html.set('id', elem.content[0].identifier)
    return RawInline(etree.tostring(html, encoding='utf-8', xml_declaration=False, pretty_print=True).decode('utf-8'), format='html')


def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(html_img_to_image, doc=doc)

if __name__ == "__main__":
    main()
