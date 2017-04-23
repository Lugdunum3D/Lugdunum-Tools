#! /usr/bin/env python
"""
Pandoc filter to download remote files in Images
"""

__author__ = "Antoine Bolvy"

import sys
import os
from urllib.parse import unquote
from urllib.request import urlopen
from urllib.error import HTTPError
import shutil
import logging

from panflute import run_filter, Image
from utils import is_valid_url


IMAGEDIR = 'cache-dl-images'


def download_image(elem, _):
    """
    Download an image from the web
    """
    if not isinstance(elem, Image):
        return

    result = is_valid_url(elem.url)
    if not result: # not a valid url, return
        return

    file_name = unquote(result.path).split('/')[-1]
    full_path = os.path.join(IMAGEDIR, file_name)

    if os.path.isfile(full_path):
        elem.url = full_path
    else:
        try:
            os.mkdir(IMAGEDIR)
            sys.stderr.write('Created directory ' + IMAGEDIR + '\n')
        except OSError:
            pass

        try:
            with urlopen(elem.url) as response, open(full_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                elem.url = full_path
        except HTTPError as err:
            logging.warning('HTTP error %s %d %s', elem.url, err.code, err.reason)

def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(download_image, doc=doc)

if __name__ == "__main__":
    main()
