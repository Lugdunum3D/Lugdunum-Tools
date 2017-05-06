#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "graphviz" into
graphviz-generated images.
Needs pygraphviz
"""

import hashlib
import os
import sys
import pygraphviz
from panflute import toJSONFilter, Para, Str, Image, CodeBlock

IMAGE_DIR = "graphviz-images"


def md5(content):
    """
    Returns the md5sum of a string content
    """
    return hashlib.md5(content.encode(sys.getfilesystemencoding())).hexdigest()


def graphviz(elem, doc):
    """
    Generate a graphviz pdf/png from raw code with a graphviz class
    """
    if isinstance(elem, CodeBlock) and 'graphviz' in elem.classes:
        code = elem.text
        graph = pygraphviz.AGraph(string=code)
        title = graph.graph_attr.pop('label', '')
        graph.layout()
        filename = md5(code)
        filetype = {'html': 'png', 'latex': 'pdf'}.get(doc.format, 'png')
        src = IMAGE_DIR + '/' + filename + '.' + filetype
        if not os.path.isfile(src):
            try:
                os.mkdir(IMAGE_DIR)
                sys.stderr.write('Created directory ' + IMAGE_DIR + '\n')
            except OSError:
                pass
            graph.draw(src, prog='dot')
            sys.stderr.write('Created image ' + src + '\n')
        return Para(Image(Str(''), url=src, title=title, attributes={'width': '100%'}))


if __name__ == "__main__":
    toJSONFilter(graphviz)
