#!/usr/bin/env python
# coding=UTF-8
#
# E-ARK Validation
# Copyright (C) 2019
# All rights reserved.
#
# Licensed to the E-ARK project under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The E-ARK project licenses
# this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""
E-ARK : Information package validation
        E-ARK Test Corpus processing
"""
import argparse
from datetime import datetime
import os.path
from pathlib import Path
import re
import sys
import zipfile
import io

from git import Repo
from jinja2 import Environment, PackageLoader

import swagger_server.forge.tests as TEST
from swagger_server.cli.testcases import TestCase, DEFAULT_NAME, GitTestCase
from swagger_server.cli.app import EXIT_CODES, process_ip
from swagger_server.forge.specification import SPECIFICATIONS
__version__ = "0.1.0"

defaults = {
    'description': """E-ARK Test Case validation (tc-check).
tc-check is a command-line tool to run test across corpora.""",
    'epilog': """
DILCIS Board (http://dilcis.eu)
See LICENSE for license information.
GitHub: https://github.com/E-ARK-Software/py-rest-ip-validator
Author: Carl Wilson (OPF), 2020
Maintainer: Carl Wilson (OPF), 2020"""
}

SKIPPED_KEYWORDS = [
    'rel',
    'master',
    'example',
    'doc',
    'feat',
    'gh-pages',
    'template'
]
class Corpus():
    """
    Encapsulates a test corpus of E-ARK information packages.
    """
    def __init__(self, name, root, cases=None):
        self._name = name
        self._root = root
        self._cases = {} if cases is None else self._load_cases(cases)

    @property
    def name(self):
        """Return the corpus name."""
        return self._name

    @property
    def root(self):
        """Return the corpus' root directory path."""
        return self._root

    @property
    def cases(self):
        """Generator to return test cases in a iterable form."""
        for case in self._cases.values():
            yield case

    @property
    def case_count(self):
        """Return the number of test cases in the corpus."""
        return len(self._cases)

    @property
    def rule_count(self):
        """Return the total number of validation rules in the corpus."""
        count = 0
        for case in self.cases:
            count+=len(case.rules)
        return count

    @property
    def package_count(self):
        """Return the total number of test packages in the corpus."""
        count = 0
        for case in self.cases:
            count+=case.package_count
        return count

    @property
    def missing_package_count(self):
        """Return the total number of test packages in the corpus."""
        count = 0
        for case in self.cases:
            count+=case.missing_package_count
        return count

    def case_by_id(self, case_id):
        """Return an individual test case by ID."""
        case = self._cases.get(case_id, None)
        return case

    def __str__(self):
        return "name:" + self.name + ", root:" + self.root + ", cases:" + str(self.case_count) + \
            ", rules:" + str(self.rule_count) + ", packages:" + str(self.package_count)

    @classmethod
    def _load_cases(cls, cases):
        cases_dict = {}
        for case in cases:
            cases_dict[case.case_id.requirement_id] = case
        return cases_dict

    @classmethod
    def from_root(cls, root, name):
        """Create a new corpus instance from a root directory."""
        if not os.path.exists(root) or not os.path.isdir(root):
            return None
        cases = _get_test_cases(root)
        return cls(name, root, cases)

class Corpora():
    """Encapsulates the full set of E-ARK corpora derived from the contents of
    the git repository."""
    def __init__(self, repo, corpora, skipped=None):
        self._repo = repo
        self._corpora = corpora
        self._skipped = skipped if skipped else []

    @property
    def git_path(self):
        """Return the git repository path."""
        return self._repo.common_dir

    @property
    def repo(self):
        """Return the git repo."""
        return self._repo

    @property
    def corpora(self):
        """Return the full copora dictionary."""
        return self._corpora

    def corpus_by_key(self, name):
        """Return a corpus by name."""
        return self._corpora[name]

    @classmethod
    def get_packages(cls, test_case):
        packages = {}
        for rule in test_case.rules:
            for package in rule.packages:
                imz = InMemoryZip()
                for path in _list_tree_paths(test_case.ref.commit.tree):
                    path_parts = str(path).lower().split('/')
                    if test_case.case_id.requirement_id.lower() in path_parts:
                        if package.name.lower() in path_parts:
                            blob = test_case.ref.commit.tree / str(path)
                            parts = str(path).split('/')
                            rel_parts = parts[parts.index(package.name):]
                            imz.append('/'.join(rel_parts),
                                       blob.data_stream.read())
                if imz.size() > 0:
                    packages[package.name] = imz
        return packages


    @property
    def skipped(self):
        """Return the list of skipped branches."""
        return self._skipped

    @classmethod
    def from_git_repo(cls, git_path):
        """Create all corpus instances from a git repository root."""
        # Open the passed path as if it were a git repo
        if not os.path.exists(git_path) or not os.path.isdir(git_path):
            raise ValueError('Parameter {} must be an existing directory.'.format(git_path))
        repo = Repo(git_path)
        # empty list to store the skipped branches
        skipped = []
        # Empty dictionary for the corpora
        case_lookup = {}
        for key in SPECIFICATIONS:
            # Empty list for each specification key
            case_lookup[key] = []
        # Loop through the remote branches
        for ref in repo.refs:
            if ref.name.replace('origin/', '') in SKIPPED_KEYWORDS:
                skipped.append(_skipped_item(ref.name, "On skipped list."))
                print('skipping {}'.format(ref.name))
                continue
            # Get the test case for this ref
            test_case, message = cls.test_case_from_ref(ref)
            if test_case is None:
                skipped.append(_skipped_item(ref.name, message))
                print('skipping {}: {}'.format(ref.name, message))
                continue
            try:
                case_lookup[test_case.case_id.specification].append(test_case)
            except AttributeError:
                skipped.append(_skipped_item(ref.name, message))
                continue
        corpora = cls.build_corpora(git_path, case_lookup)
        return cls(repo, corpora, skipped=skipped)

    @classmethod
    def build_corpora(cls, git_path, cases):
        """Return a corpus dictionary populated with passed cases."""
        corpora = {}
        for item, value in cases.items():
            corpora[item] = Corpus(item, git_path, value)
        return corpora

    @classmethod
    def test_case_from_ref(cls, ref):
        """Return the test case for a particular git reference."""
        name_parts = cls._get_ref_parts(ref.name)
        # The branch name should be 4 parts origin/<corpus>/<section>/<reqID>
        # If the path isn't 4 parts or the second element is not an recognised
        # corpus id then return nothing.
        if len(name_parts) < 3 and not ref.name.endswith('integration'):
            return None, 'Invalid branch name {} should have at least 3 parts.'.format(ref)
        # Check for a valid ID
        if not re.search(r'^{}[0-9]{{1,3}}$'.format('|'.join(SPECIFICATIONS)),
                         name_parts[-1].upper()):
            return None, 'Invalid branch name {}, '.format(ref) + \
                         'last element {} should be an id.'.format(name_parts[-1])
        # Iterate the paths of the blobs found for this commit tree
        for path in _list_tree_paths(ref.commit.tree):

            # get lower case path elements as a list
            path_parts = str(path).lower().split('/')

            # if the branch name requirement id is found in the path
            # AND the element name (without path, basename) is testCase.xml
            if (name_parts[-1].lower() in path_parts) & (path.name == DEFAULT_NAME):
                # test case match, return the results of parsing
                case, message = cls.test_case_from_tree_path(ref.commit.tree, path)
                return GitTestCase(ref, path, case), message

        # Never found a matching test case
        return None, 'No test case found for {}.'.format(ref.name)

    @classmethod
    def _get_ref_parts(cls, name):
        # If we have more than 3 parts just return the last 3 parts
        return name.split('/')[-3:]

    @classmethod
    def test_case_from_tree_path(cls, tree, path):
        """Return the test case parsed from the blob defined by tree and path params."""
        # get the blob from commit tree and path
        test_case_blob = tree / str(path)
        try:
            # Return the test case and it's path
            _tc = TestCase.from_xml_string(test_case_blob.data_stream.read())
            if not _tc.valid:
                return None, 'Test case XML failed schema validation for ' + \
                             '{}. \nSchema validation error: {}'.format(str(path),
                                                                        _tc.description)
            return _tc, str(path)
        except ValueError:
            # Bad test case XML.
            return None, 'Badly formed test case XML in file {}.'.format(str(path))

    @classmethod
    def test_case_from_path(cls, path):
        """Return the test case parsed from a path`."""
        try:
            # Return the test case and it's path
            _tc = TestCase.from_xml_file(path)
            if not _tc.valid:
                return None, 'Test case XML failed schema validation for ' + \
                             '{}. \nSchema validation error: {}'.format(str(path), _tc.description)
            return _tc, str(path)
        except ValueError:
            # Bad test case XML.
            return None, 'Badly formed test case XML in file {}.'.format(str(path))

    @classmethod
    def package_from_tree_path(cls, tree, path):
        """Return the test case parsed from the blob defined by tree and path params."""
        # get the blob from commit tree and path
        test_case_blob = tree / str(path)
        try:
            # Return the test case and it's path
            _tc = TestCase.from_xml_string(test_case_blob.data_stream.read())
            if not _tc.valid:
                return None, 'Test case XML failed schema validation for {}.'.format(str(path))
            return _tc, str(path)
        except ValueError:
            # Bad test case XML.
            return None, 'Badly formed test case XML in file {}.'.format(str(path))

def _skipped_item(ref, message):
    return {
        'ref': ref,
        'message': message
    }

def _list_tree_paths(root, path=Path('.')):
    for blob in root.blobs:
        yield path / blob.name
    for tree in root.trees:
        yield from _list_tree_paths(tree, path / tree.name)

ROOT = os.path.dirname(os.path.abspath(__file__))
env = Environment( loader = PackageLoader('swagger_server.cli') )

def app_html(root, specifications, corpora):
    """Write an HTML file home page."""
    template = _init_template('home.html')
    _mkdirs(root)
    with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as filehand:
        filehand.write(template.render(
            specifications=specifications,
            corpora=corpora
        ))

def skipped_html(root, skipped):
    """Write an HTML file for skipped branches."""
    template = _init_template('skipped.html')
    _mkdirs(root)
    with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as filehand:
        filehand.write(template.render(
            skipped=skipped
        ))

def corpus_html(root, corpus, specification):
    """Write an HTML file summarising a corpus."""
    if (root is None) | (corpus is None) | (specification is None):
        return
    template = _init_template('corpus.html')
    _mkdirs(root)
    with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as filehand:
        filehand.write(template.render(
            corpus = corpus,
            specification = specification,
        ))

def case_html(root, case):
    """Write an HTML file summarising a test case."""
    if case is None or case.case_id is None or case.case_id.requirement_id is None:
        return
    packages = Corpora.get_packages(case)
    template = _init_template('case.html')
    out_dir = os.path.join(root, case.case_id.requirement_id)
    _mkdirs(out_dir)
    for rule in case.rules:
        for package in rule.packages:
            if package.name in packages.keys():
                package.exists = True
            package_html(out_dir, case, rule, package, packages.get(package.name, None))
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as filehand:
        filehand.write(template.render(
            case = case,
            packages = len(packages),
        ))

def package_html(root, case, rule, package, zip):
    """Write an HTML file summarising a package."""
    template = _init_template('package.html')
    out_dir = os.path.join(root, package.name)
    _mkdirs(out_dir)
    if zip:
        zip.writetofile(os.path.join(out_dir, '{}.zip'.format(package.name)))
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as filehand:
        filehand.write(template.render(
            case = case,
            rule = rule,
            package = package,
            exists = (zip is not None)
        ))

def _mkdirs(_dir):
    try:
        os.makedirs(_dir)
    except FileExistsError:
        # directory already exists
        pass

def _init_template(name):
    template = env.get_template(name)
    template.globals['now'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    template.globals['url_root'] = './'
    return template

def _get_test_cases(root):
    cases = []
    for rootdir, subdirs, files in os.walk(root):
        for file in files:
            if file == DEFAULT_NAME:
                cases.append(rootdir)
        for subdir in subdirs:
            cases+=(_get_test_cases(subdir))
    return cases

# Create PARSER
PARSER = argparse.ArgumentParser(description=defaults['description'], epilog=defaults['epilog'])

class InMemoryZip():
    """In memory zip for quick package assembly."""
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = io.BytesIO()

    def size(self):
        ret_val = 0
        try:
            with zipfile.ZipFile(self.in_memory_zip, "r", zipfile.ZIP_DEFLATED, False) as _zf:
                ret_val = len(_zf.namelist())
        except zipfile.BadZipFile:
            return ret_val
        return ret_val

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode
        with zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False) as _zf:
            # Write the file to the in-memory zip
            _zf.writestr(filename_in_zip, file_contents)
            # Mark the files as having been created on Windows so that
            # Unix permissions are not inferred as 0000
            for zfile in _zf.filelist:
                zfile.create_system = 0

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        with open(filename, 'wb') as filehand:
            filehand.write(self.read())

def parse_command_line():
    """Parse command line arguments."""
    # Add arguments
    PARSER.add_argument('--verbose', '-v',
                        action="store_true",
                        dest="outputVerboseFlag",
                        default=False,
                        help="report results in verbose format")
    PARSER.add_argument('--version',
                        action='version',
                        version=__version__)
    PARSER.add_argument('files',
                        nargs='*',
                        default=[],
                        metavar='FILE',
                        help='Root IP folders or archived IPs to check.')

    # Parse arguments
    args = PARSER.parse_args()

    return args

def main():
    """Main command line application."""
    _exit = 0
    # Get input from command line
    args = parse_command_line()
    # If no target files or folders specified then print usage and exit
    if not args.files:
        PARSER.print_help()

    # for file_arg in args.files:
    #     git_corpus = Corpora.from_git_repo(file_arg)
    #     for key in SPECIFICATIONS:
    #         corpus = git_corpus.corpora[key]
    #         if corpus:
    #             for case in corpus.cases:
    #                 case_html(os.path.join('results', key), case)
    #             corpus_html(os.path.join('results', key), corpus, SPECIFICATIONS[key])

    for file_arg in args.files:
        cases = _get_test_cases(file_arg)
        for case in cases:
            ret_stat, path = _process_test_case(case)
            if ret_stat > 0:
                sys.stderr.write(EXIT_CODES[ret_stat].format(path))
                sys.stderr.write(os.linesep)
                _exit = ret_stat
                continue
    # app_html('results', SPECIFICATIONS, git_corpus.corpora)
    # skipped_html(os.path.join('results', 'skipped'), git_corpus.skipped)
    sys.exit(_exit)

def _compare_results(report_a, report_b):
    structs_equiv = TEST.compare_result_lists(report_a.structure.messages,
                                              report_b.structure.messages)
    print('COMPARING Structure Results: %s' % (structs_equiv))
    schm_equiv = TEST.compare_result_lists(report_a.metadata.schema_results.messages,
                                           report_b.metadata.schema_results.messages)
    print('COMPARING Schema Results: %s' % (schm_equiv))
    schmtrn_equiv = TEST.compare_result_lists(report_a.metadata.schematron_results.messages,
                                              report_b.metadata.schematron_results.messages)
    print('COMPARING Schematron Results: %s' % (schmtrn_equiv))
    return structs_equiv and schm_equiv and schmtrn_equiv

def _process_test_case(case_path):
    test_case = None
    try:
        test_case = TestCase.from_path(case_path)
    except FileNotFoundError:
        return 1, case_path
    except ValueError:
        return 3, case_path
    print('')
    print('TEST CASE: {}'.format(test_case))
    for rule in test_case.rules:
        print('    RULE: {}'.format(rule))
        for package in rule.packages:
            print('        PACKAGE: {}'.format(package))
            ret_stat, validation_report = process_ip(package.resolve_path(case_path),
                                                      metadata= (not test_case.is_struct))
    return 0, case_path


if __name__ == "__main__":
    main()
