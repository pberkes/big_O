"""Data generators for big_O module."""

# Author: Pietro Berkes < pietro _DOT_ berkes _AT_ googlemail _DOT_ com >
# Copyright (c) 2011 Pietro Berkes
# License: GPL v3

import random
import string

def n_(n):
    """Return N."""
    return n

def range_n(n, start=0):
    """Return the sequence [start, start+1, ..., start+N-1]."""
    return range(start, start+n)

def integers(n, min_, max_):
    """Return sequence of N random integers between min_ and max_ (included).
    """
    return [random.randint(min_, max_) for _ in range(n)]

def large_integers(n):
    """Return sequence of N large random integers."""
    return [random.randint(-50, 50) * 1000000 + random.randint(0,10000)
            for _ in range(n)]

def strings(n, chars=string.letters):
    """Return random string of N characters, sampled at random from `chars`."""
    return ''.join([random.choice(chars) for i in xrange(n)])
