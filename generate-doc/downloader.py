#!/usr/bin/env python
"""
Python script to download remote documentation files, from
from a configuration YAML file
"""

__author__ = "Antoine Bolvy"

import sys
import os
import re
import logging
import argparse
import requests
import shutil
import yaml

from collections import OrderedDict

# from http://stackoverflow.com/a/21912744/2367848
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

class Downloader(object):
    """
    Main class for building the documentation,
    to compile a documentation PDF from a YAML config
    """

    def __init__(self):
        super().__init__()

        self.args = None
        self.parse_args()

        levels = [logging.WARNING, logging.INFO, logging.DEBUG]
        level = levels[min(len(levels) - 1, self.args.verbose)]  # capped to number of levels

        logger = logging.getLogger()

        log_handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)8s] %(message)s')
        log_handler.setFormatter(formatter)
        logger.setLevel(level=level)

        with open(self.args.config) as config_file:
            self.config = ordered_load(config_file)

        self.session = requests.Session()

    def parse_args(self):
        """
        Parse the commandline arguments
        """
        parser = argparse.ArgumentParser(description='Download md documentation')
        parser.add_argument('config', help='YAML config file')
        parser.add_argument('-f', '--fast', help='Do not update toc',
                            action='store_true', default=False)
        parser.add_argument('-v', '--verbose', help='Enables verbose output; '
                            'repeat up to three time for more verbose output',
                            action='count', default=0)

        self.args = parser.parse_args()

    def download_file(self, file_config):
        if 'url' in file_config:
            # Download the file from `url` and save it locally under `file_name`:
            logging.info('Downloading %s', file_config['source'])
            # urllib.request.urlretrieve(file_config['url'], file_config['source'])
            headers = {}
            if 'etag' in file_config:
                headers['If-None-Match'] = file_config['etag']
            r = self.session.get(file_config['url'], headers=headers, stream=True)
            logging.info('Status code %d', r.status_code)
            if r.status_code == 200:
                with open(file_config['source'], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                file_config['etag'] = r.headers['ETag']
            logging.info('Done %s', file_config['source'])

    def run(self):
        """
        """

        for file in self.config['bodies']:
            self.download_file(file)
        for file in self.config['abstract']:
            self.download_file(file)
        for file in self.config['summary']:
            self.download_file(file)

        with open(self.args.config, 'w') as yaml_file:
            ordered_dump(self.config, yaml_file, default_flow_style=False)

        logging.info('Done!')

def main():
    """
    Run the main
    """
    Downloader().run()

if __name__ == '__main__':
    main()
