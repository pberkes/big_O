"""Definition of complexity classes."""

# Author: Pietro Berkes < pietro _DOT_ berkes _AT_ googlemail _DOT_ com >
# Copyright (c) 2011 Pietro Berkes
# License: GPL v3

import numpy as np

# TODO: cubic
# TODO: pretty print utility that prints first significant numbers
# TODO: transform fitted numbers in seconds to have interpretable results

class NotFittedError(Exception):
    pass

class ComplexityClass(object):
    def __init__(self):
        # list of parameters of the fitted function class as returned by the
        # last square method np.linalg.lstsq
        self.coeff = None

    def fit(self, n, t):
        x = self._transform_n(n)
        y = self._transform_time(t)
        coeff, residuals, rank, s = np.linalg.lstsq(x, y)
        self.coeff = coeff
        return residuals

    def compute(self, n):
        """Compute f(n)."""
        if self.coeff is None:
            raise NotFittedError()

        # result is linear combination of the terms with the fitted coefficients
        x = self._transform_n(n)
        tot = 0
        for i in range(len(self.coeff)):
            tot += self.coeff[i] * x[i]
        return tot

    def __str__(self):
        prefix = '%s: ' % self.__class__.__name__

        if self.coeff is None:
            return prefix + ': not yet fitted'
        return prefix + self.format_str() % tuple(self.coeff)

    # --- abstract methods

    @classmethod
    def format_str(cls):
        return 'FORMAT STRING NOT DEFINED'

    def _transform_n(self, n):
        """Terms of f(n).
        
        Output format: number of Ns x number of coefficients .
        """
        raise NotImplementedError()

    def _transform_time(self, t):
        return t

# --- Concrete implementations of the most popular complexity classes

class Constant(ComplexityClass):
    def _transform_n(self, n):
        return np.ones((len(n), 1))

    @classmethod
    def format_str(cls):
        return 'time = %.3f'

class Linear(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    @classmethod
    def format_str(cls):
        return 'time = %.3f + %.3f*n'

class Quadratic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * n]).T

    @classmethod
    def format_str(cls):
        return 'time = %.3f + %.3f*n^2'

class Cubic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n**3]).T

    @classmethod
    def format_str(cls):
        return 'time = %.3f + %.3f*n^3'

class Logarithmic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    @classmethod
    def format_str(cls):
        return 'time = %.3f + %.3f*log(n)'

class Linearithmic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * np.log(n)]).T

    @classmethod
    def format_str(cls):
        return 'time = %.3f + %.3f*n*log(n)'

class Polynomial(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def _transform_time(self, t):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return 'time = %.3f * x^%.3f'

class Exponential(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    def _transform_time(self, t):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return 'time = %.3f * %.3f^n'

ALL_CLASSES = [Constant, Linear, Quadratic, Cubic, Polynomial,
               Logarithmic, Linearithmic, Exponential]
