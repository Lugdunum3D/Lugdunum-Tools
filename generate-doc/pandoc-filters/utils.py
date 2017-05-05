#! /usr/bin/env python
"""
Collection of utility functions
"""

import re
from urllib.parse import urlparse
from functools import partial
from panflute import run_filter, Header, Image, RawInline, RawBlock, Citation
from panflute.tools import HorizontalSpaces, VerticalSpaces

# Inspired from django's url validation regex
def is_valid_url(string):
    """
    Check if an URL is valid
    """
    try:
        result = urlparse(string)
        if result.scheme not in ('http', 'https'):
            return None
        if not result.netloc and not result.path:
            return None
        return result
    except ValueError:
        return None

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    regex = re.compile(r'|'.join(
        re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))
    ))
    return regex.sub(lambda match: conv[match.group()], str(text))

def stringify(element):
    """
    Return the raw text version of an elements (and its children element).
    """

    def attach_str(elem, _, answer):
        """
        A
        """
        if isinstance(elem, (RawInline, RawBlock)) and elem.format == 'tex':
            ans = elem.text
        elif hasattr(elem, 'text'):
            ans = tex_escape(elem.text)
        elif isinstance(elem, HorizontalSpaces):
            ans = ' '
        elif isinstance(elem, VerticalSpaces):
            ans = '\n\n'
        elif isinstance(elem, Citation):
            ans = ''
        else:
            ans = ''
        answer.append(ans)

    answer = []
    element.walk(partial(attach_str, answer=answer))
    return ''.join(answer)
