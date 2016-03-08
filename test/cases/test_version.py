# -*- coding: utf-8 -*-
# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.


__requirements__ = []

def test_version(dut, profile):
    version = dut.execute('show version', encoding='json')
    assert profile['version'] in version
