# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import glob
import fnmatch

# from shakedown import BaseCollector

DEFAULT_PATTERN = 'test_*.py'

def collect(config, filter):

    filter = filter or ['.']
    print ("filter")
    print(filter)
    tests = []
    paths = []

    for path in filter:
        paths += glob.glob(os.path.abspath(path))

    for path in paths:
        if os.path.isfile(path):
           if fnmatch.fnmatch(os.path.basename(path), DEFAULT_PATTERN):
               tests.append(path)

        elif os.path.isdir(path):
            matches = glob.glob(os.path.join(path, DEFAULT_PATTERN))
            if matches:
                tests.extend(matches)
    print ("in collect")
    print (tests)
    return tests
