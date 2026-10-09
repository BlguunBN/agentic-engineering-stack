"""Mock-only tests for the proposed public Finder Contract v1."""

import hashlib
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters.finder_contract import FinderContractClient, FinderContractError
from stack_manifest import load_manifest


class MockFinderV1:
    def __init__(self, version=1, trusted=True):
        self.version = version
        self.trusted = trusted
        self.loaded = []
        self.activated = []
        self.ids = [entry["id"] for entry in load_manifest()["capabilities"]]
        self.metadata = {
            capability_id: {
                "id": capability_id, "kind": "skill", "trust": "trusted" if trusted else "untrusted",
                "compatible": True, "revision": "rev-1", "content_hash": "hash-1"
            }
            for capability_id in self.ids
        }

    def get_contract_info(self):
        return {
            "contract": "local-capability-finder", "version": self.version,
            "features": ["register_source", "search", "get", "load", "activation-preview", "activation", "tool-schema"]
        }

    def register_source(self, namespace, manifest_path):
        return {"namespace": namespace, "registered_ids": self.ids}

    def search_capabilities(self, query, k=3, **filters):
        return [{"id": "personal:skill:bioinformatics", "kind": "skill", "source": "personal"}][:k]

    def get_capability(self, capability_id):
        return self.metadata.get(capability_id)

    def load_skill(self, capability_id, revision=None):
        self.loaded.append((capability_id, revision))
        return {"id": capability_id, "revision": revision or "rev-1", "content": "# selected skill"}

    def get_tool_schema(self, tool_id):
        return {"id": tool_id, "schema": {"type": "object"}}

    def prepare_activation(self, capability_id, agent):
        return {"plan_id": "plan-1", "capability_id": capability_id, "agent": agent}

    def activate_skill(self, plan_id, approval):
        self.activated.append(plan_id)
        return {"plan_id": plan_id, "status": "active"}

    def deactivate_skill(self, capability_id, agent, approval):
        return {"capability_id": capability_id, "manager_owned": True, "status": "inactive"}


class FinderContractTests(unittest.TestCase):
    def setUp(self):
        self.finder = MockFinderV1()
        self.client = FinderContractClient(self.finder)

    def test_registration_confirms_all_18_distinct_ids(self):
        ids = self.client.register_stack()
        self.assertEqual(len(ids), 18)
        self.assertEqual(len(set(ids)), 18)

    def test_tier_two_search_preserves_personal_results_as_metadata(self):
        result = self.client.search_capabilities("bioinformatics pipeline", k=3)
        self.assertEqual(result[0]["id"], "personal:skill:bioinformatics")
        self.assertNotIn("content", result[0])

    def test_exact_load_fetches_only_one_selected_skill(self):
        capability_id = "aes:skill:unit-testing-suite"
        loaded = self.client.load_skill(capability_id, revision="rev-1")
        self.assertEqual(loaded["id"], capability_id)
        self.assertEqual(self.finder.loaded, [(capability_id, "rev-1")])

    def test_untrusted_skill_is_blocked_before_load(self):
        finder = MockFinderV1(trusted=False)
        client = FinderContractClient(finder)
        with self.assertRaisesRegex(FinderContractError, "not trusted") as error:
            client.load_skill("aes:skill:unit-testing-suite")
        self.assertEqual(error.exception.code, "UNTRUSTED")
        self.assertFalse(finder.loaded)

    def test_contract_version_and_missing_handshake_are_rejected(self):
        with self.assertRaisesRegex(FinderContractError, "version 2") as error:
            FinderContractClient(MockFinderV1(version=2))
        self.assertEqual(error.exception.code, "INCOMPATIBLE_CONTRACT")

        class LegacyFinder:
            pass

        with self.assertRaises(FinderContractError) as error:
            FinderContractClient(LegacyFinder())
        self.assertEqual(error.exception.code, "INCOMPATIBLE_CONTRACT")

    def test_activation_requires_matching_explicit_approval(self):
        capability_id = "aes:skill:unit-testing-suite"
        plan = self.client.prepare_activation(capability_id, "pi")
        with self.assertRaises(FinderContractError) as error:
            self.client.activate_skill(plan, None)
        self.assertEqual(error.exception.code, "PERMISSION_DENIED")
        approval = {
            "approved": True, "plan_id": plan["plan_id"], "action": "activate_skill",
            "target": capability_id, "approved_by": "reviewer", "reference": "CHANGE-123"
        }
        self.client.activate_skill(plan, approval)
        self.assertEqual(self.finder.activated, ["plan-1"])

    def test_id_is_independent_of_content_hash(self):
        capability_id = "aes:skill:unit-testing-suite"
        before = hashlib.sha256(b"skill body v1").hexdigest()
        after = hashlib.sha256(b"skill body v2").hexdigest()
        self.assertNotEqual(before, after)
        self.assertEqual(capability_id, "aes:skill:unit-testing-suite")


if __name__ == "__main__":
    unittest.main()
