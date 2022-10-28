import unittest
import big_o
from big_o import reports

class TestReport(unittest.TestCase):

    def test_report_return(self):
        best, others = big_o.big_o(sorted, lambda n: big_o.datagen.integers(n, 100, 500))

        assert isinstance(reports.big_o_report(best, others), str)

    def test_report_return_raw_data_true(self):
        best, others = big_o.big_o(sorted, lambda n: big_o.datagen.integers(n, 100, 500), return_raw_data=True)

        report = reports.big_o_report(best, others)
        assert 'measures' not in report
        assert 'times' not in report

