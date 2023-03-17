import unittest
import time
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import big_o
from big_o import datagen
from big_o import complexities as compl


def dummy_constant_function(n):
    # Dummy operation with constant complexity.
    x = 0
    for i in range(100):
        x += 1
    return n


def dummy_linear_function(n):
    # Dummy operation with linear complexity.

    # Constant component of linear function
    dummy_constant_function(n)

    x = 0
    for i in range(n):
        for j in range(20):
            x += 1
    return x // 20


def dummy_quadratic_function(n):
    # Dummy operation with quadratic complexity.

    # Constant component of quadratic function
    dummy_constant_function(n)

    x = 0
    for i in range(n):
        for j in range(n):
            for k in range(20):
                x += 1
    return x // 20


def dummy_linearithmic_function(n):
    # Dummy operation with linearithmic complexity.

    # Constant component of linearithmic function
    dummy_constant_function(n)

    x = 0
    log_n = int(np.log(n))
    for i in range(n):
        for j in range(log_n):
            for k in range(20):
                x += 1
    return x // 20


class TestBigO(unittest.TestCase):

    def test_measure_execution_time(self):
        def f(n):
            time.sleep(0.1 * n)
            return n
        ns, t = big_o.measure_execution_time(
            f, datagen.n_,
            min_n=1, max_n=5, n_measures=5, n_repeats=1, n_timings=5
        )
        assert_array_equal(ns, np.arange(1, 6))
        assert_array_almost_equal(t*10., np.arange(1, 6), 1)

    def test_infer_big_o(self):
        x = np.linspace(10, 100, 100)

        desired = [
            (lambda x: x*0.+2., compl.Constant, [2.]),
            (lambda x: 4.*x, compl.Linear, [0., 4.]),
            (lambda x: 3.*x**2., compl.Quadratic, [0., 3.]),
            (lambda x: 2.5*x**3 + 2., compl.Cubic, [2., 2.5]),
            (lambda x: 2.*x**4., compl.Polynomial, [np.log(2.), 4.]),
            (lambda x: 1.5*np.log(x), compl.Logarithmic, [0., 1.5]),
            (lambda x: x*np.log(x), compl.Linearithmic, [0., 1.]),
            (lambda x: 0.6**x, compl.Exponential, [0., np.log(0.6)]),
        ]

        for f, class_, coeff in desired:
            y = f(x)
            res_class, fitted = big_o.infer_big_o_class(x, y)
            self.assertEqual(class_, res_class.__class__)
            assert_array_almost_equal(coeff, res_class.coeff, 2)

    def test_infer_big_o_list_input(self):
        # Check a normal list / iterable can be passed to infer_big_o_class()
        ns = range(10, 100, 10)
        time = [x**2 for x in ns]

        best, fitted = big_o.infer_big_o_class(ns, time)

        ns_np = np.array(ns)
        time_np = np.array(time)

        best_check, fitted_check = big_o.infer_big_o_class(ns_np, time_np)

        self.assertEqual(best.order, best_check.order,
            msg = "Order of complexity {} did not match check complexity {}".format(
                best, best_check))
        self.assertAlmostEqual(fitted[best], fitted_check[best_check])

    def test_big_o(self):
        # Numpy sorts are fast enough that they are very close to linear
        # In testing, heapsort was found to follow the best clear n * log(n) curve
        random_state = np.random.RandomState()
        random_array = random_state.rand(100000)

        # Each test case is a tuple
        # (function_to_evaluate, expected_complexity_class, range_for_n)
        desired = [
            (dummy_constant_function, compl.Constant, (1000, 10000)),
            (dummy_linear_function, compl.Linear, (100, 5000)),
            (dummy_quadratic_function, compl.Quadratic, (1, 100)),
            (dummy_linearithmic_function, compl.Linearithmic, (10, 5000)),
        ]
        for func, class_, n_range in desired:
            res_class, fitted = big_o.big_o(
                func, datagen.n_,
                min_n=n_range[0],
                max_n=n_range[1],
                n_measures=25,
                n_repeats=1,
                n_timings=10,
                return_raw_data = True)

            residuals = fitted[res_class]

            if residuals > 5e-4:
                if isinstance(res_class, class_):
                    err_msg = "(but test would have passed)"
                else:
                    err_msg = "(and test would have failed)"

                # Residual value is too high
                # This is likely caused by the CPU being too noisy with other processes
                # that is preventing clean timing results.
                self.fail(
                    "Complexity fit residuals ({:f}) is too high to be reliable {}"
                    .format(residuals, err_msg))

            sol_class, sol_residuals = next(
                (complexity, residuals) for complexity, residuals in fitted.items()
                if isinstance(complexity, class_))

            self.assertIsInstance(res_class, class_,
                msg = "Best matched complexity is {} (r={:f}) when {} (r={:f}) was expected"
                    .format(res_class, residuals, sol_class, sol_residuals))

    def test_big_o_return_raw_data_default(self):
        _, fitted = big_o.big_o(
            dummy_linear_function,
            datagen.n_,
            min_n=10,
            max_n=1000)

        for _, v in fitted.items():
            self.assertIsInstance(v, np.float64)

    def test_big_o_return_raw_data_false(self):
        _, fitted = big_o.big_o(
            dummy_linear_function,
            datagen.n_,
            min_n=10,
            max_n=1000,
            return_raw_data=False)

        for _, v in fitted.items():
            self.assertIsInstance(v, np.float64)

    def test_big_o_return_raw_data_true(self):
        def dummy(n):
            time.sleep(0.001)

        n_measures = 10
        n_repeats = 5
        n_timings = 3

        _, fitted = big_o.big_o(
            dummy,
            datagen.n_,
            min_n=100,
            max_n=1000,
            n_measures=n_measures,
            n_repeats=n_repeats,
            n_timings=n_timings,
            return_raw_data=True)

        for k, v in fitted.items():
            if isinstance(k, compl.ComplexityClass):
                self.assertIsInstance(v, np.float64)

        self.assertIn('measures', fitted)
        measures = fitted['measures']
        self.assertEqual(len(measures), n_measures)
        for i in range(1, n_measures):
            self.assertGreater(measures[i], measures[i-1])

        self.assertIn('times', fitted)
        times = fitted['times']
        self.assertEqual(len(times), n_measures)
        for t in times:
            self.assertGreaterEqual(t, 0.001 * n_repeats)
