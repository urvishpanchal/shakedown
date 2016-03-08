# -*- coding: utf-8 -*-
# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import pytest
import os

from shakedown.config import Config

def test_config():
    c = Config({'a': 1, 'b': 1, 'c': {'a': 2}})
    print c
