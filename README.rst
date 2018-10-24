=====
big_O
=====

big_O is a Python module to estimate the time complexity of Python code from
its execution time.  It can be used to analyze how functions scale with inputs
of increasing size.


big_O executes a Python function for input of increasing size `N`, and measures
its execution time. From the measurements, big_O fits a set of time complexity
classes and returns the best fitting class. This is an empirical way to
compute the asymptotic class of a function in `"Big-O"
<http://en.wikipedia.org/wiki/Big_oh>`_.  notation. (Strictly
speaking, we're empirically computing the Big Theta class.)

Usage
-----

For concreteness, let's say we would like to compute the asymptotic behavior
of a simple function that finds the maximum element in a list of positive
integers:

    >>> def find_max(x):
    ...     """Find the maximum element in a list of positive integers."""
    ...     max_ = 0
    ...     for el in x:
    ...         if el > max_:
    ...             max_ = el
    ...     return max_
    ...

To do this, we call `big_o.big_o` passing as argument the function and a
data generator that provides lists of random integers of length N:

    >>> import big_o
    >>> positive_int_generator = lambda n: big_o.datagen.integers(n, 0, 10000)
    >>> best, others = big_o.big_o(find_max, positive_int_generator, n_repeats=100)
    >>> print(best)
    Linear: time = -0.0021 + 4E-06*n

`big_o` inferred that the asymptotic behavior of the `find_max` function is
linear, and returns an object containing the fitted coefficients for the
complexity class. The second return argument, `others`, contains a dictionary
of all fitted classes with the residuals from the fit as keys:

    >>> for class_, residuals in others.items():
    ...     print('{:<60s}    (res: {:.2G})'.format(class_, residuals))
    ...
    Logarithmic: time = -0.3 + 0.05*log(n)                      (res: 0.072)
    Cubic: time = 0.1 + 3.6E-16*n^3                             (res: 0.028)
    Quadratic: time = 0.068 + 3.8E-11*n^2                       (res: 0.011)
    Constant: time = 0.2                                        (res: 0.17)
    Exponential: time = -4.2 * 4.1E-05^n                        (res: 9.6)
    Linearithmic: time = 0.0077 + 3.5E-07*n*log(n)              (res: 0.00055)
    Polynomial: time = -11 * x^0.84                             (res: 0.12)
    Linear: time = -0.0021 + 4E-06*n                            (res: 0.00054)

Submodules
----------

- `big_o.datagen`: this sub-module contains common data generators, including an identity generator that simply returns N (`datagen.n_`), and a data generator that returns a list of random integers of length N (`datagen.integers`).
- `big_o.complexities`: this sub-module defines the complexity classes to be fit to the execution times. Unless you want to define new classes, you don't need to worry about it.


Standard library examples
-------------------------

Sorting a list in Python is O(n*log(n)) (a.k.a. 'linearithmic'):

    >>> big_o.big_o(sorted, lambda n: big_o.datagen.integers(n, -100, 100))
    (<big_o.complexities.Linearithmic object at 0x031DA9D0>, ...)

Inserting elements at the beginning of a list is O(n):

    >>> def insert_0(lst):
    ...     lst.insert(0, 0)
    ...
    >>> print big_o.big_o(insert_0, big_o.datagen.range_n, n_repeats=100)[0]
    Linear: time = 0.00035 + 7.5E-08*n

Inserting elements at the beginning of a queue is O(1):

    >>> from collections import deque
    >>> def insert_0_queue(queue):
    ...     queue.insert(0, 0)
    ...
    >>> def queue_generator(n):
    ...      return deque(xrange(n))
    ...
    >>> print big_o.big_o(insert_0_queue, queue_generator, n_repeats=100)[0]
    Constant: time = 0.00012

`numpy` examples
----------------

Creating an array:

- `numpy.zeros` is O(n), since it needs to initialize every element to 0:

    >>> import numpy as np
    >>> big_o.big_o(np.zeros, big_o.datagen.n_, max_n=100000, n_repeats=100)
    (<class 'big_o.big_o.Linear'>, ...)

- `numpy.empty` instead just allocates the memory, and is thus O(1):

    >>> big_o.big_o(np.empty, big_o.datagen.n_, max_n=100000, n_repeats=100)
    (<class 'big_o.big_o.Constant'> ...)

Additional examples
--------------

We can compare the estimated time complexities of different Fibonacci number implementations. The naive implementation is exponential O(2^n). Since this implementation is very inefficient we'll reduce the maximum tested n:

    >>> def fib_naive(n):
    ...     if n < 0:
    ...         return -1
    ...     if n < 2:
    ...         return n
    ...     return fib_naive(n-1) + fib_naive(n-2)
    ...
    >>> print(big_o.big_o(fib_naive, big_o.datagen.n_, n_repeats=20, min_n=2, max_n=25)[0])
    Exponential: time = -11 * 0.45^n

A more efficient implementation to find Fibonacci numbers involves using dynamic programming and is linear O(n):

    >>> def fib_dp(n):
    ...     if n < 0:
    ...         return -1
    ...     if n < 2:
    ...         return n
    ...     a = 0
    ...     b = 1
    ...     for i in range(2, n+1):
    ...         a, b = b, a+b
    ...     return b
    ...
    >>> print(big_o.big_o(fib2, big_o.datagen.n_, n_repeats=100, min_n=2, max_n=1000)[0])
    Linear: time = 0.00012 + 1E-05*n


License
-------

big_O is released under the GPL v3. See LICENSE.txt .

Copyright (c) 2011, Pietro Berkes. All rights reserved.
