# -*- coding: utf-8 -*-
# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import abc
import collections
import imp
import os
#import tempfile
import argparse
import yaml
#import jinja2
from six import iteritems
#from builtins import object

# if 'TEMPDIR' not in os.environ:
#     os.environ['TEMPDIR'] = tempfile.gettempdir()

DEFAULT_CONFIG = {
    'collector': {
        'name': 'filesys',
        'basedir': os.path.join(os.environ['PWD'], 'cases')
    },
    'runner': {
        'name': 'pytest_'
    },
    'reporter': {
        'html': {
            'outputdir': os.path.join(os.environ['PWD'], 'reports')
        }
    }
}

class Config(collections.MutableMapping):
    """Find a key in current or parent node"""

    _session = None

    def __init__(self, data=None):
        """
        """

        self._store = {}

        if data:
            self.update(data)

    @classmethod
    def load(cls, data):
        """
        Load dictionaries into the config.  Each subsequent dict merges into
        the previous one
        """
        session = cls.session()

        return session.update(yaml.load(data))

    @classmethod
    def session(cls):
        """
        Get the existing config session or create a new empty config object
        """
        if not cls._session:
            cls._session = Config()

        return cls._session

    def __setitem__(self, item, value):
        """
        """
        self._store[item] = value

    def __setattr__(self, item, value):
        if item.startswith('_'):
            super(Config, self).__setattr__(item, value)
        else:
            self.__setitem__(item, value)

    def __getattr__(self, item):

        return self.__getitem__(item)

    def __getitem__(self, item):
        """
        """
        value = self._store[item]

        if isinstance(value, collections.Mapping):
            value = Config(value)

        return value

    def __delitem__(self, item):
        del(self._store[item])

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return str(self._store)

    def merge(self, data):
        """
        Deep-merge config
        """
        def _merge(source, destination):
            for key, value in iteritems(source):
                if isinstance(value, dict):
                    # get node or create one
                    node = destination.setdefault(key, {})
                    _merge(value, node)
                else:
                    destination[key] = value

            return destination

        self.update(_merge(yaml.load(data), self._store))

class BaseCollector(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def collect(self, config, filter=[]):
        pass

class BaseRunner(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        pass

class BaseReporter(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def write(self):
        pass

def load_plugin(name, path=[]):
    """Load protocol module from name"""

    # by default search current working directoy and installed directory
    path += [os.path.abspath('./plugins'), os.path.dirname(__file__)]

    f, filename, description = imp.find_module(name, path)
    loaded = imp.load_module('shakedown.{}'.format(name), f, filename,
                             description)

    return loaded

def classify(string):
    split_ = string.split('_')
    caps_ = [ str_.capitalize() for str_ in split_ ]
    return "".join(caps_)

def collect(config, filter):
    """
    """
    name = config['collector'].get('name','testrail')
    module = load_plugin(name)

    # the collect function should return a list of tests to run
    return module.collect(config, filter)

def run(config, tests):
    """
    """
    name = config['runner'].get('name', 'pytest')
    module = load_plugin(name)

    #
    return module.run(config, tests)

def parse_args():
    parser = argparse.ArgumentParser(prog="shakedown")
    arg = parser.add_argument
    arg('filter', nargs='*', help=('filter tests to run. can be ids, globs, '
                                   'or paths... depending on runner plugin'))
    arg('-v', '--version', action='store_true', help="Display version info")
    arg('-f', '--config', help=('specifies path to shakedown '
                                'configuration file'))
    #arg('-d', '--dut-profile', help='specifies path to dut profile')
    arg('-b', '--basedir', help=('the path to the working directory if not '
                                 'specified the current working directory is '
                                 'used'))
    #arg('-o', '--output-dir')
    arg('-m', '--marker', action='append', help=('run tests with specified '
                                                 'markers'))
    arg('-e', '--eval', default={}, help='override config file settings')

    return parser.parse_args()

def main():
    """Main routing. provides entrypoint hook to setuputils"""
    args = parse_args()

    if args.basedir:
        os.chdir(os.path.abspath(args.basedir))

    config = Config.session()

    if args.config:
        with open(args.config, 'r') as fh:
            config.merge(fh.read())

    if args.eval:
        config.merge(args.eval)
    #print(config)
    #invoke the collector...
    tests = collect(config, args.filter)
    #print(tests)
    # run the tests...
    results = run(config, tests)

    print(results)
    #invoke the runner...
    #results = run_runner(config['runner'], tests)

    #invoke the reporter...

if __name__ == '__main__':
    main()
