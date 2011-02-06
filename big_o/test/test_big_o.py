# Author: Pietro Berkes < pietro _DOT_ berkes _AT_ googlemail _DOT_ com >
# Copyright (c) 2011 Pietro Berkes
# License: GPL v3

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
        ns, t =  big_o.measure_execution_time(f, datagen.n_,
                                              min_n=1, max_n=5, n_measures=5,
                                              n_repeats=1)
        assert_array_equal(ns, np.arange(1, 6))
        assert_array_almost_equal(t*10., np.arange(1, 6), 1)

    def test_infer_big_o(self):
        x = np.linspace(10, 100, 100)
        
        desired = [(lambda x: x*0.+2., compl.Constant, [2.]),
                   (lambda x: 4.*x, compl.Linear, [0., 4.]),
                   (lambda x: 3.*x**2., compl.Quadratic, [0., 3.]),
                   (lambda x: 2.5*x**3 + 2., compl.Cubic, [2., 2.5]),
                   (lambda x: 2.*x**4., compl.Polynomial, [np.log(2.), 4.]),
                   (lambda x: 1.5*np.log(x), compl.Logarithmic, [0., 1.5]),
                   (lambda x: x*np.log(x), compl.Linearithmic, [0., 1.]),
                   (lambda x: 0.6**x, compl.Exponential, [0., np.log(0.6)])]
        for f, class_, coeff in desired:
            y = f(x)
            res_class, fitted = big_o.infer_big_o_class(x, y)
            self.assertEqual(class_, res_class.__class__)
            assert_array_almost_equal(coeff, res_class.coeff, 2)

    def test_big_o(self):
        desired = [(lambda n: [i for i in xrange(n*100)], compl.Linear),
                   (lambda n: 1., compl.Constant),
                   (lambda n: [i+j for i in xrange(n) for j in xrange(n)],
                        compl.Quadratic),
                   (lambda n: sorted(np.random.randn(n*100)),
                        compl.Linearithmic)]
        for func, class_ in desired:
            res_class, fitted = big_o.big_o(func, datagen.n_,
                                            min_n=100, max_n=1000, n_repeats=5)
            self.assertEqual(class_, res_class.__class__)

    def test_compute(self):
        x = np.linspace(10, 100, 100)
        y = 3.*x + 2.
        linear = compl.Linear()
        linear.fit(x, y)
        assert_array_almost_equal(linear.compute(x), y, 10)

    def test_not_fitted(self):
        linear = compl.Linear()
        self.assertRaises(compl.NotFittedError, linear.compute, 100)

if __name__=='__main__':
    unittest.main()