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

class WBSTree(object):
    def __init__(self, tree=None, level=0, indexes=[]):
        super().__init__()
        self.tree = tree
        self.level = level
        self.indexes = indexes

    def print(self):

        def _print(tree, level):
            data = '    ' * level + tree['name']
            print(data + (50 - len(data)) * ' ' + '| ' + tree['desc'], file=sys.stderr)
            for child in tree['children']:
                _print(child, level + 1)

        _print(self.tree, self.level)

    def get_completed(self, subtree=None):
        if not subtree:
            subtree = self.tree

        def _get_completed(tree):
            avg_values = []
            if not len(tree['children']):
                return tree['percentage']
            for child in tree['children']:
                avg_values.append(_get_completed(child))
            return sum(avg_values) / len(avg_values)
        return _get_completed(subtree)

    def parse_tree(self, source, root_name):
        with open(source) as csv_f:
            reader = csv.reader(csv_f)
            next(reader, None)

            lines = []
            self.tree = {
                'level': 0,
                'percentage': 0,
                'name': root_name,
                'desc': '',
                'type': '',
                'children': []
            }
            levels = [self.tree]
            for i, line in enumerate(reader):
                if not ''.join(line).strip():  # empty line means last section ends
                    levels[-1]['type'] = 'last_of_group'
                    continue
                level = line[2].count("    ") + 1
                node = {
                    'level': level,
                    'percentage': int(line[1]) if line[1] is not '' else 0,
                    'name': line[2].strip(),
                    'desc': line[3],
                    'type': line[4],
                    'children': []
                }
                print(line[4], file=sys.stderr)
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
                return tree, level, indexes
            for i, child in enumerate(tree['children']):
                # print(i, child['name'], file=sys.stderr)
                _subtree, _level, _indexes = _find_subtree(child, name, level + 1, indexes + [i])
                # _find_subtree worked, so we return its results, or we continue
                if _subtree != None:
                    # print(i, 'FOUND', file=sys.stderr)
                    return _subtree, _level, _indexes
            # end of the function, return empty results
            return None, None, []

        subtree, level, indexes = _find_subtree(self.tree, name, self.level, self.indexes)

        if subtree == None:
            return None

        new_tree = WBSTree(subtree, level, indexes)
        # print(indexes, level, file=sys.stderr)
        # new_tree.print()
        # sys.exit(1)
        return new_tree

    def generate_initial_values(self, doc, counter_prefix, max_level):
        initial_values = []
        for curr_level in range(1, max_level + 1):
            doc.wbs_counters.add(counter_prefix + str(curr_level))
            if curr_level - 1 < len(self.indexes):
                if curr_level == self.level:
                    initial_values.append([counter_prefix + str(curr_level), self.indexes[curr_level - 1]])
                else:
                    initial_values.append([counter_prefix + str(curr_level), self.indexes[curr_level - 1] + 1])
            else:
                initial_values.append([counter_prefix + str(curr_level), 0])
        return initial_values

    def generate_forest(self, doc, config):
        template = LATEX_JINJA_ENV.get_template('./wbs.tex')

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
            if level == 0:  # we are at the root
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
                    if level == self.level and 'show' in config and child['name'] not in config['show']:  # if is hidden
                        # we still need to add a step to the counter
                        counter = counter_prefix + str(level + 1)
                        out.write((level + 1) * "  " + "\\stepcounter{" + counter + "}\n")
                    else:
                        _gen_forest(child, level + 1)

                out.write(level * "  " + "]\n")

        _gen_forest(self.tree, self.level)

        return template.render(content=out.getvalue(), counters=self.generate_initial_values(doc, counter_prefix, max_level))

    def generate_table(self, doc, config):
        template = LATEX_JINJA_ENV.get_template('./wbs-table.tex')

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

        lines = []

        out = StringIO()
        def _gen_table(tree, level=0):
            line = []

            if level != 0:
                counter = counter_prefix + str(level)

                value = '\\textbf{' + tex_escape(tree['name']) + '}' if tree['type'] == 'group' else tex_escape(tree['name'])

                lines.append({
                    'type': tree['type'],
                    'data': [
                        "\\stepcounter{" + counter + "}" + _gen_counter(level),
                        str(int(self.get_completed(tree))) + "\\%",
                        "\\parshape 1 " + str(level - 1) + "em \\dimexpr\\linewidth-" + str(level - 1) + "em\\relax " + value,
                        tex_escape(tree['desc'])
                    ]
                })

            if not len(tree['children']) or (level > config['limit'] and config['limit'] != -1):  # level limit
                return

            for child in tree['children']:
                if level == self.level and 'show' in config and child['name'] not in config['show']:  # if is hidden
                    # we still need to add a step to the counter
                    counter = counter_prefix + str(level + 1)
                    # out.write((level + 1) * "  " + "\\stepcounter{" + counter + "}\n")
                else:
                    _gen_table(child, level + 1)

            # out.write(level * "  " + "]\n")

        _gen_table(self.tree, self.level)

        # print(lines, file=sys.stderr)

        return template.render(lines=lines, counters=self.generate_initial_values(doc, counter_prefix, max_level))

def prepare(doc):
    """
    This function is called at the begining of the filter, it is used to initialize
    some more global variables, store them in the doc object which will be passed in
    each function later
    """
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

    config = yaml.load(elem.text)

    tree = WBSTree()
    if not tree.parse_tree(config['features'], config['root_name']):
        logging.error('Failed to parse tree %s', source)
        sys.exit(1)

    if 'subtree' not in config:
        config['subtree'] = config['root_name']


    subtree = tree.find_subtree(config['subtree'])
    if not subtree:
        logging.error('Tree %s not found', config['subtree'])
        sys.exit(1)

    subtree.print()

    output_latex = ''
    if config['type'] == 'tree':
        output_latex = subtree.generate_forest(doc, config)
    elif config['type'] == 'table':
        output_latex = subtree.generate_table(doc, config)
    return RawBlock(text=output_latex, format="latex")

def finalize(doc):
    """
    This function is called once at the end of the filter. Removes the global
    thingies we set earlier in prepare
    Also writes the counter initialization.
    """

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
