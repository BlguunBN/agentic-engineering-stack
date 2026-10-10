"""Black-box Contract v1 integration with a compatible Finder checkout."""

import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FINDER_ROOT = Path(os.environ.get("CAPFIND_CHECKOUT", ROOT.parent / "local-capability-finder-release"))
if not (FINDER_ROOT / "capability_mcp.py").is_file():
    FINDER_ROOT = Path()
sys.path.insert(0, str(ROOT))
from adapters.finder_contract import FinderContractClient
from adapters.finder_mcp import FinderMCPClient


@unittest.skipUnless(FINDER_ROOT and (FINDER_ROOT / "capability_mcp.py").is_file(), "set CAPFIND_CHECKOUT to a Contract v1 Finder checkout")
class FinderMCPIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.library = self.base / "library"
        personal = self.home / ".agents" / "skills" / "personal-dicom"
        personal.mkdir(parents=True)
        (personal / "SKILL.md").write_text(
            "---\nname: personal-dicom\ndescription: Validate DICOM imaging series\n---\nPersonal DICOM workflow.\n",
            encoding="utf-8",
        )
        self.env = dict(os.environ)
        self.env["CAPFIND_HOME"] = str(self.home)
        self.env["CAPFIND_LIBRARY"] = str(self.library)
        self.client = FinderMCPClient(
            [sys.executable, str(FINDER_ROOT / "capability_mcp.py")],
            finder_root=FINDER_ROOT,
            env=self.env,
            agent="codex",
        )
        self.addCleanup(self.client.close)
        self.contract = FinderContractClient(self.client)

    def test_register_search_exact_load_and_activation_lifecycle(self):
        manifest = ROOT / "stack.manifest.json"
        ids = self.contract.register_stack(manifest)
        self.assertEqual(18, len(ids))
        self.assertEqual(18, len(set(ids)))

        hits = self.contract.search_capabilities("table-driven unit tests with fixtures", k=3, kind="skill")
        selected = "aes:skill:unit-testing-suite"
        self.assertIn(selected, [hit["id"] for hit in hits])
        loaded = self.contract.load_skill(selected)
        self.assertEqual(selected, loaded["id"])
        self.assertIn("Arrange", loaded["content"])
        self.assertNotIn("DICOM workflow", loaded["content"])

        personal = self.contract.search_capabilities("validate DICOM imaging series", k=3, kind="skill")
        self.assertIn("agents:skill:personal-dicom", [hit["id"] for hit in personal])

        plan = self.client.prepare_activation(selected, "codex")
        approval = {
            "approved": True,
            "plan_id": plan["plan_id"],
            "action": "activate_skill",
            "target": selected,
            "approved_by": "test-user",
            "reference": "integration-test",
        }
        activated = self.contract.activate_skill(plan, approval)
        self.assertEqual("activated", activated["status"])
        self.assertTrue((Path(activated["path"]) / "SKILL.md").is_file())
        deactivated = self.contract.deactivate_skill(selected, "codex", {
            "approved": True,
            "action": "deactivate_skill",
            "target": selected,
            "approved_by": "test-user",
            "reference": "integration-test-cleanup",
        })
        self.assertTrue(deactivated["manager_owned"])
        self.assertFalse(os.path.lexists(activated["path"]))


if __name__ == "__main__":
    unittest.main()
