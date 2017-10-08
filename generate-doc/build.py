#!/usr/bin/env python
"""
Python build script to build the documentation, from
from a configuration YAML file
"""

__author__ = "Antoine Bolvy"

import sys
import os
import re
import logging
import subprocess
import hashlib
import shutil
import errno
import argparse

import yaml
import jinja2

OUT_FOLDER = 'build-tmp'

def make_sure_path_exists(path):
    """
        :param path: path to create
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

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

def install_jinja_logger():
    """
    Inits a logger to log undefined values in jinja template expansions
    """
    logger = logging.getLogger(__name__)
    return jinja2.make_logging_undefined(
        logger=logger,
        base=jinja2.Undefined
    )

LATEX_JINJA_ENV = jinja2.Environment(
    block_start_string='\\b{',
    block_end_string='}',
    variable_start_string='\\v{',
    variable_end_string='}',
    comment_start_string='\\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    lstrip_blocks=False,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.realpath(__file__))),
    undefined=install_jinja_logger()
)

LATEX_JINJA_ENV.filters['texesc'] = tex_escape


class Build(object):
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
            self.config = yaml.load(config_file)

    def parse_args(self):
        """
        Parse the commandline arguments
        """
        parser = argparse.ArgumentParser(description='Build PDF documentation')
        parser.add_argument('config', help='YAML config file')
        parser.add_argument('-f', '--fast', help='Do not update toc',
                            action='store_true', default=False)
        parser.add_argument('-p', '--pandoc', help='Only pandoc, no latex',
                            action='store_true', default=False)
        parser.add_argument('-n', '--nocache', help='Disable cache',
                            action='store_true', default=False)
        parser.add_argument('-v', '--verbose', help='Enables verbose output; '
                            'repeat up to three time for more verbose output',
                            action='count', default=0)

        self.args = parser.parse_args()

    def write(self):
        """
        Compile the latex document from the job self.config['name']
        """

        cmnd = ['lualatex', '--interaction=nonstopmode', self.config['name']]

        pipes = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out, std_err = pipes.communicate()

        if pipes.returncode != 0:
            # An error happened!
            sys.stdout.buffer.write(std_out)
            sys.stdout.buffer.write(std_err)
            err_msg = "Code: %s" % pipes.returncode
            print(err_msg, file=sys.stderr)
            raise Exception('Error')

    def get_file_extension(self):
        if self.config['type'] == 'website':
            return '.md'
        return '.tex'

    def generate_file_name(self, source_file):
        source_hash = hashlib.md5(open(source_file, 'rb').read()).hexdigest()
        hash_prefix = source_hash[:8] + '_'
        job_name = os.path.splitext(os.path.basename(source_file))[0]
        target_file_name = os.path.join(OUT_FOLDER, hash_prefix + job_name) + self.get_file_extension()
        return job_name, hash_prefix, target_file_name

    def get_type(self):
        if self.config['type'] == 'website':
            return 'markdown' + \
                '-simple_tables' + \
                '-grid_tables' + \
                '-multiline_tables' + \
                '-inline_code_attributes' + \
                '-fenced_code_attributes' + \
                '+pipe_tables' + \
                '+raw_html' + \
                '+yaml_metadata_block' + \
                '+fenced_code_blocks' + \
                '+auto_identifiers' + \
                '+ascii_identifiers' + \
                '+backtick_code_blocks' + \
                '+autolink_bare_uris' + \
                '+intraword_underscores' + \
                '+strikeout' + \
                '+hard_line_breaks' + \
                '+emoji' + \
                '+shortcut_reference_links' + \
                '+angle_brackets_escapable'
        return 'latex'

    def pandoc_file(self, file_config):
        """
        Run pandoc with our filters on a part of a file, store the tex output in a temp dir
        """
        file_config['job_name'], hash_prefix, target_file_name = self.generate_file_name(file_config['source'])
        file_config['generated'] = target_file_name

        if os.path.isfile(target_file_name) and not self.args.nocache:
            logging.info('Cache exists for %s', file_config['source'])
            return

        logging.info('Running pandoc for %s', file_config['source'])

        cmd = [
            'pandoc',
            '--from=markdown_github+yaml_metadata_block+raw_tex+inline_code_attributes+implicit_figures+link_attributes+bracketed_spans+footnotes+inline_notes',
            '--metadata=hash-prefix:' + hash_prefix,
            '--filter=./pandoc-filters/pandoc-links-to-footnotes.py',
            '--filter=./pandoc-filters/pandoc-github-img.py',
            '--filter=./pandoc-filters/pandoc-dl-images.py',
            '--filter=./pandoc-filters/pandoc-mermaid.py',
            '--filter=./pandoc-filters/pandoc-graphviz.py',
            '--filter=./pandoc-filters/pandoc-generate-doxylinks.py',
            '--filter=./pandoc-filters/pandoc-alerts.py',
            '--filter=./pandoc-filters/pandoc-add-captions.py',
            '--filter=./pandoc-filters/pandoc-google-drive.py'
        ]

        if self.config['type'] != 'website':
            cmd += [
                '--filter=./pandoc-filters/pandoc-svg-to-any.py',
                '--filter=./pandoc-filters/pandoc-header-images-to-latex.py',
            ]

        if 'header_shift' in file_config and file_config['header_shift']: # also check if not 0
            logging.info('Header shift %s', file_config['header_shift'])
            cmd += [
                '--metadata=filter-header-shift:' + str(file_config['header_shift']),
                '--filter=./pandoc-filters/pandoc-header-shift.py',
            ]

        if 'wbs' in file_config and file_config['wbs']:
            logging.info('Enabling wbs')
            cmd += [
                '--filter=./wbs/pandoc-filters/wbs.py'
            ]


        if self.config['type'] == 'website':
            cmd += [
                '--filter=./pandoc-filters/pandoc-pdf-to-svg.py',
                '--filter=./pandoc-filters/pandoc-assets.py',
                '--filter=./pandoc-filters/pandoc-image-to-html.py',
                '--filter=./pandoc-filters/pandoc-latex-to-md.py',
                '--no-highlight',
                '--toc',
                '--template=template.md',
                '--standalone',
            ]

        cmd += [
            '--listings',
            '--atx-headers',
            '--to=' + self.get_type(),
            '--output=' + target_file_name,
            file_config['source'],
        ]

        # print(' '.join(cmd))

        logging.debug(' '.join(cmd))
        pipes = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std_out, std_err = pipes.communicate()

        sys.stdout.buffer.write(std_out)
        sys.stdout.buffer.write(std_err)
        if pipes.returncode != 0:
            # An error happened!
            err_msg = "Code: %s" % pipes.returncode
            print(err_msg, file=sys.stderr)
            raise Exception('Error')
        logging.info('Done pandoc for %s', file_config['source'])

    def run(self):
        """
        Compile a documentation PDF from a YAML config
        """
        make_sure_path_exists(OUT_FOLDER)

        if self.config['type'] == 'website':
            make_sure_path_exists(self.config['out_folder'])


        for file in self.config['bodies']:
            if file['type'] == 'content':
                self.pandoc_file(file)
                if self.config['type'] == 'website':
                    shutil.copyfile(file['generated'], os.path.join(self.config['out_folder'], os.path.basename(file['source'])))

        if self.config['type'] == 'website':
            return

        for file in self.config['abstract']:
            self.pandoc_file(file)
        for file in self.config['summary']:
            self.pandoc_file(file)

        template = LATEX_JINJA_ENV.get_template(self.config['template_file'])

        logging.info('Rendering template')
        out = template.render(**self.config)
        with open(self.config['name'] + self.get_file_extension(), 'w') as file:
            file.write(out)

        if not self.args.pandoc:
            logging.info('Rendering latex')
            self.write()
            if not self.args.fast:
                logging.info('Rendering latex, again')
                self.write() # twice for the toc

        logging.info('Done!')

def main():
    """
    Run the main
    """
    Build().run()

if __name__ == '__main__':
    main()
