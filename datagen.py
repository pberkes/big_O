"""Data generators for big_O module."""

import random

def n_(n):
    """Return N."""
    return n

def range_n(n, start=0):
    """Return the sequence [start, start+1, ..., N+start]."""
    return range(start, start+n)

def integers(n, min_, max_):
    """Return Sequence of n integers between min_ and max_.
    Includes extremes."""
    return [random.randint(min_, max_) for _ in range(n)]

def large_integers(n):
    """Sequence of n large integers."""
    return [random.randint(-50, 50) * 1000000 + random.randint(0,10000)
            for _ in range(n)]
