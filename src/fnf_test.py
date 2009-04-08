"""Unit test for fnf_main.py"""

import fnf_main
import unittest

class TestFacts(unittest.TestCase):
    def test_get_facts(self):
        fact = fnf_main.Facts()
        result = fact.get_facts()
        self.assertEqual('haha',result)