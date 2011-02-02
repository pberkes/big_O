"""Definition of complexity classes."""

# Author: Pietro Berkes < pietro _DOT_ berkes _AT_ googlemail _DOT_ com >
# Copyright (c) 2011 Pietro Berkes
# License: GPL v3

import numpy as np

# TODO: cubic
# TODO: give these classes more responsibility, define superclass
# XXX: fitting should be a task for these classes
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
