#  Copyright 2008-2012 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
import random
import math
from robot.conf.settings import RobotSettings
from robot.result import ExecutionResult
from robot.running.model import TestSuite


class Yabot(object):

    def __init__(self,
                 random_tests=True,
                 fraction_of_tests_to_run=0.1,
                 rerun_failed_from=None,
                 source=None,
                 runner=None,
                 arguments=None):
        self._random_tests = random_tests
        self._fraction_of_tests_to_run = fraction_of_tests_to_run
        self._rerun_failed_from = rerun_failed_from
        self._source = source
        self._runner = runner
        self._arguments = arguments or []

    def execute(self):
        self._write_argument_file(self._select_tests_to_run())
        self._execute_runner_script()

    def _execute_runner_script(self):
        print self._runner, '--argumentfile yabot_args.txt', self._arguments

    def _write_argument_file(self, tests):
        with open('yabot_args.txt', 'w') as out:
            for t in tests:
                out.write('--test %s\n' % t.longname)

    def _select_tests_to_run(self):
        tests_to_run = []
        if self._rerun_failed_from:
            tests_to_run += self.get_failed_tests(
                ExecutionResult(self._rerun_failed_from))
        all_tests_from_source = self._get_available_tests()
        number_of_tests_to_execute = math.ceil(
            len(all_tests_from_source) * self._fraction_of_tests_to_run)
        tests_to_add = number_of_tests_to_execute - len(tests_to_run)
        if  tests_to_add > 0:
            tests_to_run += self.random_tests(
                [t for t in all_tests_from_source if t not in tests_to_run],
                 tests_to_add)
        return tests_to_run

    def random_tests(self, tests, number_of):
        return sorted(random.sample(tests, number_of))

    random_suites = random_tests

    def get_failed_tests(self, execution_result):
        return [t for t in self._get_tests(execution_result.suite) if not t.passed]

    def get_failed_suites(self, execution_result):
        return [s for s in self._get_test_suites(execution_result.suite) if s.status == 'FAIL']

    def _get_tests(self, suite):
        for s in suite.suites:
            for t in self._get_tests(s):
                yield t
        for t in suite.tests:
            yield t

    def _get_test_suites(self, suite):
        for s in suite.suites:
            for test_suite in self._get_test_suites(s):
                yield test_suite
        if suite.tests:
            yield suite

    def _get_available_tests(self):
        return list(self._get_tests(self._suite()))

    def _get_available_test_suites(self):
        return list(self._get_test_suites(self._suite()))

    def _suite(self):
        settings = RobotSettings(self._arguments)
        return TestSuite([os.path.abspath(self._source)], settings)
