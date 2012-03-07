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

from robot.conf import RobotSettings
from robot.running import TestSuite

def get_available_tests(source):
    settings = RobotSettings()
    suite = TestSuite([os.path.abspath(source)], settings)
    return gather_tests(suite)

def gather_tests(suite, tests_so_far=None):
    tests_so_far = tests_so_far or []
    for s in suite.suites:
        tests_so_far = gather_tests(s, tests_so_far)
    return tests_so_far + [t.longname for t in suite.tests]

if __name__ == '__main__':
    s = os.path.abspath('../../robot/atest/testdata')
    print s
    for test in get_available_tests(s):
        print test
