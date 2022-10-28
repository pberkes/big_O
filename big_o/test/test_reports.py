import unittest
import big_o
from big_o import reports

class TestReport(unittest.TestCase):

    def test_report_return(self):
        best, others = big_o.big_o(sorted, lambda n: big_o.datagen.integers(n, 100, 500))

        assert isinstance(reports.big_o_report(best, others), str)

