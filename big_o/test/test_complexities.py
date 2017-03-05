import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal

from big_o import complexities


class TestComplexities(unittest.TestCase):

    def test_compute(self):
        x = np.linspace(10, 100, 100)
        y = 3.0 * x + 2.0
        linear = complexities.Linear()
        linear.fit(x, y)
        assert_array_almost_equal(linear.compute(x), y, 10)

    def test_not_fitted(self):
        linear = complexities.Linear()
        self.assertRaises(complexities.NotFittedError, linear.compute, 100)
