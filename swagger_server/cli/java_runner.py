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
import subprocess

MAIN_OPTS = [
    'java',
    '-jar',
    '/home/cfw/Downloads/commons-ip2-cli-2.0.0.jar',
    'validate',
    '-i'
]
REP_OPTS = [
    '-r',
    'eark'
]

def java_runner(ip_root):
    command = MAIN_OPTS
    command.append(ip_root)
    command+=REP_OPTS
    proc_results = subprocess.run(command, capture_output=True)
    return proc_results.returncode, proc_results.stdout.rstrip(), proc_results.stderr
