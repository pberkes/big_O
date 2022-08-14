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
            residuals = complexity.fit(x, y)

            ref_y = complexity.compute(x)
            assert_allclose(y, ref_y,
                err_msg = "compute() failed to match expected values for class %r" % class_)

            # Check residuals are correct
            # Use the atol constant from np.allclose() because the default for
            # np.testing.assert_allclose() for atol (0) is too low for this comparison
            assert_allclose(residuals, np.sum((y - ref_y) ** 2), rtol=1e-07, atol=1e-08,
                err_msg = "compute() residuals failed to match expected values for class %r" % class_)

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

    def test_fit_list_input(self):
        # Check a normal list / iterable can be passed to fit()
        ns = range(10, 100, 10)
        time = [x**2 for x in ns]

        quadratic = complexities.Quadratic()
        quadratic.fit(ns, time)

        coeff = quadratic.coeff
        coefficients = quadratic.coefficients()

        ns_np = np.array(ns)
        time_np = np.array(time)

        quadratic_check = complexities.Quadratic()
        quadratic_check.fit(ns_np, time_np)

        coeff_check = quadratic_check.coeff
        coefficients_check = quadratic_check.coefficients()

        assert_allclose(coeff, coeff_check,
            err_msg = "coeff of {} did not match coeff of check complexity {}".format(
                quadratic, quadratic_check))
        assert_allclose(coefficients, coefficients_check,
            err_msg = "coefficients of {} did not match coefficients of check complexity {}".format(
                quadratic, quadratic_check))
