"""Regression coverage for the workflow evidence-gate fixture."""

import unittest

from examples.bugfix_fixture import is_allowed_status


class StatusValidationRegressionTests(unittest.TestCase):
    def test_accepts_supported_statuses(self):
        self.assertTrue(is_allowed_status("active"))
        self.assertTrue(is_allowed_status("inactive"))

    def test_rejects_unknown_statuses(self):
        self.assertFalse(is_allowed_status("disabled"))
        self.assertFalse(is_allowed_status(""))


if __name__ == "__main__":
    unittest.main()
