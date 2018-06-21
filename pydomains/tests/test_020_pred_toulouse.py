#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for pred_toulouse.py

"""

import os
import shutil
import unittest
import pandas as pd
from pydomains import pred_toulouse
from . import capture


class TestPredToulouse(unittest.TestCase):

    def setUp(self):
        domains = [{'label': 'test1', 'url': 'http://www.google.com'},
                 {'label': 'test2', 'url': 'http://www.sanook.com'}]
        self.df = pd.DataFrame(domains)

    def tearDown(self):
        pass

    def test_pred_toulouse_2017(self):
        odf = pred_toulouse(self.df, 'url')
        self.assertIn('pred_toulouse_2017_lab', odf.columns)


if __name__ == '__main__':
    unittest.main()
