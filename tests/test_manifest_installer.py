"""Manifest and safe installer behavior tests using disposable roots."""

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import install
from stack_manifest import MANIFEST_PATH, ManifestError, load_manifest, validate_manifest


class ManifestTests(unittest.TestCase):
    def test_manifest_has_18_distinct_on_demand_skills(self):
        manifest = load_manifest()
        entries = manifest["capabilities"]
        self.assertEqual(len(entries), 18)
        self.assertEqual(len({entry["id"] for entry in entries}), 18)
        self.assertTrue(all(entry["activation"] == "on-demand" for entry in entries))

    def test_duplicate_ids_and_paths_are_rejected(self):
        manifest = load_manifest()
        duplicate = copy.deepcopy(manifest)
        duplicate["capabilities"].append(copy.deepcopy(duplicate["capabilities"][0]))
        with self.assertRaisesRegex(ManifestError, "duplicate capability ID"):
            validate_manifest(duplicate)

    def test_path_traversal_is_rejected(self):
        manifest = {
            "schema_version": 1,
            "namespace": "aes",
            "package": "agentic-engineering-stack",
            "capabilities": [{
                "id": "aes:skill:outside",
                "path": "../outside",
                "kind": "skill",
                "activation": "on-demand",
                "profile_tags": [],
                "requires": [],
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ManifestError, "escapes repository root"):
                validate_manifest(manifest, Path(directory))

    def test_profiles_are_valid_and_route_to_manifest_ids(self):
        manifest_ids = {entry["id"] for entry in load_manifest()["capabilities"]}
        profiles = sorted((ROOT / "profiles").glob("*.json"))
        self.assertEqual({path.stem for path in profiles}, {"minimal", "core", "frontend", "infrastructure", "research", "strict"})
        for path in profiles:
            profile = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(profile["name"], path.stem)
            self.assertLessEqual(profile["max_loaded_suites"], 2)
            for route in profile["routes"]:
                self.assertIn(route["primary"], manifest_ids)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.root = self.home / ".claude" / "skills"
        self.root.parent.mkdir(parents=True)
        self.patches = [
            patch.object(install, "HOME", self.home),
            patch.object(install, "AGENT_SKILL_ROOTS", {"claude": self.root}),
        ]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def test_dry_run_does_not_create_targets_or_home_rules(self):
        report = install.install(target_agents=["claude"], copy_rules=True, dry_run=True, skills=["systematic-debugging-suite"])
        self.assertEqual(len(report.changed), 2)
        self.assertFalse(self.root.exists())
        self.assertFalse((self.home / "AGENTS.local.md").exists())

    def test_explicit_selection_installs_only_that_skill_and_is_idempotent(self):
        first = install.install(target_agents=["claude"], copy_rules=False, skills=["aes:skill:docker-containers-suite"])
        target = self.root / "docker-containers-suite"
        self.assertEqual(len(first.changed), 1)
        self.assertTrue((target / "SKILL.md").is_file())
        self.assertEqual([p.name for p in self.root.iterdir()], ["docker-containers-suite"])
        second = install.install(target_agents=["claude"], copy_rules=False, skills=["docker-containers-suite"])
        # Links/junctions to this source are idempotent; fallback copies are
        # deliberately conflicts because the standalone installer cannot prove ownership.
        if target.resolve() == (ROOT / "suites" / "docker-containers-suite").resolve():
            self.assertEqual(len(second.skipped), 1)
            self.assertFalse(second.conflicts)
        else:
            self.assertEqual(len(second.conflicts), 1)

    def test_existing_unmanaged_target_is_preserved_as_conflict(self):
        self.root.mkdir(parents=True)
        target = self.root / "unit-testing-suite"
        target.mkdir()
        marker = target / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        report = install.install(target_agents=["claude"], copy_rules=False, skills=["unit-testing-suite"])
        self.assertEqual(len(report.conflicts), 1)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
        self.assertEqual(report.exit_code, 1)

    def test_empty_unknown_agents_and_skills_are_rejected(self):
        with self.assertRaisesRegex(install.InstallError, "at least one agent"):
            install.install(target_agents=[], copy_rules=False)
        with self.assertRaisesRegex(install.InstallError, "Unknown agent"):
            install.install(target_agents=["not-an-agent"], copy_rules=False)
        with self.assertRaisesRegex(install.InstallError, "at least one skill"):
            install.install(target_agents=["claude"], copy_rules=False, skills=[])
        with self.assertRaisesRegex(install.InstallError, "Unknown skill"):
            install.install(target_agents=["claude"], copy_rules=False, skills=["not-a-suite"])


if __name__ == "__main__":
    unittest.main()
