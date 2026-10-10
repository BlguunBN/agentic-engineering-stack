"""Exercise Contract v1 facade over an actual JSON-RPC stdio subprocess."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters.finder_contract import FinderContractClient
from adapters.finder_mcp import FinderMCPClient


class FinderMCPWireTests(unittest.TestCase):
    def test_version_search_exact_load_and_approved_state_changes(self):
        fixture = ROOT / "tests" / "fixtures" / "finder_contract_v1.py"
        with FinderMCPClient([sys.executable, str(fixture)], finder_root=ROOT, agent="codex") as finder:
            client = FinderContractClient(finder)
            self.assertEqual(1, finder.get_contract_info()["version"])
            hits = client.search_capabilities("unit testing", k=3)
            capability_id = "aes:skill:unit-testing-suite"
            self.assertEqual(capability_id, hits[0]["id"])
            loaded = client.load_skill(capability_id, revision="sha256:fixture-v1")
            self.assertEqual(capability_id, loaded["id"])
            self.assertIn("Fixture skill body", loaded["content"])
            self.assertEqual("sha256:fixture-v1", loaded["revision"])

            plan = client.prepare_activation(capability_id, "codex")
            approval = {
                "approved": True,
                "plan_id": plan["plan_id"],
                "action": "activate_skill",
                "target": capability_id,
                "approved_by": "test-user",
                "reference": "wire-test",
            }
            active = client.activate_skill(plan, approval)
            self.assertEqual("activated", active["status"])
            removed = client.deactivate_skill(capability_id, "codex", {
                "approved": True,
                "action": "deactivate_skill",
                "target": capability_id,
                "approved_by": "test-user",
                "reference": "wire-test-cleanup",
            })
            self.assertTrue(removed["manager_owned"])


if __name__ == "__main__":
    unittest.main()
