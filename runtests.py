#!/usr/bin/env python
import unittest
import sys

from os.path import dirname, abspath

from tests import basic_types, editormm, newser, snoopy_types, scheduler


def runtests():
    parent_path = dirname(abspath(__file__))
    sys.path.insert(0, parent_path)

    loader = unittest.TestLoader()
    suite_list = []
    for module in (basic_types, editormm, newser, snoopy_types, scheduler):
        suite = loader.loadTestsFromModule(module)
        suite_list.append(suite)
        unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    # just to make it extendable
    runtests()
