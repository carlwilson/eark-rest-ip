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
"""METS Schema validation."""
import fnmatch
import logging
import os

from lxml import etree
from lxml.isoschematron import Schematron

from importlib_resources import files

import swagger_server.forge.resources.schemas as SCHEMA
import swagger_server.forge.resources.schematron as SCHEMATRON
from swagger_server.models import (
    MetadataStatus,
    TestResult,
    Severity,
    MetadataChecks,
    MetadataResults,
    Checksum,
    ChecksumAlg
)

XLINK_NS = 'http://www.w3.org/1999/xlink'
METS_NS = 'http://www.loc.gov/METS/'
QUAL_METS_NS = '{{{}}}'.format(METS_NS)

DILCIS_EXT_NS = 'https://DILCIS.eu/XML/METS/CSIPExtensionMETS'
SCHEMATRON_NS = "{http://purl.oclc.org/dsdl/schematron}"
SVRL_NS = "{http://purl.oclc.org/dsdl/svrl}"
ALGS = vars(ChecksumAlg)

class FileRef():
    def __init__(self, path, size, checksum):
        self._path = path
        self._size = size
        self._checksum = checksum

    @property
    def path(self):
        return self._path

    @property
    def size(self):
        return self._size

    @property
    def checksum(self):
        return self._checksum

    def __str__(self):
        return '\'path\': \'{}\' \'size\': \'{}\' \'checksum\': \'{}\''.format(self.path, self.size, self.checksum)

class MetsValidator():
    """Encapsulates METS schema validation."""
    def __init__(self, root):
        self.validation_errors = []
        self.schema_wrapper = etree.XMLSchema(file=str(files(SCHEMA).joinpath('wrapper.xsd')))
        self.rootpath = root
        self.subsequent_mets = []
        self.file_refs = []

    def validate_mets(self, mets):
        '''
        Validates a Mets file. The Mets file is parsed with etree.iterparse(),
        which allows event-driven parsing of large files. On certain events/conditions
        actions are taken, like file validation or adding Mets files found inside
        representations to a list so that they will be evaluated later on.

        @param mets:    Path leading to a Mets file that will be evaluated.
        @return:        Boolean validation result.
        '''
        # Handle relative package paths for representation METS files.
        self.rootpath, mets = _handle_rel_paths(self.rootpath, mets)
        try:
            parsed_mets = etree.iterparse(mets, events=('start', 'end'), schema=self.schema_wrapper)
            for event, element in parsed_mets:
                # Define what to do with specific tags.
                if event == 'end' and element.tag == _q(METS_NS, 'file'):
                    # files
                    self.file_refs.append(_file_ref_from_ele(element))
                    # element.clear()
                    # while element.getprevious() is not None:
                    #     del element.getparent()[0]
                elif event == 'end' and \
                    element.tag == _q(METS_NS, 'fileGrp') and \
                    element.attrib.get('USE', '').startswith('Representations/'):
                    # representation mets files
                    rep = element.attrib['USE'].rsplit('/', 1)[1]
                    for file in element.iter(_q(METS_NS, 'file')):
                        file_ref = _file_ref_from_ele(file)
                        if os.path.basename(file_ref.path).casefold() == 'METS.xml'.casefold():
                            sub_mets = rep, file_ref
                            self.subsequent_mets.append(sub_mets)
                        else:
                            self.file_refs.append(file_ref)
                    # element.clear()
                    # while element.getprevious() is not None:
                    #     del element.getparent()[0]
                elif event == 'end' and element.tag == _q(METS_NS, 'dmdSec'):
                    for ref in element.iter(_q(METS_NS, 'mdRef')):
                        self.file_refs.append(_file_ref_from_mdref_ele(ref))
                elif event == 'end' and element.tag == _q(METS_NS, 'amdSec'):
                    for ref in element.iter(_q(METS_NS, 'mdRef')):
                        self.file_refs.append(_file_ref_from_mdref_ele(ref))
        except etree.XMLSyntaxError as synt_err:
            self.validation_errors.append(TestResult(rule_id="METS", location=mets,
                                          message=synt_err.msg.replace(QUAL_METS_NS, "mets:"),
                                          severity=Severity.ERROR))
        # except Exception as base_err:
        #     self.validation_errors.append(TestResult(rule_id="METS", location=mets,
        #                                   message=str(base_err), severity=Severity.ERROR))

        status = MetadataStatus.NOTVALID if len(self.validation_errors) else MetadataStatus.VALID
        return status == MetadataStatus.VALID, MetadataChecks(status=status, messages=self.validation_errors)

def _file_ref_from_ele(element):
    algid = element.attrib.get('CHECKSUMTYPE', None)
    chksm = element.attrib.get('CHECKSUM', None)
    size = element.attrib.get('SIZE', None)
    checksum = None
    ref = None
    for alg in ALGS:
        if getattr(ChecksumAlg, alg) == algid:
            checksum = Checksum(algid, chksm)
    for child in element.getchildren():
        if child.tag == _q(METS_NS, 'FLocat'):
            path = child.attrib[_q(XLINK_NS, 'href')]
            ref = FileRef(path, size, checksum)
    return ref

def _file_ref_from_mdref_ele(element):
    algid = element.attrib.get('CHECKSUMTYPE', None)
    chksm = element.attrib.get('CHECKSUM', None)
    size = element.attrib.get('SIZE', None)
    checksum = None
    ref = None
    for alg in ALGS:
        if getattr(ChecksumAlg, alg) == algid:
            checksum = Checksum(algid, chksm)
    path = element.attrib.get(_q(XLINK_NS, 'href'), None)
    ref = FileRef(path, size, checksum)
    return ref


def _handle_rel_paths(rootpath, metspath):
    if metspath.startswith('file://./'):
        relpath = os.path.join(rootpath, metspath[9:])
        # change self.rootpath to match any relative path found in the
        # current (subsequent) mets
        return relpath.rsplit('/', 1)[0], relpath
    return metspath.rsplit('/', 1)[0], metspath

def _q(_ns, _v):
    return '{{{}}}{}'.format(_ns, _v)

class ValidationRules():
    REP_SKIPS = [
        'CSIP60',
        'CSIP97',
        'CSIP101',
        'CSIP113',
        'CSIP114'
    ]
    """Encapsulates a set of Schematron rules loaded from a single file."""
    def __init__(self, name: str, rules_path: str=None):
        """Initialise a set of validation rules from a file or name.

        Retrieve a validation profile by type and version # noqa: E501

        :param name: The name of the rule set once loaded. If no path is provided
                     this param will be compared to the standard set of rules and
                     a matching rule set will be loaded if found. For reference the
                     standard ruleset corresponds to the different METS file sections
                     i.e. amd, dmd, file, hdr, root, structmap
        :type type: str
        :param rules_path: A complete path to a set of schematron rules to load
        :type version: str
        """
        self.name = name
        if not rules_path:
            # If no path is provided use the name param to try to load a standard ruleset
            rules_path = str(files(SCHEMATRON).joinpath('mets_{}_rules.xml'.format(name)))
        self.rules_path = rules_path
        logging.debug("path: %s", self.rules_path)
        # Load the schematron file from the path
        self.ruleset = Schematron(file=self.rules_path, store_schematron=True, store_report=True)

    def get_assertions(self):
        """Generator that returns the rules one at a time."""
        xml_rules = etree.XML(bytes(self.ruleset.schematron))

        for ele in xml_rules.iter():
            if ele.tag == SCHEMATRON_NS + 'assert':
                yield ele

    def validate(self, to_validate):
        """Validate a file against the loaded Schematron ruleset."""
        xml_file = etree.parse(to_validate)
        self.ruleset.validate(xml_file)

    def get_report(self):
        """Get the report from the last validation."""
        xml_report = etree.XML(bytes(self.ruleset.validation_report))
        messages = []
        rule = None
        status = MetadataStatus.VALID
        for ele in xml_report.iter():
            if ele.tag == SVRL_NS + 'fired-rule':
                rule = ele
            elif ele.tag == SVRL_NS + 'failed-assert':
                rule_id = ele.get('id', '')
                if rule_id in self.REP_SKIPS:
                    continue
                severity = Severity.WARN
                if ele.get('role') == 'ERROR':
                    severity = Severity.ERROR
                    status = MetadataStatus.NOTVALID
                elif ele.get('role') == 'INFO':
                    severity = Severity.INFO
                messages.append(
                    TestResult(
                        rule_id=ele.get('id'),
                        location=rule.get('context').replace('/*[local-name()=\'', '') +
                        '/' + ele.get('test'),
                        message=ele.find(SVRL_NS + 'text').text,
                        severity=severity
                    )
                )

        return MetadataChecks(status=status, messages=messages)

class ValidationProfile():
    """ A complete set of Schematron rule sets that comprise a complete validation profile."""
    NAMES = {
        'root': 'METS Root',
        'hdr': 'METS Header',
        'amd': 'Adminstrative Metadata',
        'dmd': 'Descriptive Metadata',
        'file': 'File Section',
        'structmap': 'Structural Map'
    }
    SECTIONS = NAMES.keys()

    def __init__(self):
        self.rulesets = {}
        self.is_valid = False
        self.is_wellformed = False
        self.results = {}
        self.messages = []
        for section in self.SECTIONS:
            self.rulesets[section] = ValidationRules(section)

    def validate(self, to_validate, is_root=True):
        """Validates a file against each loaded ruleset."""
        is_valid = True
        self.is_wellformed = True
        self.results = {}
        self.messages = []
        for section in self.SECTIONS:
            try:
                self.rulesets[section].validate(to_validate)
            except etree.XMLSyntaxError as parse_err:
                self.is_wellformed = False
                self.is_valid = False
                self.messages.append(parse_err.msg)
                return
            self.results[section] = self.rulesets[section].get_report()
            if self.results[section].status != MetadataStatus.VALID:
                is_valid = False
        self.is_valid = is_valid
        messages = []
        status = MetadataStatus.VALID
        for sect, result in self.results.items():
            messages+=result.messages
            if result.status == MetadataStatus.NOTVALID:
                status = MetadataStatus.NOTVALID
        return status != MetadataStatus.NOTVALID, MetadataChecks(status=status, messages=messages)


    def get_results(self):
        """Return the full set of results."""
        return self.results

    def get_result(self, name):
        """Return only the results for element name."""
        return self.results.get(name)

def validate_ip(to_validate):
    # Schematron validation profile
    schema_results = {}
    schematron_results = {}
    package_files = {}
    validator = MetsValidator(to_validate)
    mets_path = os.path.join(to_validate, 'METS.xml')
    results = validator.validate_mets(mets_path)
    schema_results['root'] = results
    package_files['root'] = validator.file_refs
    for mets in validator.subsequent_mets:
        sub_validator = MetsValidator(mets[1].path)
        schema_results[mets[0]] = sub_validator.validate_mets(os.path.join(to_validate,
                                                                           mets[1].path))
        package_files[mets[0]] = sub_validator.file_refs
    profile = ValidationProfile()
    schematron_results['root'] = profile.validate(mets_path)
    for name, result in schema_results.items():
        if result[0]:
            for mets in validator.subsequent_mets:
                mets_path = mets[1].path
                schematron_results[mets[0]] = profile.validate(os.path.join(to_validate, mets_path),
                                                               False)
    return schema_results['root'][0] and schematron_results['root'][0], MetadataResults(results[1], schematron_results)
