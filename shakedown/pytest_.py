# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import os
import pytest
import arcomm
#import report

# def pytest_addoption(parser):
#     """pytest hook for adding conosole options"""
#     group = parser.getgroup('autotest', 'autotest network device testing')
#     group.addoption('--dut', action='store', metavar="DUT")
#     group.addoption('--working-dir', action='store', metavar='working_path',
#                     help=('base directory for tests, templates and '
#                           'profiles.  By default use current dir'))
#     group.addoption('--output-dir', action='store', metavar='output_path',
#                     help='base directory for reports')
#     group.addoption("--run-slow", action="store_true",
#                     help="run slow tests")
#     group.addoption("--rescan", action="store_true",
#                     help=("rescan output directory and regenerate html"
#                           "reports, but don't run any test cases"))

def mkdir(path):
    """Create a directory and ignore directory already exists errors"""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        import errno
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class ShakedownPlugin(object):

    def __init__(self, config):
        self.config = config

    @pytest.mark.tryfirst
    def pytest_configure(self, config):
        """pytest hook for handling extra command line args"""

        # if not config.option.working_dir:
        #     config.option.working_dir = os.getcwd()
        #
        # outputdir = config.option.output_dir
        # if outputdir:
        #     outputdir = os.path.expanduser(outputdir)
        #     mkdir(outputdir)
        # config.option.resultlog = os.path.join(outputdir, "result.log")

    def pytest_unconfigure(self, config):
        """pytest hook - called after all tests have completed"""
        # outputdir = config.option.output_dir
        # if outputdir:
        #    reporting.generate(outputdir)
        # indexer.index(outputdir)

    def pytest_ignore_collect(self, path, config):
        """ignore all directories if 'rescan' options is used. also make sure the
        '--dut' option is used"""
        # pylint: disable=unused-argument
        # if config.option.rescan:
        #     if not config.option.output_dir:
        #         pytest.exit("'--output-dir' is required with option '--rescan'")
        #     return True
        # if not config.option.dut:
        #     pytest.exit("'--dut' option is required to run tests")

    def pytest_runtest_setup(self, item):
        """run before executing test"""
        if "slow" in item.keywords and not item.config.getoption("--run-slow"):
            pytest.skip("need --run-slow option to run")
        if "obsolete" in item.keywords:
            pytest.skip("Skipping obsolete test")

        # section = autocert.report.section(item.nodeid)
        # if item.function.__doc__:
        #     section.header(item.function.__doc__, 3)

    def pytest_runtest_teardown(self, item):
        """Call after the test completes to update the report description"""

    def pytest_runtest_logreport(self, report):
        """Call after the test completes to update the outcome and trace"""
        # if report.when == "call":
        #     section = autocert.report.section(report.nodeid)
        #     section.paragraph("__Outcome: {}__".format(report.outcome.upper()))
        #     section.outcome = report.outcome
        #     section.duration = report.duration
        #     if report.longrepr:
        #         section.codeblock(report.longrepr)

    @pytest.fixture(scope='session')
    def dut(self):

        # hostname field is required, others have defaults
        hostname = self.config['dut']['hostname']
        user = self.config['dut'].get('username', 'admin')
        password = self.config['dut'].get('password', '')
        authorize = self.config['dut'].get('authorize', '')
        protocol = self.config['dut'].get('protocol', 'eapi')

        conn = arcomm.connect(hostname, (user, password), protocol=protocol)
        conn.authorize()

        return conn

    @pytest.fixture(scope='session')
    def profile(self):
        pass

def run(config, tests): #, report):
    opts = config.get('addopts', '').split()
    opts += tests
    print opts
    pytest.main(opts, plugins=[ShakedownPlugin(config)])
