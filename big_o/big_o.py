# Author: Pietro Berkes < pietro _DOT_ berkes _AT_ googlemail _DOT_ com >
# Copyright (c) 2011 Pietro Berkes
# License: GPL v3

import numpy as np
from timeit import Timer

from .complexities import ALL_CLASSES

_TIMER_SETUP = """
from __main__ import func
x = data_generator(%d)
"""

def measure_execution_time(func, data_generator,
                           min_n=100, max_n=100000, n_measures=10,
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

def infer_big_o_class(ns, time, classes=ALL_CLASSES, verbose=False):
    """Return the complexity class from execution times.
    
    Input:
    ns -- Array of values of N for which execution time has been measured.
    time -- Array of execution times for each N in `ns`.
    classes -- The complexity classes to consider
               Deafault: all the classes in ALL_CLASSES
    verbose -- Print parameters and residuals of the fit for each complexity
               class
    
    Output:
    best_class -- an object representing the complexity class that best fits
                  the measured execution times
    best_coeff -- the fitted parameters
    """

    best_class = None
    best_coeff = None
    best_residuals = np.inf
    for class_ in classes:
        x, y = class_.get_xy(ns, time)
        coeff, residuals, rank, s = np.linalg.lstsq(x, y)
        # NOTE: subtract 1e-6 for tiny preference for simpler methods
        # TODO: improve simplicity detection
        if residuals < best_residuals - 1e-6:  
            best_residuals = residuals
            best_coeff = coeff
            best_class = class_
        if verbose:
            print '%s: %s (r=%f)' % (class_.__name__,
                                       class_.pprint(coeff),
                                       residuals)
    return best_class, best_coeff

def big_o(func, data_generator,
          min_n=100, max_n=100000, n_measures=10,
          n_repeats=1, classes=ALL_CLASSES, verbose=False):
    """Estimate time complexity of a Python function from execution time.

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
    classes -- The complexity classes to consider
               Deafault: all the classes in ALL_CLASSES
    verbose -- Print parameters and residuals of the fit for each complexity
               class
    
    Output:
    best_class -- an object representing the complexity class that best fits
                  the measured execution times
    best_coeff -- the fitted parameters
    """
    ns, time = measure_execution_time(func, data_generator,
                                      min_n, max_n, n_measures, n_repeats)
    return infer_big_o_class(ns, time, classes, verbose=verbose)
