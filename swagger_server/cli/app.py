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
        Command line validation application
"""
import argparse
import json
import os.path
import sys

import swagger_server.cli.testcases as TC
import swagger_server.cli.java_runner as JR
import swagger_server.forge.packages as PKG
from swagger_server.models import ValidationReport

__version__ = "0.1.0"

defaults = {
    'description': """E-ARK Information Package validation (ip-check).
ip-check is a command-line tool to analyse and validate the structure and
metadata against the E-ARK Information Package specifications.
It is designed for simple integration into automated work-flows.""",
    'epilog': """
DILCIS Board (http://dilcis.eu)
See LICENSE for license information.
GitHub: https://github.com/E-ARK-Software/py-rest-ip-validator
Author: Carl Wilson (OPF), 2020
Maintainer: Carl Wilson (OPF), 2020"""
}

EXIT_CODES = {
    0: 'Execution completed successfully.',
    1: '{} is not an existing file or directory.',
    2: '{} must be a zip/tar archive or an XML METS file.',
    3: 'Badly formed test case XML in file {}.'
}

# Create PARSER
PARSER = argparse.ArgumentParser(description=defaults['description'], epilog=defaults['epilog'])

def parse_command_line():
    """Parse command line arguments."""
    # Add arguments
    PARSER.add_argument('--testcase', '-t',
                        action="store_true",
                        dest="testCase",
                        default=False,
                        help="Treat [FILE]s as XML test cases and drive validation from those.")
    PARSER.add_argument('--recurse', '-r',
                        action="store_true",
                        dest="inputRecursiveFlag",
                        default=True,
                        help="When analysing an information package recurse into representations.")
    PARSER.add_argument('--checksum', '-c',
                        action="store_true",
                        dest="inputChecksumFlag",
                        default=False,
                        help="Calculate and verify file checksums in packages.")
    PARSER.add_argument('--verbose', '-v',
                        action="store_true",
                        dest="outputVerboseFlag",
                        default=False,
                        help="report results in verbose format")
    PARSER.add_argument('--structure', '-s',
                        action="store_true",
                        dest="structureFlag",
                        default=False,
                        help="run package structure tests only")
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
    # Get input from command line
    args = parse_command_line()
    # If no target files or folders specified then print usage and exit
    if not args.files:
        PARSER.print_help()
    _exit = _process_test_cases(args) if args.testCase else _process_ips(args)
    print('Exiting with {}'.format(_exit))
    sys.exit(_exit)

def _process_ips(args):
    # Iterate the file arguments
    _exit = 0
    for file_arg in args.files:
        # Get the package root and find out if this is something we can validate
        ret_stat, _ = _process_ip(file_arg, args.structureFlag)
        # if ret_stat > 0 then this is somethign we can't handle
        if ret_stat > 0:
            sys.stderr.write(EXIT_CODES[ret_stat].format(file_arg))
            sys.stderr.write(os.linesep)
            _exit = ret_stat
            continue
    return _exit

def _process_ip(info_pack, struct_only):
    to_validate = info_pack
    try:
        to_validate, _ = PKG.get_ip_root(info_pack)
    except FileNotFoundError:
        return 1, info_pack
    except ValueError:
        return 2, info_pack
    is_valid, validation_report = PKG.validate(to_validate, struct_only=struct_only)
    ret_code, file_name, stderr = JR.java_runner(to_validate)
    print('ret: {}, stdout: {}'.format(ret_code, file_name))
    if ret_code == 0:
        f = open(file_name, 'r')
        contents = f.read()
        f.close()
        os.remove(file_name)

        rep = ValidationReport(**json.loads(contents))
        print(rep)
    else:
        print('')
        print('ERROR')
        print(stderr)
        print('')
    print(validation_report)
    return 0, None

def _process_test_cases(args):
    # Iterate the file arguments
    _exit = 0
    for file_arg in args.files:
        # Get the package root and find out if this is something we can validate
        ret_stat, path = _process_test_case(file_arg)
        # if ret_stat > 0 then this is somethign we can't handle
        if ret_stat > 0:
            sys.stderr.write(EXIT_CODES[ret_stat].format(path))
            sys.stderr.write(os.linesep)
            _exit = ret_stat
            continue
    return _exit

def _process_test_case(case_path):
    test_case = None
    try:
        test_case = TC.TestCase.from_path(case_path)
    except FileNotFoundError:
        return 1, case_path
    except ValueError:
        return 3, case_path
    print(test_case)
    for rule in test_case.rules:
        for package in rule.packages:
            ret_stat, validation_report = _process_ip(package.resolve_path(case_path),
                                                      struct_only=test_case.is_struct)
            if ret_stat > 0:
                return ret_stat, validation_report
    return 0, case_path


# def _test_case_schema_checks():
if __name__ == "__main__":
    main()
