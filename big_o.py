import numpy as np
from timeit import Timer

_TIMER_SETUP = """
from __main__ import func
x = data_generator(%d)
"""

n_generator = lambda n: n
range_n_generator = lambda n: range(n)

def measure_execution_time(func, data_generator,
                           min_n=1, max_n=100000, n_measures=10,
                           n_repeats=1):
    """Measure the execution time of a function for increasing N.
    
    Input:
    func -- function of which the execution time is measured
            the function is called as func(data), where data is returned
            by data_generator
    data_generator -- function that returns input data for different Ns
                      each input data fpor func is created as data_generator(N)
    min_n, max_n, n_measures -- the execution time of func is measured
                                at n_measures points between min_n and max_n
                                (included)
    n_repeats -- number of times func is called to compute execution time
                 (return the cumulative time of execution)
    
    Returns
    ns -- list of Ns used as input to data_generator
    time -- list of execution time for each N
    """

    class func_wrapper(object):
        def __init__(self, n):
            self.data = data_generator(n)
        def __call__(self):
            return func(self.data)

    ns = np.linspace(min_n, max_n, n_measures).astype('int64')
    time = np.empty(n_measures)
    for i, n in enumerate(ns):
        timer = Timer(func_wrapper(n))
        time[i] = timer.timeit(n_repeats)
    return ns, time

