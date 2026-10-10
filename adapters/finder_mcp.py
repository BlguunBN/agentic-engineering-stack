"""Synchronous stdio-MCP facade for Local Capability Finder Contract v1."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from adapters.finder_contract import FinderContractError


class FinderMCPClient:
    """Adapt Finder's documented MCP tools and registration CLI to the Stack facade."""

    def __init__(
        self,
        command: list[str],
        *,
        finder_root: Path,
        env: dict[str, str] | None = None,
        agent: str | None = None,
    ):
        if not command:
            raise ValueError("Finder MCP command must not be empty")
        self.finder_root = Path(finder_root).resolve()
        self.agent = agent
        self.env = dict(os.environ if env is None else env)
        try:
            self.process = subprocess.Popen(
                command,
                cwd=self.finder_root,
                env=self.env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
            )
        except OSError as exc:
            raise FinderContractError("UNSUPPORTED_OPERATION", f"Cannot start Finder MCP server: {exc}") from exc
        self._next_id = 1
        self._plans: dict[str, dict[str, Any]] = {}
        initialized = self._request("initialize", {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "agentic-engineering-stack", "version": "1"},
        })
        if initialized.get("protocolVersion") != "2025-11-25":
            self.close()
            raise FinderContractError("INCOMPATIBLE_CONTRACT", "Finder MCP handshake did not negotiate the expected protocol")
        self._notify("notifications/initialized", {})

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        process = self.process
        if process.poll() is not None or process.stdin is None:
            raise FinderContractError("EXECUTION_FAILED", "Finder MCP server is not running")
        try:
            process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method, "params": params}) + "\n")
            process.stdin.flush()
        except OSError as exc:
            raise FinderContractError("EXECUTION_FAILED", f"Cannot notify Finder MCP server: {exc}") from exc

    def close(self) -> None:
        process = getattr(self, "process", None)
        if process is None:
            return
        if process.poll() is None:
            if process.stdin:
                process.stdin.close()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream and not stream.closed:
                stream.close()

    def __enter__(self) -> "FinderMCPClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        process = self.process
        if process.poll() is not None or process.stdin is None or process.stdout is None:
            raise FinderContractError("EXECUTION_FAILED", "Finder MCP server is not running")
        request_id = self._next_id
        self._next_id += 1
        request = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
        try:
            process.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
            process.stdin.flush()
            while True:
                line = process.stdout.readline()
                if not line:
                    detail = process.stderr.read() if process.stderr else ""
                    raise FinderContractError("EXECUTION_FAILED", f"Finder MCP server exited without a response: {detail.strip()}")
                response = json.loads(line)
                if response.get("jsonrpc") == "2.0" and "id" not in response and isinstance(response.get("method"), str):
                    continue
                break
        except (OSError, json.JSONDecodeError) as exc:
            raise FinderContractError("EXECUTION_FAILED", f"Invalid Finder MCP response: {exc}") from exc
        if response.get("jsonrpc") != "2.0" or response.get("id") != request_id:
            raise FinderContractError("CONFLICT", "Finder MCP response ID did not match the request")
        if "error" in response:
            error = response["error"]
            data = error.get("data") if isinstance(error, dict) else None
            code = data.get("code") if isinstance(data, dict) else None
            raise FinderContractError(code or "CONFLICT", str(error.get("message", "Finder MCP call failed")))
        result = response.get("result")
        if not isinstance(result, dict):
            raise FinderContractError("CONFLICT", "Finder MCP returned a malformed result")
        return result

    def _tool(self, name: str, arguments: dict[str, Any]) -> Any:
        result = self._request("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise FinderContractError("EXECUTION_FAILED", "Finder MCP tool returned an error")
        content = result.get("content")
        if not isinstance(content, list) or not content or not isinstance(content[0], dict):
            raise FinderContractError("CONFLICT", f"Finder tool {name} returned no structured content")
        try:
            return json.loads(content[0]["text"])
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise FinderContractError("CONFLICT", f"Finder tool {name} returned invalid JSON content") from exc

    def get_contract_info(self) -> dict[str, Any]:
        return self._tool("get_contract_info", {})

    def register_source(self, namespace: str, manifest_path: str) -> dict[str, Any]:
        manifest = Path(manifest_path).resolve()
        source_path = manifest.parent / "suites"
        if not manifest.is_file() or not source_path.is_dir():
            raise FinderContractError("NOT_FOUND", "Stack manifest or suites directory is missing")
        library = Path(self.env.get("CAPFIND_LIBRARY") or (Path(self.env.get("CAPFIND_HOME", str(Path.home()))) / "ai-agent-library")).expanduser()
        catalog = self.finder_root / "library_catalog.py"
        if not catalog.is_file():
            raise FinderContractError("UNSUPPORTED_OPERATION", "Finder registration CLI is unavailable")
        def cli(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, str(catalog), *args], cwd=self.finder_root,
                env=self.env, capture_output=True, text=True, encoding="utf-8", check=False,
            )
        listed = cli("list-sources", "--json", "--library", str(library))
        if listed.returncode != 0:
            raise FinderContractError("EXECUTION_FAILED", listed.stderr.strip() or "Cannot inspect Finder sources")
        try:
            sources = json.loads(listed.stdout)
        except json.JSONDecodeError as exc:
            raise FinderContractError("CONFLICT", "Finder source registry is malformed") from exc
        previous = next((row for row in sources if row.get("id") == namespace), None)
        if previous:
            if Path(previous["path"]).resolve() != source_path.resolve():
                raise FinderContractError("CONFLICT", f"Finder source {namespace} points to a different path")
            if previous.get("trust") != "approved":
                raise FinderContractError("UNTRUSTED", f"Finder source {namespace} is not approved; review it through Finder's documented CLI")
        registered = cli("register-source", "--id", namespace, "--path", str(source_path), "--trust", "approved", "--library", str(library))
        if registered.returncode != 0:
            raise FinderContractError("CONFLICT", registered.stderr.strip() or registered.stdout.strip())
        indexed = cli("--quiet")
        if indexed.returncode != 0:
            raise FinderContractError("EXECUTION_FAILED", indexed.stderr.strip() or "Finder catalog refresh failed")
        self._tool("refresh_catalog", {})
        # Verify registration against exact public IDs; do not infer success from CLI output.
        from stack_manifest import load_manifest
        expected = [entry["id"] for entry in load_manifest(manifest)["capabilities"]]
        for capability_id in expected:
            self.get_capability(capability_id)
        return {"namespace": namespace, "registered_ids": expected}

    def search_capabilities(self, query: str, k: int = 3, **filters: Any) -> list[dict[str, Any]]:
        source = filters.pop("source", None)
        unknown = set(filters) - {"kind", "agent", "project_hint"}
        if unknown:
            raise ValueError(f"unsupported Finder search filters: {', '.join(sorted(unknown))}")
        if source is not None and (not isinstance(source, str) or not source.strip()):
            raise ValueError("source must be a non-empty string")
        arguments: dict[str, Any] = {"query": query, "limit": 20 if source else k}
        for key in ("kind", "agent", "project_hint"):
            if filters.get(key) is not None:
                arguments[key] = filters[key]
        rows = self._tool("search_capabilities", arguments)
        if not isinstance(rows, list):
            raise FinderContractError("CONFLICT", "Finder search returned malformed results")
        output = []
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise FinderContractError("CONFLICT", "Finder search returned malformed metadata")
            if source and row["id"].split(":", 1)[0] != source:
                continue
            output.append({**row, "kind": row.get("kind", row.get("type")), "source": row["id"].split(":", 1)[0]})
            if len(output) == k:
                break
        return output

    def get_capability(self, capability_id: str) -> dict[str, Any]:
        item = self._tool("get_capability", {"capability_id": capability_id})
        if not isinstance(item, dict) or item.get("id") != capability_id:
            raise FinderContractError("NOT_FOUND", f"No exact capability metadata for {capability_id}")
        trust_status = item.get("trust_status", "unscanned")
        item["trust"] = "trusted" if trust_status == "approved" else trust_status
        item["revision"] = item.get("content_hash")
        agents = item.get("compatible_agents")
        item["compatible"] = not (self.agent and isinstance(agents, list) and agents and self.agent not in agents and "all" not in agents)
        item["kind"] = item.get("kind", item.get("type"))
        return item

    def load_skill(self, capability_id: str, revision: str | None = None) -> dict[str, Any]:
        arguments: dict[str, Any] = {"capability_id": capability_id}
        if revision is not None:
            arguments["revision"] = revision
        result = self._tool("load_skill", arguments)
        result["trust"] = "trusted" if result.get("trust_status") == "approved" else result.get("trust_status", "unscanned")
        return result

    def get_tool_schema(self, tool_id: str) -> dict[str, Any]:
        return self._tool("get_tool_schema", {"capability_id": tool_id})

    def prepare_activation(self, capability_id: str, agent: str) -> dict[str, Any]:
        result = self._tool("prepare_activation", {"capability_id": capability_id, "agent": agent})
        plan = result.get("plan") if isinstance(result, dict) else None
        if not isinstance(plan, dict) or plan.get("id") != capability_id:
            raise FinderContractError("CONFLICT", "Finder returned an invalid activation preview")
        normalized = {**plan, "capability_id": capability_id}
        plan_id = json.dumps({key: normalized.get(key) for key in ("capability_id", "agent", "revision", "target", "status", "method")}, sort_keys=True, separators=(",", ":"))
        import hashlib
        normalized["plan_id"] = hashlib.sha256(plan_id.encode("utf-8")).hexdigest()
        self._plans[normalized["plan_id"]] = normalized
        return normalized

    def activate_skill(self, plan_id: str, approval: dict[str, Any]) -> dict[str, Any]:
        plan = self._plans.get(plan_id)
        if plan is None:
            raise FinderContractError("STALE_REVISION", "Activation plan was not prepared by this Finder client")
        current = self.prepare_activation(plan["capability_id"], plan["agent"])
        if current["plan_id"] != plan_id or current.get("status") not in ("ready", "already_active"):
            raise FinderContractError("STALE_REVISION", "Activation preview changed or is no longer ready")
        trust = current.get("trust_status", "unscanned")
        if trust == "blocked":
            raise FinderContractError("UNTRUSTED", "Finder policy blocks this skill")
        result = self._tool("activate_skill", {
            "capability_id": plan["capability_id"], "agent": plan["agent"],
            "confirm_untrusted": trust in ("needs_review", "unscanned"), "method": "link",
        })
        return {**result, "plan_id": plan_id}

    def deactivate_skill(self, capability_id: str, agent: str, approval: dict[str, Any]) -> dict[str, Any]:
        result = self._tool("deactivate_skill", {"capability_id": capability_id, "agent": agent})
        return {**result, "capability_id": capability_id, "manager_owned": True}
