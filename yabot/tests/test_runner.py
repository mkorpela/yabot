import random
import unittest
from yabot.yabot import Yabot


def _test(passed=True):
    t = lambda:0
    t.passed = passed
    return t

def _suite(failed_tests=None, failed_suites=None):
    s = lambda:0
    s.suites = []
    s.tests = []
    if failed_suites:
        s.suites = [_suite(failed_tests=1) for _ in xrange(failed_suites)]
    if failed_tests:
        s.tests = [_test(passed=False )for _ in xrange(failed_tests)]
        s.status = 'FAIL'
    else:
        s.status = 'PASS'
    return s

def _execution_result(failed_tests=None, failed_suites=None):
    result = lambda:0
    result.suite = _suite(failed_tests=failed_tests, failed_suites=failed_suites)
    return result

class RunnerTestCase(unittest.TestCase):

    def test_random_tests(self):
        tests = Yabot().random_tests([_test(i) for i in xrange(200)], 10)
        self.assertEqual(10, len(tests))

    def test_random_test_suites(self):
        suites = Yabot().random_suites([_suite(i) for i in xrange(400)], 21)
        self.assertEqual(21, len(suites))

    def test_rerun_failed_tests(self):
        tests = Yabot().get_failed_tests(_execution_result(failed_tests=215))
        self.assertEqual(215, len(tests))

    def test_rerun_failed_suites_when_random_suites(self):
        suites = Yabot().get_failed_suites(_execution_result(failed_suites=4))
        self.assertEqual(4, len(suites))

    def test_all_failed_are_executed_even_if_there_are_more_of_them_then_the_required_fraction(self):
        pass

    def test_fraction_settings(self):
        pass

if __name__ == '__main__':
    unittest.main()
