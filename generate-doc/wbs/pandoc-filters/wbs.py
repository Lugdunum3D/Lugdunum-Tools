#!/usr/bin/env python

"""
Pandoc filter to replace wbs config to actual schematics
"""

__author__ = "Antoine Bolvy"

import re
import yaml
from panflute import run_filter, CodeBlock, RawBlock
from panflute.elements import builtin2meta
import sys
import os
import logging
import jinja2
import csv
from io import StringIO

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
        ',': r'\,',
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

class WBSTree(object):
    def __init__(self, source, root_name):
        super().__init__()
        self.tree = None
        self.root_name = root_name
        if not self.parse_tree(source):
            logging.error('Failed to parse tree %s', source)
            sys.exit(1)

    def parse_tree(self, source):
        with open(source) as csv_f:
            reader = csv.reader(csv_f)
            next(reader, None)

            lines = []
            self.tree = {
                'level': 0,
                'name': self.root_name,
                'desc': '',
                'children': []
            }
            levels = [self.tree]
            for i, line in enumerate(reader):
                if not ''.join(line).strip():  # skip empty lines
                    continue

                level = line[1].count("    ") + 1
                node = {
                    'level': level,
                    'name': line[1].strip(),
                    'desc': line[2],
                    'children': []
                }
                # print(level, len(levels) - 1, level == len(levels) - 1, level > len(levels) - 1, node['name'])
                # print(levels)
                if level == len(levels) - 1:
                    # We're on the same level of the tree, we want to append our node,
                    # and make that if there is a subtree comming it will add to its
                    # children

                    # add the node to the parent
                    levels[-2]['children'].append(node)
                    # replace the last level with the current node
                    levels[-1] = node
                elif level > len(levels) - 1:
                    # We have a new level
                    levels[-1]['children'].append(node)
                    levels.append(node)
                else:
                    # Back one level
                    del levels[level:-1]
                    levels[-2]['children'].append(node)
                    levels[-1] = node
            return True
        return False

    def find_subtree(self, name):

        def _find_subtree(tree, name, level=0, indexes=[]):
            # print('_find_subtree ', tree['name'], indexes)
            if tree['name'] == name:
                return indexes, tree, level
            for i, child in enumerate(tree['children']):
                _indexes, _subtree, _level = _find_subtree(child, name, level + 1, indexes + [i])
                # _find_subtree worked, so we return its results, or we continue
                if _subtree != None:
                    return _indexes, _subtree, _level
            # end of the function, return empty results
            return [], None, None

        return _find_subtree(self.tree, name, 0, [])

    def generate_forest(self, template, doc, config, indexes=[], subtree=None, starting_level=0):

        if not subtree:
            subtree = self.tree

        max_level = 0
        counter_prefix = doc.hash_prefix + 'treecounter'

        def _gen_counter(level):
            """
            Utility to generate a counter string in latex, e.g. "2.5.5.3" in function of the level
            """
            counters = []
            nonlocal max_level
            if max_level < level:
                max_level = level
            for level in range(1, level + 1):
                counters.append(counter_prefix + str(level))
            return ''.join(["\\arabic{" + counter + "}." for counter in counters])

        out = StringIO()
        def _gen_forest(tree, level=0):
            if level == 0:
                out.write("[" + tex_escape(tree['name']))
            else:
                counter = counter_prefix + str(level)
                out.write(level * "  " + "[\\stepcounter{" + counter + "}" + _gen_counter(level) + " " + tex_escape(tree['name']))
            if not len(tree['children']) or (level > config['limit'] and config['limit'] != -1):  # level limit
                out.write("]\n")
            else:
                print(level, config['limit'], file=sys.stderr)
                out.write("\n")
                for child in tree['children']:
                    if level == starting_level and 'show' in config and child['name'] not in config['show']:  # if is hidden
                        # we still need to add a step to the counter
                        counter = counter_prefix + str(level + 1)
                        out.write((level + 1) * "  " + "\\stepcounter{" + counter + "}\n")
                    else:
                        _gen_forest(child, level + 1)

                out.write(level * "  " + "]\n")

        _gen_forest(subtree, starting_level)

        initial_values = []
        for curr_level in range(1, max_level + 1):
            doc.wbs_counters.add(counter_prefix + str(curr_level))
            if curr_level - 1 < len(indexes):
                if curr_level == starting_level:
                    initial_values.append([counter_prefix + str(curr_level), indexes[curr_level - 1]])
                else:
                    initial_values.append([counter_prefix + str(curr_level), indexes[curr_level - 1] + 1])


        return template.render(content=out.getvalue(), counters=initial_values)

def prepare(doc):
    doc.wbs_counters = set()
    doc.hash_prefix = doc.get_metadata('hash-prefix')

def handle_wbs(elem, doc):
    """
    Do the heavy lifting
    """
    # Only interested in wbs code blocks
    if not isinstance(elem, CodeBlock) or 'wbs' not in elem.classes:
        return

    logger = logging.getLogger()

    log_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)8s] %(message)s')
    log_handler.setFormatter(formatter)

    template = LATEX_JINJA_ENV.get_template('./wbs.tex')

    config = yaml.load(elem.text)

    tree = WBSTree(config['features'], config['root_name'])
    if 'subtree' not in config:
        config['subtree'] = config['root_name']

    indexes, subtree, level = tree.find_subtree(config['subtree'])
    if not subtree:
        print("Tree '{}' not found".format(config['subtree']))
        sys.exit(1)

    print(indexes, file=sys.stderr)

    forest_latex = tree.generate_forest(template, doc, config, indexes, subtree, level)
    return RawBlock(text=forest_latex, format="latex")

def finalize(doc):
    template = LATEX_JINJA_ENV.get_template('./counters.tex')
    # add the counters at the beginning of the page
    doc.content.insert(0, RawBlock(text=template.render(counters=sorted(list(doc.wbs_counters))), format="latex"))
    del doc.wbs_counters, doc.hash_prefix

def main(doc=None):
    """
    Run the fitler
    """
    return run_filter(handle_wbs, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == "__main__":
    main()
