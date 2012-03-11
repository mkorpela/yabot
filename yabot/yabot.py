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
import random


class Yabot(object):

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
