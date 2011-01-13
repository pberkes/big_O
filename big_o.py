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

# -------- define all big-O classes considered in the fitting functions
class Constant(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.ones((len(ns), 1))
        return x, time
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f' % coeff[0]

class Linear(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.vstack([np.ones(len(ns)), ns]).T
        return x, time
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f + %.3f*n' % (coeff[0], coeff[1])

class Quadratic(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.vstack([np.ones(len(ns)), ns*ns]).T
        return x, time
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f + %.3f*n^2' % (coeff[0], coeff[1])

class Logarithmic(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.vstack([np.ones(len(ns)), np.log(ns)]).T
        return x, time
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f + %.3f*log(n)' % (coeff[0], coeff[1])

class Linearithmic(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.vstack([np.ones(len(ns)), ns*np.log(ns)]).T
        return x, time
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f + %.3f*n*log(n)' % (coeff[0], coeff[1])

class Polynomial(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.vstack([np.ones(len(ns)), np.log(ns)]).T
        y = np.log(time)
        return x, y
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f * x^%.3f' % (np.exp(coeff[0]), coeff[1])

class Exponential(object):
    @staticmethod
    def get_xy(ns, time):
        x = np.vstack([np.ones(len(ns)), ns]).T
        y = np.log(time)
        return x, y
    @staticmethod
    def pprint(coeff):
        return 'y = %.3f * %.3f^x' % (np.exp(coeff[0]), np.exp(coeff[1]))

ALL_CLASSES = [Constant, Linear, Quadratic, Polynomial,
               Logarithmic, Linearithmic, Exponential]

def infer_big_o_class(ns, time, classes=ALL_CLASSES, verbose=False):
    """Return the complexity class of func.
    """

    best_class = None
    best_coeff = None
    best_residuals = np.inf
    for class_ in classes:
        x, y = class_.get_xy(ns, time)
        coeff, residuals, rank, s = np.linalg.lstsq(x, y)
        # NOTE: subtract 1e-6 for tiny preference for simpler methods
        if residuals < best_residuals - 1e-6:  
            best_residuals = residuals
            best_coeff = coeff
            best_class = class_
        if verbose:
            print '%s: %s (r=%f)' % (class_.__name__,
                                       class_.pprint(coeff),
                                       residuals)
    return best_class, best_coeff

