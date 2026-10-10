"""Tests for skill metadata and progressive-reference validation."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.lint_skills import lint_skill_directory


class SkillLintTests(unittest.TestCase):
    def test_all_canonical_skills_pass(self):
        self.assertEqual(lint_skill_directory(ROOT / "suites"), [])

    def test_missing_metadata_and_references_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            suite = Path(directory) / "example-suite"
            suite.mkdir()
            (suite / "SKILL.md").write_text(
                "---\nname: example-suite\ndescription: Example skill\n---\n"
                "## Workflow\nSee [missing](references/not-there.md).\n",
                encoding="utf-8",
            )
            errors = lint_skill_directory(Path(directory))
            self.assertTrue(any("missing fields" in error for error in errors), errors)
            self.assertTrue(any("missing reference" in error for error in errors), errors)

    def test_reference_cannot_escape_suite_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            suite = Path(directory) / "example-suite"
            suite.mkdir()
            (suite / "SKILL.md").write_text(
                "---\nname: example-suite\ndescription: Example skill\n"
                "use_when: yes\navoid_when: yes\nentry_inputs: yes\n"
                "workflow: yes\nverification: yes\nexit_output: yes\n---\n"
                "## Workflow\nSee [outside](../../secret.md).\n",
                encoding="utf-8",
            )
            errors = lint_skill_directory(Path(directory))
            self.assertTrue(any("escapes suite directory" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
