import unittest
import time
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import big_o

class TestBigO(unittest.TestCase):
    def test_measure_execution_time(self):
        def f(n):
            time.sleep(0.01 * n)
            return n
        ns, t =  big_o.measure_execution_time(f, big_o.n_generator,
                                              min_n=1, max_n=10, n_measures=10,
                                              n_repeats=1)
        assert_array_equal(ns, np.arange(1, 11))
        assert_array_almost_equal(t*100., np.arange(1, 11), 1)

if __name__=='__main__':
    unittest.main()