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
Factory methods for validation testing classes.
"""
from swagger_server.forge import structure


class Structure():
    """
    Generate structure validation results from testable sources.
    """
    @classmethod
    def from_directory(cls, to_test):
        """Returns a structure test result from an information package directory root."""
        structure_tester = structure.PackageStructTests(to_test)
        return structure_tester.get_test_results()

    @classmethod
    def from_archive(cls, to_test):
        """Returns a structure test result from an information package archive (zip or tar)."""
        pass

    @classmethod
    def from_manifest(cls, to_test):
        """Returns a structure test result from a maninfest instance."""
        pass
