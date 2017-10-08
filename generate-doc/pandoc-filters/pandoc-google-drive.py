#!/usr/bin/env python

"""
Pandoc filter to replace google drive links with actual content
"""

__author__ = "Antoine Bolvy"

import re
import httplib2
import yaml
from panflute import run_filter, CodeBlock, RawBlock
from panflute.elements import builtin2meta
import sys
import os
import logging
import jinja2
from io import StringIO

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


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
        ',': r'{,}',
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

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = '../client_secret.json'
APPLICATION_NAME = 'Pandoc Google Sheets API Python'

class GDrive(object):
    def __init__(self, config):
        super().__init__()
        self.config = config;

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-lugdunum.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def fetch_data(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
        result = service.spreadsheets().values().get(
            spreadsheetId=self.config['doc_id'],
            range=self.config['range']
        ).execute()
        values = result.get('values', [])
        return values

    def generate_table(self):
        template = LATEX_JINJA_ENV.get_template('./gdrive-table.tex')

        lines = self.fetch_data()
        # print(data, file=sys.stderr)
        return template.render(lines=lines, columns_format=self.config['columns_format'])

def prepare(doc):
    """
    This function is called at the begining of the filter, it is used to initialize
    some more global variables, store them in the doc object which will be passed in
    each function later
    """
    doc.hash_prefix = doc.get_metadata('hash-prefix')

def handle_google_drive(elem, doc):
    """
    Do the heavy lifting
    """
    # Only interested in google-drive code blocks
    if not isinstance(elem, CodeBlock) or 'google-drive' not in elem.classes:
        return

    logger = logging.getLogger()

    log_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)8s] %(message)s')
    log_handler.setFormatter(formatter)

    gdrive = GDrive(yaml.load(elem.text))

    output_latex = gdrive.generate_table()
    return RawBlock(text=output_latex, format="latex")

def finalize(doc):
    """
    This function is called once at the end of the filter. Removes the global
    thingies we set earlier in prepare
    Also writes the counter initialization.
    """

    del doc.hash_prefix

def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(handle_google_drive, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == "__main__":
    main()
