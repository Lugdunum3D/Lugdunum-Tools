#! /usr/bin/env python
"""
Pandoc filter to convert mermaid snippets to svg
"""

__author__ = "Antoine Bolvy"

import hashlib
import subprocess
import os
import sys
from panflute import run_filter, Image, CodeBlock, Str, Para

IMAGE_DIR = "mermaid-images"

def md5(content):
    """
    Returns the md5sum of a string content
    """
    return hashlib.md5(content.encode(sys.getfilesystemencoding())).hexdigest()

def mermaid_to_svg(elem, doc):
    """
    Convert a mermaid snippet to svg
    """
    if isinstance(elem, CodeBlock) and 'mermaid' in elem.classes:
        code = elem.text
        filename = md5(code)
        target = IMAGE_DIR + '/' + filename + '.svg'
        tmpfn = IMAGE_DIR + '/' + filename
        if os.path.isfile(target):
            return Para(Image(Str(''), url=target, title='', attributes={'width': '100%'}))
        try:
            os.mkdir(IMAGE_DIR)
            sys.stderr.write('Created directory ' + IMAGE_DIR + '\n')
        except OSError:
            pass

        with open(tmpfn, 'wb') as tmpfn_f:
            tmpfn_f.write(code.encode('utf-8'))

        cmd_line = ['mermaid', '-s', tmpfn, '--phantomPath=/usr/bin/phantomjs', '-o', IMAGE_DIR]
        sys.stderr.write("Running %s\n" % " ".join(cmd_line))

        try:
            p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            raise RuntimeError('command %r cannot be run (needed for mermaid '
                               'output), check the cmd_line setting' % cmd_line)

        stdout, stderr = p.communicate()

        if p.returncode != 0:
            raise RuntimeError('Mermaid exited with error:\n[stderr]\n%s\n'
                               '[stdout]\n%s' % (stderr, stdout))

        if not os.path.isfile(target):
            raise RuntimeError('Mermaid did not produce an output file:\n[stderr]\n%s\n'
                               '[stdout]\n%s' % (stderr, stdout))
        sys.stderr.write('Created image ' + target + '\n')
        return Para(Image(Str(''), url=target, title='', attributes={'width': '100%'}))

def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(mermaid_to_svg, doc=doc)

if __name__ == "__main__":
    main()
