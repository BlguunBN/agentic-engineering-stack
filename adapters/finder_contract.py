"""Stack-side client for the proposed public Finder Contract v1 surface.

`finder` is a host/MCP client facade exposing contract operation methods; this
module deliberately does not import Finder implementation code or MCP SDKs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from stack_manifest import load_manifest

CONTRACT_NAME = "local-capability-finder"
CONTRACT_VERSION = 1
TRUSTED_LEVELS = {"trusted", "first-party"}


class FinderContractError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class FinderContractClient:
    def __init__(self, finder: Any):
        self.finder = finder
        try:
            info = self._call("get_contract_info")
        except FinderContractError as exc:
            raise FinderContractError("INCOMPATIBLE_CONTRACT", "Finder does not expose the required Contract v1 handshake") from exc
        if not isinstance(info, dict) or info.get("contract") != CONTRACT_NAME:
            raise FinderContractError("INCOMPATIBLE_CONTRACT", "Finder did not identify the required public contract")
        if info.get("version") != CONTRACT_VERSION:
            raise FinderContractError("INCOMPATIBLE_CONTRACT", f"Finder contract version {info.get('version')} is unsupported")
        features = info.get("features")
        if not isinstance(features, list) or not all(isinstance(feature, str) for feature in features):
            raise FinderContractError("INCOMPATIBLE_CONTRACT", "Finder contract features must be a string list")
        self.features = set(features)
        required = {"register_source", "search", "get", "load", "activation-preview", "activation"}
        missing = required - self.features
        if missing:
            raise FinderContractError("UNSUPPORTED_OPERATION", f"Finder Contract v1 lacks required features: {', '.join(sorted(missing))}")

    def _call(self, operation: str, *args: Any, **kwargs: Any) -> Any:
        method = getattr(self.finder, operation, None)
        if not callable(method):
            raise FinderContractError("UNSUPPORTED_OPERATION", f"Finder Contract v1 operation unavailable: {operation}")
        result = method(*args, **kwargs)
        if isinstance(result, dict) and isinstance(result.get("error"), dict):
            error = result["error"]
            raise FinderContractError(str(error.get("code", "CONFLICT")), str(error.get("message", "Finder request failed")))
        return result

    def register_stack(self, manifest_path: Path | None = None) -> list[str]:
        manifest = load_manifest(manifest_path) if manifest_path else load_manifest()
        expected = [entry["id"] for entry in manifest["capabilities"]]
        result = self._call("register_source", "aes", str(manifest_path or Path(__file__).resolve().parents[1] / "stack.manifest.json"))
        if not isinstance(result, dict) or result.get("namespace") != "aes":
            raise FinderContractError("CONFLICT", "Finder returned an invalid Stack registration result")
        registered = result.get("registered_ids")
        if not isinstance(registered, list) or set(registered) != set(expected) or len(registered) != len(expected):
            raise FinderContractError("CONFLICT", "Finder registration did not confirm all unique canonical Stack IDs")
        return expected

    def search_capabilities(self, query: str, k: int = 3, **filters: Any) -> list[dict[str, Any]]:
        if not query.strip() or isinstance(k, bool) or not 1 <= k <= 20:
            raise ValueError("query must be non-empty and k must be between 1 and 20")
        results = self._call("search_capabilities", query, k=k, **filters)
        if not isinstance(results, list) or len(results) > k:
            raise FinderContractError("CONFLICT", "Finder search must return a bounded metadata list")
        for item in results:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                raise FinderContractError("CONFLICT", "Finder search returned malformed metadata")
            if any(key in item for key in ("content", "skill_md", "body")):
                raise FinderContractError("CONFLICT", "Search must return metadata only; use exact-ID load")
        return results

    def get_capability(self, capability_id: str) -> dict[str, Any]:
        result = self._call("get_capability", capability_id)
        if not isinstance(result, dict) or result.get("id") != capability_id:
            raise FinderContractError("NOT_FOUND", f"No exact capability metadata for {capability_id}")
        return result

    def load_skill(self, capability_id: str, revision: str | None = None) -> dict[str, Any]:
        metadata = self.get_capability(capability_id)
        trust = metadata.get("trust")
        if trust not in TRUSTED_LEVELS:
            raise FinderContractError("UNTRUSTED", f"Capability {capability_id} is not trusted for loading")
        if metadata.get("compatible") is False:
            raise FinderContractError("UNSUPPORTED_AGENT", f"Capability {capability_id} is incompatible with this host")
        result = self._call("load_skill", capability_id, revision=revision)
        if not isinstance(result, dict) or result.get("id") != capability_id:
            raise FinderContractError("NOT_FOUND", f"Finder did not load exact ID {capability_id}")
        if not isinstance(result.get("content"), str) or not result["content"].strip():
            raise FinderContractError("CONFLICT", "load_skill must return one non-empty skill body")
        if revision is not None and result.get("revision") != revision:
            raise FinderContractError("STALE_REVISION", f"Finder returned a different revision for {capability_id}")
        return result

    def get_tool_schema(self, tool_id: str) -> dict[str, Any]:
        result = self._call("get_tool_schema", tool_id)
        if not isinstance(result, dict) or result.get("id") != tool_id or not isinstance(result.get("schema"), dict):
            raise FinderContractError("NOT_FOUND", f"No exact tool schema for {tool_id}")
        return result

    def prepare_activation(self, capability_id: str, agent: str) -> dict[str, Any]:
        result = self._call("prepare_activation", capability_id, agent)
        if not isinstance(result, dict) or not isinstance(result.get("plan_id"), str):
            raise FinderContractError("CONFLICT", "Activation preview must return a plan_id")
        return result

    def activate_skill(self, plan: dict[str, Any], approval: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(plan, dict) or not isinstance(plan.get("plan_id"), str):
            raise FinderContractError("CONFLICT", "A valid preview plan is required")
        target = plan.get("capability_id")
        if not isinstance(approval, dict) or approval.get("approved") is not True:
            raise FinderContractError("PERMISSION_DENIED", "Explicit approval is required before activation")
        if approval.get("plan_id") != plan["plan_id"]:
            raise FinderContractError("STALE_REVISION", "Approval does not match the prepared plan")
        if approval.get("action") != "activate_skill" or approval.get("target") != target:
            raise FinderContractError("PERMISSION_DENIED", "Approval must match the exact activation action and capability")
        if not all(isinstance(approval.get(key), str) and approval[key].strip() for key in ("approved_by", "reference")):
            raise FinderContractError("PERMISSION_DENIED", "Approval must identify an approver and reference")
        result = self._call("activate_skill", plan["plan_id"], approval)
        if not isinstance(result, dict) or result.get("plan_id") != plan["plan_id"]:
            raise FinderContractError("CONFLICT", "Finder returned an invalid activation result")
        return result

    def deactivate_skill(self, capability_id: str, agent: str, approval: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(approval, dict) or approval.get("approved") is not True:
            raise FinderContractError("PERMISSION_DENIED", "Explicit approval is required before deactivation")
        if approval.get("action") != "deactivate_skill" or approval.get("target") != capability_id:
            raise FinderContractError("PERMISSION_DENIED", "Approval must match the exact deactivation action and capability")
        if not all(isinstance(approval.get(key), str) and approval[key].strip() for key in ("approved_by", "reference")):
            raise FinderContractError("PERMISSION_DENIED", "Approval must identify an approver and reference")
        result = self._call("deactivate_skill", capability_id, agent, approval)
        if not isinstance(result, dict) or result.get("capability_id") != capability_id:
            raise FinderContractError("CONFLICT", "Finder returned an invalid deactivation result")
        if result.get("manager_owned") is not True:
            raise FinderContractError("PERMISSION_DENIED", "Finder may remove only manager-owned activations")
        return result
