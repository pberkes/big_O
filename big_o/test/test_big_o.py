import unittest
import time
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import big_o
from big_o import datagen
from big_o import complexities as compl


class TestBigO(unittest.TestCase):

    def test_measure_execution_time(self):
        def f(n):
            time.sleep(0.1 * n)
            return n
        ns, t = big_o.measure_execution_time(
            f, datagen.n_,
            min_n=1, max_n=5, n_measures=5, n_repeats=1,
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

    def test_big_o(self):
        def dummy_linear_function(n):
            for i in range(n):
                # Dummy operation with linear complexity.
                8282828 * 2322

        def dummy_quadratic_function(n):
            for i in range(n):
                for j in range(n):
                    # Dummy operation with quadratic complexity.
                    8282828 * 2322

        # In the best case, TimSort is linear, so we fix a random array to
        # make sure we hit a close-to-worst case scenario, which is
        # O(n*log(n)).
        random_state = np.random.RandomState(89342787)
        random_array = random_state.rand(100000)

        # Each test case is a tuple
        # (function_to_evaluate, expected_complexity_class, range_for_n)
        desired = [
            (dummy_linear_function, compl.Linear, (100, 10000)),
            (lambda n: 1., compl.Constant, (1000, 10000)),
            (dummy_quadratic_function, compl.Quadratic, (50, 500)),
            (lambda n: np.sort(random_array[:n], kind='mergesort'),
             compl.Linearithmic, (100, random_array.shape[0])),
        ]
        for func, class_, n_range in desired:
            res_class, fitted = big_o.big_o(
                func, datagen.n_,
                min_n=n_range[0],
                max_n=n_range[1],
                n_measures=25,
                n_repeats=10,
                n_timings=10,
            )
            self.assertEqual(class_, res_class.__class__)

    def test_big_o_return_raw_data_default(self):
        def dummy_linear_function(n):
            for _ in range(n):
                # Dummy operation with constant complexity.
                8282828 * 2322

        _, fitted = big_o.big_o(
            dummy_linear_function,
            datagen.n_,
            min_n=100,
            max_n=10000,
            n_measures=25,
            n_repeats=10,
            n_timings=10)

        for _, v in fitted.items():
            self.assertIsInstance(v, np.float64)

    def test_big_o_return_raw_data_false(self):
        def dummy_linear_function(n):
            for _ in range(n):
                # Dummy operation with constant complexity.
                8282828 * 2322

        _, fitted = big_o.big_o(
            dummy_linear_function,
            datagen.n_,
            min_n=100,
            max_n=10000,
            n_measures=25,
            n_repeats=10,
            n_timings=10,
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
