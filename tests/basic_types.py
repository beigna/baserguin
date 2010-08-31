
import unittest
import datetime
import sys
import os

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')
from lib.basic_types import Boolean, DateTime, String, Integer

class TestBasicTypes(unittest.TestCase):
    def setUp(self):
        self.boolean_true = ('t', True, 'True', '1', 1)
        self.boolean_false = ('f', False, 'False', '0', 0)
        self.boolean_type_fail = (3, 'algo')
        self.boolean_value_fail = (None, '')

        self.datetime_ok = (datetime.datetime.now(), '2010-08-31 00:42:38')
        self.datetime_type_fail = (datetime.datetime.now().date(), 234)
        self.datetime_value_fail = (None, '', 'bla bla')

        self.integer_int = (1, -34, 66, '59')
        self.integer_long = ('12334546565678567', 123123123123123)
        self.integer_fail = ('hola mundo', '')

    def tearDown(self):
        pass

    def test_boolean(self):
        for e in self.boolean_true:
            a = Boolean(e)
            self.assertEqual(a.data, True)

        for e in self.boolean_false:
            a = Boolean(e)
            self.assertEqual(a.data, False)

        for e in self.boolean_type_fail:
            try:
                a = Boolean(e)
            except TypeError, e:
                self.assertEqual(type(e), TypeError)

        for e in self.boolean_value_fail:
            try:
                a = Boolean(e)
            except ValueError, e:
                self.assertEqual(type(e), ValueError)

    def test_datetime(self):
        for e in self.datetime_ok:
            a = DateTime(e)
            self.assertEqual(type(a.data), datetime.datetime)

        for e in self.datetime_type_fail:
            try:
                a = DateTime(e)
            except TypeError, e:
                self.assertEqual(type(e), TypeError)

        for e in self.datetime_value_fail:
            try:
                a = DateTime(e)
            except ValueError, e:
                self.assertEqual(type(e), ValueError)

    def test_integer(self):
        for e in self.integer_int:
            a = Integer(e)
            self.assertEqual(type(a.data), int)

        for e in self.integer_long:
            a = Integer(e)
            self.assertEqual(type(a.data), long)

        for e in self.integer_fail:
            try:
                a = Integer(e)
            except ValueError, e:
                self.assertEqual(type(e), ValueError)

if __name__ == '__main__':
    unittest.main()
