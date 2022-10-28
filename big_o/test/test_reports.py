import unittest
import big_o
from big_o import reports

def find_max(x):
    """Find the maximum element in a list of positive integers."""
    max_ = 0
    for el in x:
        if el > max_:
            max_ = el
    return max_

class TestReport(unittest.TestCase):

    def test_report_return(self):
        positive_int_generator = lambda n: big_o.datagen.integers(n, 0, 10000)
        best, others = big_o.big_o(find_max, positive_int_generator, n_repeats=100, return_raw_data=True)

        assert type(reports.big_o_report(best, others)) == str

