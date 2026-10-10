"""Reproducible baseline checks for the canonical skill inventory."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUITES = ROOT / "suites"
EXPECTED = {
    "systematic-debugging-suite",
    "unit-testing-suite",
    "code-review-standards-suite",
    "git-workflow-suite",
    "web-scraping-suite",
    "browser-automation-suite",
    "docker-containers-suite",
    "kubernetes-k8s-suite",
    "terraform-iac-suite",
    "office-documents-suite",
    "ui-design-systems-suite",
    "ux-accessibility-suite",
    "figma-design-prototyping-suite",
    "mobile-native-ui-suite",
    "creative-3d-motion-suite",
    "frontend-webapp-design-suite",
    "landing-page-cro-suite",
    "ai-generative-ui-suite",
}


class SuiteBaselineTests(unittest.TestCase):
    def test_canonical_inventory_and_skill_files(self):
        skill_files = sorted(SUITES.glob("*/SKILL.md"))
        self.assertEqual({path.parent.name for path in skill_files}, EXPECTED)
        self.assertEqual(len(skill_files), 18)

    def test_frontmatter_names_match_unique_folder_names(self):
        names = []
        for path in sorted(SUITES.glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            match = re.match(r"\A---\s*\n(.*?)\n---(?:\s|\Z)", text, re.DOTALL)
            self.assertIsNotNone(match, f"Missing YAML frontmatter: {path}")
            name = re.search(r"(?m)^name:\s*([A-Za-z0-9_-]+)\s*$", match.group(1))
            self.assertIsNotNone(name, f"Missing simple name field: {path}")
            self.assertEqual(name.group(1), path.parent.name)
            names.append(name.group(1))
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
