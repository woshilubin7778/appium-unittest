import unittest

from library.core.TestCase import TestCase


@unittest.skip
class WorkbenchTest(TestCase):
    """Workbench 模块"""

    def default_setUp(self):
        pass

    def default_tearDown(self):
        pass

    def test_something(self):
        """description"""
        self.assertEqual(True, False)

    def setUp_test_something(self):
        print("Run test case setup.")