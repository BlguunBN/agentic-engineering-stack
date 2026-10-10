"""Pin the Finder contract surface the Stack adapter depends on.

Runs against a live compatible Finder checkout in a disposable library, and
skips without one. Catches silent Finder drift (added/removed tools,
renamed features) that the stdio fixture cannot see.
"""

import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FINDER_ROOT = Path(
    os.environ.get("CAPFIND_CHECKOUT", ROOT.parent / "local-capability-finder-release")
)
if not (FINDER_ROOT / "capability_mcp.py").is_file():
    FINDER_ROOT = Path()
sys.path.insert(0, str(ROOT))
from adapters.finder_mcp import FinderMCPClient

REQUIRED_FEATURES = {
    "register_source",
    "search",
    "get",
    "load",
    "activation-preview",
    "activation",
    "deactivation",
    "tool-schema",
}


@unittest.skipUnless(
    FINDER_ROOT and (FINDER_ROOT / "capability_mcp.py").is_file(),
    "set CAPFIND_CHECKOUT to a Contract v1 Finder checkout",
)
class FinderContractSurfaceTests(unittest.TestCase):
    def test_live_surface_matches_pinned_contract(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        env = dict(os.environ)
        env["CAPFIND_HOME"] = str(Path(temp.name) / "home")
        env["CAPFIND_LIBRARY"] = str(Path(temp.name) / "lib")
        with FinderMCPClient(
            [sys.executable, str(FINDER_ROOT / "capability_mcp.py")],
            finder_root=FINDER_ROOT,
            env=env,
            agent="codex",
        ) as finder:
            info = finder.get_contract_info()
            self.assertEqual("local-capability-finder", info["contract"])
            self.assertEqual(1, info["version"])
            self.assertTrue(
                REQUIRED_FEATURES.issubset(set(info["features"])),
                f"Finder dropped contract features: {REQUIRED_FEATURES - set(info.get('features', []))}",
            )
            finder.register_source("aes", str(ROOT / "stack.manifest.json"))
            rows = finder.search_capabilities("unit testing", k=1, kind="skill")
            self.assertTrue(rows and rows[0]["id"].endswith("unit-testing-suite"))
            detail = finder.get_capability(rows[0]["id"])
            self.assertIn("trust_status", detail)
            self.assertIn("content_hash", detail)


if __name__ == "__main__":
    unittest.main()
