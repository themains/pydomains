#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for shalla_cat.py

"""

import os
import shutil
import unittest
import pandas as pd
from pydomains import shalla_cat
from . import capture


class TestShallCat(unittest.TestCase):

    def setUp(self):
        domains = [{'label': 'test1', 'url': 'http://www.google.com'},
                 {'label': 'test2', 'url': 'http://www.sanook.com'}]
        self.df = pd.DataFrame(domains)

    def tearDown(self):
        pass

    def test_shalla_cat_2017(self):
        odf = shalla_cat(self.df, 'url')
        self.assertIn('shalla_2017_cat', odf.columns)


if __name__ == '__main__':
    unittest.main()
