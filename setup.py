# -*- coding: utf-8 -*-
# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys
import os
from setuptools import setup, find_packages

if sys.version_info < (2, 7, 0):
    raise NotImplementedError("Sorry, you need at least Python 2.7 to install.")

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from shakedown import __version__

readme = open('README.md').read()

setup(
    name = "shakedown",
    version = __version__,
    author = "Jesse Mather",
    author_email = "jmather@arista.com",
    description = "",
    long_description = readme,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Terminals"
    ],
    packages = find_packages(),
    url = "https://github.com/mathershifter/shakedown",
    license = "MIT Licesnse",
    entry_points = {
        'console_scripts': [
            'shakedown = shakedown.entry:main',
        ]
    }
)
