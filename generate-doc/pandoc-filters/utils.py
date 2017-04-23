#! /usr/bin/env python
"""
Collection of utility functions
"""

import re
from urllib.parse import urlparse

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
