#  Copyright 2012 Mikko Korpela
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

from robot.conf import RobotSettings
from robot.running import TestSuite
from robot.result import ExecutionResult

def get_available_tests(source):
    settings = RobotSettings()
    suite = TestSuite([os.path.abspath(source)], settings)
    return list(get_tests(suite))

def get_available_test_suites(source):
    settings = RobotSettings()
    suite = TestSuite([os.path.abspath(source)], settings)
    return list(get_test_suites(suite))

def get_tests(suite):
    for s in suite.suites:
        for t in get_tests(s):
            yield t
    for t in suite.tests:
        yield t

def get_test_suites(suite):
    for s in suite.suites:
        for test_suite in get_test_suites(s):
            yield test_suite
    if suite.tests:
        yield suite

def get_failing_tests_from_output_xml(output_xml):
    results = ExecutionResult(output_xml)
    return [t for t in get_tests(results.suite) if not t.passed]

def get_failing_test_suites_from_output_xml(output_xml):
    results = ExecutionResult(output_xml)
    return [s for s in get_test_suites(results.suite) if s.status == 'FAIL']

if __name__ == '__main__':
    test_suites =  get_available_test_suites(os.path.join(os.path.dirname(__file__), '..', '..', 'robot','atest', 'robot'))
    with open('suites.txt', 'w') as out:
        for s in sorted(random.sample(test_suites, len(test_suites)/10)):
            out.write('--suite %s\n' % s.longname)
    ##tests = get_available_tests(os.path.join(os.path.dirname(__file__), '..', '..', 'robot','atest', 'robot'))
    ##with open('tests.txt', 'w') as out:
    ##    for t in sorted(random.sample(tests, len(tests)/10)):
    ##        out.write('--test %s\n' % t.longname)
    for item in get_failing_test_suites_from_output_xml(os.path.join(os.path.dirname(__file__), '..', 'testdata', 'output.xml')):
        print item.longname
