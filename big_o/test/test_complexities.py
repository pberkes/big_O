import unittest
import numpy as np
from numpy.testing import assert_allclose

from big_o import complexities


class TestComplexities(unittest.TestCase):

    def test_compute(self):
        desired = [
            (lambda x: 2.+x*0., complexities.Constant),
            (lambda x: 5.*x+3., complexities.Linear),
            (lambda x: 8.1*x**2.+0.9, complexities.Quadratic),
            (lambda x: 1.0*x**3+11.0, complexities.Cubic),
            (lambda x: 5.2*x**2.5, complexities.Polynomial),
            (lambda x: 8.5*np.log(x)+99.0, complexities.Logarithmic),
            (lambda x: 1.7*x*np.log(x)+2.74, complexities.Linearithmic),
            (lambda x: 3.14**x, complexities.Exponential)
        ]

        x = np.linspace(10, 100, 100)
        for f, class_ in desired:
            y = f(x)
            complexity = class_()
            complexity.fit(x, y)
            assert_allclose(y, complexity.compute(x), err_msg = "compute() failed to match expected values for class %r" % class_)

    def test_not_fitted(self):
        for class_ in complexities.ALL_CLASSES:
            self.assertRaises(complexities.NotFittedError, class_().compute, 100)

    def test_str_includes_units(self):
        x = np.linspace(10, 100, 100)
        y = 3.0 * x + 2.0
        linear = complexities.Linear()
        linear.fit(x, y)
        linear_str = str(linear)
        assert '(sec)' in linear_str
