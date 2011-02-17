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
	>>> print best
	Linear: time = -0.0028 + 6.1E-06*n

`big_o` inferred that the asymptotic behavior of the `find_max` fuction is
linear, and returns an object containing the fitted coefficients for the
complexity class. The second return argument, `others`, contains a dictionary
of all fitted classes with the residuals from the fit as keys:

	>>> for class_, residuals in others.items():
	...     print class_, '   (res: %.2G)' % residuals
	...
	Linear: time = 0.0015 + 5.8E-06*n    (res: 8.9E-05)
	Polynomial: time = -12 * x^0.95    (res: 0.0093)
	Logarithmic: time = -0.44 + 0.073*log(n)    (res: 0.14)
	Linearithmic: time = 0.016 + 5E-07*n*log(n)    (res: 0.00064)
	Exponential: time = -4.1 * 4.5E-05^n    (res: 14)
	Constant: time = 0.29    (res: 0.35)
	Cubic: time = 0.15 + 5.1E-16*n^3    (res: 0.062)
	Quadratic: time = 0.1 + 5.4E-11*n^2    (res: 0.026)

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
	...      lst.insert(0, 0)
	...
	>>> print big_o.big_o(insert_0, big_o.datagen.range_n, n_repeats=100)[0]
	Linear: time = 0.00035 + 7.5E-08*n
	
Inserting elements at the beginning of a queue is O(1):

	>>> from collections import deque
	>>> def insert_0_queue(queue):
	...      lst.insert(0, 0)
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
	>>> big_o.big_o(np.zeros, big_o.datagen.n_, max_n=1000000, n_repeats=5) # doctest: +ELLIPSIS
	(<class 'big_o.big_o.Linear'>, ...)

- `numpy.empty` instead just allocates the memory, and is thus O(1):

	>>> big_o.big_o(np.empty, big_o.datagen.n_, max_n=1000000, n_repeats=5) # doctest: +ELLIPSIS
	(<class 'big_o.big_o.Constant'> ...)


License
-------

big_O is released under the GPL v3. See LICENSE.txt .

Copyright (c) 2011, Pietro Berkes. All rights reserved.
