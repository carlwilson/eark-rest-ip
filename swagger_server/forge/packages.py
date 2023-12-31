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
Factory methods for the package classes.
"""
import errno
import os
import tarfile
import tempfile
import zipfile

from swagger_server.forge import manifests
from swagger_server.forge import structure, metadata
from swagger_server.models import PackageDetails, ValidationReport

class ArchivePackageHandler():
    """Class to handle archive / compressed information packages."""
    def __init__(self, unpack_root=tempfile.gettempdir()):
        self._unpack_root = unpack_root

    @property
    def unpack_root(self):
        """Returns the root directory for archive unpacking."""
        return self._unpack_root

    def unpack_package(self, to_unpack, dest=None):
        """Unpack an archived package to a destination (defaults to tempdir).
        returns the destination folder."""
        if not os.path.isfile(to_unpack) or not self.is_archive(to_unpack):
            raise ValueError('Parameter "to_unpack": {} does not reference a file'
                'of known archive format (zip or tar).'.format(to_unpack))
        sha1 = manifests.Checksums.from_file(to_unpack)
        dest_root = dest if dest else self.unpack_root
        destination = os.path.join(dest_root, sha1.value)
        if zipfile.is_zipfile(to_unpack):
            with zipfile.ZipFile(to_unpack) as zip_ip:
                zip_ip.extractall(path=destination)
        elif tarfile.is_tarfile(to_unpack):
            with tarfile.open(to_unpack) as tar_ip:
                tar_ip.extractall(path=destination)
        return destination

    @staticmethod
    def is_archive(to_test):
        """Return True if the file is a recognised archive type, False otherwise."""
        if zipfile.is_zipfile(to_test):
            return True
        return tarfile.is_tarfile(to_test)

def get_ip_root(info_pack):
    # This is a var for the final source to validate
    to_validate = info_pack

    if not os.path.exists(info_pack):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), info_pack)
    if os.path.isfile(info_pack):
        # Check if file is a archive format
        if not ArchivePackageHandler.is_archive(info_pack):
            # If not we can't process
            raise ValueError('{} must be a zip/tar archive or an XML METS file.'.format(info_pack))
        # Unpack the archive and set the source
        to_validate = ArchivePackageHandler().unpack_package(info_pack)
    return to_validate, PackageDetails(name=os.path.basename(to_validate))

def validate(to_validate, struct_only=False):
    struct_valid, struct_results = structure.validate(to_validate)
    if not struct_valid or struct_only:
        return False, ValidationReport(structure=struct_results)
    md_valid, md_results = metadata.validate_ip(to_validate)
    return md_valid, ValidationReport(structure=struct_results, metadata=md_results)
