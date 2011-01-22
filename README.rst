=====
big_O
=====

big_O defines tools for estimating the time complexity of Python code from
its execution time.

License
-------

big_O is released under the GPL v3. See LICENSE.txt .

Examples
========

`numpy` examples
----------------

::

	>>> import big_o
	>>> import numpy as np

Creating an array:

- `numpy.zeros` is O(n), since it needs to initialize every element to 0:

	>>> big_o.big_o(np.zeros, big_o.datagen.n_, max_n=1000000, n_repeats=5) # doctest: +ELLIPSIS
	(<class 'big_o.big_o.Linear'>, array([...]))

- `numpy.empty` instead just allocates the memory, and is thus O(1):

	>>> big_o.big_o(np.empty, big_o.datagen.n_, max_n=1000000, n_repeats=5) # doctest: +ELLIPSIS
	(<class 'big_o.big_o.Constant'>, array([...]))
