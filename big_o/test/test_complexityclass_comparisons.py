import unittest
import numpy as np

from big_o.complexities import ComplexityClass


class FirstComplexityClass(ComplexityClass):
    order = 1


class SecondComplexityClass(ComplexityClass):
    order = 2


FirstComplexity = FirstComplexityClass()
SecondComplexity = SecondComplexityClass()


class TestComplexities(unittest.TestCase):

    def test_ge(self):
        self.assertEqual(FirstComplexity >= SecondComplexity, False)
        self.assertEqual(FirstComplexity >= FirstComplexity, True)
        self.assertEqual(SecondComplexity >= FirstComplexity, True)

    def test_le(self):
        self.assertEqual(FirstComplexity <= SecondComplexity, True)
        self.assertEqual(FirstComplexity <= FirstComplexity, True)
        self.assertEqual(SecondComplexity <= FirstComplexity, False)

    def test_l(self):
        self.assertEqual(FirstComplexity < SecondComplexity, True)
        self.assertEqual(FirstComplexity < FirstComplexity, False)
        self.assertEqual(SecondComplexity < FirstComplexity, False)

    def test_g(self):
        self.assertEqual(FirstComplexity > SecondComplexity, False)
        self.assertEqual(FirstComplexity > FirstComplexity, False)
        self.assertEqual(SecondComplexity > FirstComplexity, True)

    def test_eq(self):
        self.assertEqual(FirstComplexity == SecondComplexity, False)
        self.assertEqual(FirstComplexity == FirstComplexity, True)
