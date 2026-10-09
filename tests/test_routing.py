"""Deterministic profile routing tests including negative and conflict cases."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from routing import RoutingError, load_profile, route_task


class RoutingTests(unittest.TestCase):
    def test_core_routes(self):
        cases = [
            ("Fix a bug causing a crash", "systematic-debugging-suite"),
            ("Write a unit test for the parser", "unit-testing-suite"),
            ("Review this pull request for security", "code-review-standards-suite"),
            ("Prepare pull request and conventional commit", "git-workflow-suite"),
            ("Automate browser flow with Playwright", "browser-automation-suite"),
            ("Crawl public docs site", "web-scraping-suite"),
            ("Extract a PDF table", "office-documents-suite"),
            ("Harden a Docker image", "docker-containers-suite"),
            ("Troubleshoot Kubernetes workload", "kubernetes-k8s-suite"),
            ("Terraform state locking", "terraform-iac-suite"),
        ]
        for task, expected in cases:
            with self.subTest(task=task):
                self.assertEqual(route_task(task).primary, f"aes:skill:{expected}")
                self.assertEqual(route_task(task).tier, "tier1")

    def test_extended_profiles_route_only_the_selected_capability(self):
        cases = [
            ("Build responsive Next.js frontend", "frontend", "frontend-webapp-design-suite"),
            ("Audit WCAG keyboard accessibility", "frontend", "ux-accessibility-suite"),
            ("Define design system tokens", "frontend", "ui-design-systems-suite"),
            ("Map Figma design to code", "frontend", "figma-design-prototyping-suite"),
            ("Build mobile app with React Native", "frontend", "mobile-native-ui-suite"),
            ("Create a Three.js 3D scene", "frontend", "creative-3d-motion-suite"),
            ("Improve landing page conversion", "frontend", "landing-page-cro-suite"),
            ("Generate UI with Stitch", "frontend", "ai-generative-ui-suite"),
        ]
        for task, profile, expected in cases:
            with self.subTest(task=task):
                decision = route_task(task, profile)
                self.assertEqual(decision.primary, f"aes:skill:{expected}")
                self.assertEqual(len(decision.capabilities_to_load()), 1)

    def test_specificity_and_priority_resolve_mixed_intents_without_loading_alternatives(self):
        decision = route_task("Fix bug and add regression test")
        self.assertEqual(decision.primary, "aes:skill:systematic-debugging-suite")
        self.assertIn("aes:skill:unit-testing-suite", decision.alternatives)
        self.assertEqual(decision.capabilities_to_load(), (decision.primary,))

    def test_equally_ranked_conflicting_routes_request_disambiguation(self):
        decision = route_task("Need help with Docker and Terraform", "infrastructure")
        self.assertEqual(decision.tier, "ambiguous")
        self.assertIsNone(decision.primary)
        self.assertEqual(len(decision.alternatives), 2)

    def test_niche_falls_back_to_finder_without_preloading_or_activation(self):
        decision = route_task("Find a specialist bioinformatics pipeline skill")
        self.assertEqual(decision.tier, "tier2")
        self.assertIsNone(decision.primary)
        self.assertEqual(decision.query, "Find a specialist bioinformatics pipeline skill")

    def test_finder_outage_and_minimal_profile_report_missing_route(self):
        self.assertEqual(route_task("Specialized CAD tool", finder_available=False).tier, "unavailable")
        self.assertEqual(route_task("Fix a bug", "minimal").tier, "tier2")

    def test_strict_profile_exposes_gates_without_loading_extra_suites(self):
        decision = route_task("Fix a bug", "strict")
        self.assertEqual(decision.primary, "aes:skill:systematic-debugging-suite")
        self.assertIn("security-review", decision.gates)
        self.assertEqual(len(decision.capabilities_to_load()), 1)

    def test_exact_ids_are_checked_and_route_without_search(self):
        decision = route_task("irrelevant task", skill_id="aes:skill:terraform-iac-suite")
        self.assertEqual(decision.primary, "aes:skill:terraform-iac-suite")
        with self.assertRaisesRegex(RoutingError, "Unknown exact capability ID"):
            route_task("x", skill_id="terraform-iac-suite")

    def test_unknown_profile_fails_clearly(self):
        with self.assertRaises(RoutingError):
            load_profile("does-not-exist")

    def test_empty_task_is_rejected(self):
        with self.assertRaisesRegex(RoutingError, "non-empty"):
            route_task(" ")


if __name__ == "__main__":
    unittest.main()
