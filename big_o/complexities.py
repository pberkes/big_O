"""Definition of complexity classes."""

import numpy as np


class NotFittedError(Exception):
    pass


class ComplexityClass(object):
    """ Abstract class that fits complexity classes to timing data.
    """

    def __init__(self):
        # list of parameters of the fitted function class as returned by the
        # last square method np.linalg.lstsq
        self.coeff = None

    def fit(self, n, t):
        """ Fit complexity class parameters to timing data.

        Input:
        ------

        n -- Array of values of N for which execution time has been measured.

        t -- Array of execution times for each N in seconds.

        Output:
        -------

        residuals -- Sum of square errors of fit
        """
        x = self._transform_n(n)
        y = self._transform_time(t)
        coeff, residuals, rank, s = np.linalg.lstsq(x, y, rcond=-1)
        self.coeff = coeff
        return residuals[0]

    def compute(self, n):
        """ Compute the value of the fitted function at `n`. """
        if self.coeff is None:
            raise NotFittedError()

        # Result is linear combination of the terms with the fitted
        # coefficients
        x = self._transform_n(n)
        tot = 0
        for i in range(len(self.coeff)):
            tot += self.coeff[i] * x[:, i]
        return tot

    def __str__(self):
        prefix = '{}: '.format(self.__class__.__name__)

        if self.coeff is None:
            return prefix + ': not yet fitted'
        return prefix + self.format_str().format(*tuple(self.coeff)) + ' (sec)'

    # --- abstract methods

    @classmethod
    def format_str(cls):
        """ Return a string describing the fitted function.

        The string must contain one formatting argument for each coefficient.
        """
        return 'FORMAT STRING NOT DEFINED'

    def _transform_n(self, n):
        """ Terms of the linear combination defining the complexity class.

        Output format: number of Ns x number of coefficients .
        """
        raise NotImplementedError()

    def _transform_time(self, t):
        """ Transform time as needed for fitting.
        (e.g., t->log(t)) for exponential class.
        """
        return t

    def __gt__(self, other):
        return self.order > other.order

    def __lt__(self, other):
        return self.order < other.order

    def __le__(self, other):
        return (self < other) or self == other

    def __ge__(self, other):
        return (self > other) or self == other

    def __eq__(self, other):
        return self.order == other.order

    def __hash__(self):
        return id(self)

# --- Concrete implementations of the most popular complexity classes


class Constant(ComplexityClass):
    order = 10

    def _transform_n(self, n):
        return np.ones((len(n), 1))

    @classmethod
    def format_str(cls):
        return 'time = {:.2G}'


class Linear(ComplexityClass):
    order = 30

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} + {:.2G}*n'


class Quadratic(ComplexityClass):
    order = 50

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * n]).T

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} + {:.2G}*n^2'


class Cubic(ComplexityClass):
    order = 60

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n ** 3]).T

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} + {:.2G}*n^3'


class Logarithmic(ComplexityClass):
    order = 20

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} + {:.2G}*log(n)'


class Linearithmic(ComplexityClass):
    order = 40

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * np.log(n)]).T

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} + {:.2G}*n*log(n)'


class Polynomial(ComplexityClass):
    order = 70

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def _transform_time(self, t):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} * x^{:.2G}'


class Exponential(ComplexityClass):
    order = 80

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    def _transform_time(self, t):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return 'time = {:.2G} * {:.2G}^n'


ALL_CLASSES = [Constant, Linear, Quadratic, Cubic, Polynomial,
               Logarithmic, Linearithmic, Exponential]
