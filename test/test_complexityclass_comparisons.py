import unittest

from big_o.complexities import ComplexityClass


class FirstComplexityClass(ComplexityClass):
    order = 1


class AltFirstComplexityClass(ComplexityClass):
    order = 1


class SecondComplexityClass(ComplexityClass):
    order = 2


class TestComplexities(unittest.TestCase):

    def setUp(self):
        self.first_complexity = FirstComplexityClass()
        self.alt_first_complexity = AltFirstComplexityClass()
        self.second_complexity = SecondComplexityClass()

    def test_ge(self):
        self.assertFalse(self.first_complexity >= self.second_complexity)
        self.assertTrue(self.second_complexity >= self.first_complexity)
        self.assertTrue(self.first_complexity >= self.first_complexity)
        self.assertTrue(self.alt_first_complexity >= self.first_complexity)
        self.assertTrue(self.first_complexity >= self.alt_first_complexity)

    def test_le(self):
        self.assertTrue(self.first_complexity <= self.second_complexity)
        self.assertFalse(self.second_complexity <= self.first_complexity)
        self.assertTrue(self.first_complexity <= self.first_complexity)
        self.assertTrue(self.alt_first_complexity <= self.first_complexity)
        self.assertTrue(self.first_complexity <= self.alt_first_complexity)

    def test_l(self):
        self.assertTrue(self.first_complexity < self.second_complexity)
        self.assertFalse(self.second_complexity < self.first_complexity)
        self.assertFalse(self.first_complexity < self.alt_first_complexity)

    def test_g(self):
        self.assertFalse(self.first_complexity > self.second_complexity)
        self.assertTrue(self.second_complexity > self.first_complexity)
        self.assertFalse(self.first_complexity > self.alt_first_complexity)

    def test_eq(self):
        self.assertFalse(self.first_complexity == self.second_complexity)
        self.assertTrue(self.first_complexity == self.first_complexity)
        self.assertTrue(self.first_complexity == self.alt_first_complexity)
