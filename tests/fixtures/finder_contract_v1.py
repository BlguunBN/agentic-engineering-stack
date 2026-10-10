"""Minimal black-box MCP fixture for Stack/Finder Contract v1 client tests."""

import json
import sys

SKILL_ID = "aes:skill:unit-testing-suite"
SKILL = "---\nname: unit-testing-suite\ndescription: test fixture\n---\n# Fixture skill body\n"
INFO = {
    "contract": "local-capability-finder",
    "version": 1,
    "features": ["register_source", "search", "get", "load", "activation-preview", "activation", "deactivation", "tool-schema"],
    "registration": "library_catalog.py register-source",
}
INITIALIZED = False

RECORD = {
    "id": SKILL_ID,
    "type": "skill",
    "kind": "skill",
    "name": "unit-testing-suite",
    "source_id": "aes",
    "source_path": "tests/fixtures/unit-testing-suite/SKILL.md",
    "content_hash": "sha256:fixture-v1",
    "trust_status": "approved",
    "compatible_agents": ["all"],
    "availability": ["codex"],
}


def tool(name, args):
    if name == "get_contract_info":
        return INFO
    if name == "search_capabilities":
        return [{"id": SKILL_ID, "type": "skill", "name": RECORD["name"], "reason": "unit test fixture", "availability": ["codex"]}]
    if name == "get_capability":
        return RECORD
    if name == "load_skill":
        if args.get("revision") not in (None, RECORD["content_hash"]):
            return {"error": {"code": "STALE_REVISION", "message": "revision mismatch"}}
        return {"id": SKILL_ID, "name": RECORD["name"], "source_path": RECORD["source_path"], "revision": RECORD["content_hash"], "trust_status": "approved", "content": SKILL}
    if name == "get_tool_schema":
        return {"id": args["capability_id"], "schema": {"type": "object"}}
    if name == "prepare_activation":
        return {"plan": {"id": SKILL_ID, "agent": args["agent"], "revision": RECORD["content_hash"], "target": "/tmp/fixture", "status": "ready", "method": "symlink", "trust_status": "approved"}, "findings": [], "approval_required": False}
    if name == "activate_skill":
        return {"id": SKILL_ID, "agent": args["agent"], "status": "activated", "path": "/tmp/fixture"}
    if name == "deactivate_skill":
        return {"id": SKILL_ID, "agent": args["agent"], "status": "deactivated", "path": "/tmp/fixture"}
    if name == "refresh_catalog":
        return {"indexed": 18, "path": "/tmp/fixture/index.json"}
    raise ValueError(f"unknown tool: {name}")


def dispatch(request):
    method = request.get("method")
    params = request.get("params", {})
    if method == "initialize":
        return {"protocolVersion": "2025-11-25", "capabilities": {"tools": {}}, "serverInfo": {"name": "finder-fixture", "version": "0.2.0"}}
    if method == "tools/call":
        if not INITIALIZED:
            return {"_jsonrpc_error": {"code": -32002, "message": "initialized notification required"}}
        result = tool(params["name"], params.get("arguments", {}))
        if "error" in result:
            return {"_jsonrpc_error": result["error"]}
        return {"content": [{"type": "text", "text": json.dumps(result)}]}
    return {"error": {"code": -32601, "message": "unknown method"}}


for line in sys.stdin:
    request = json.loads(line)
    if request.get("method") == "notifications/initialized":
        INITIALIZED = True
        continue
    if "id" not in request:
        continue
    result = dispatch(request)
    if request.get("method") == "tools/call":
        print(json.dumps({"jsonrpc": "2.0", "method": "notifications/message", "params": {"level": "info", "data": "fixture notice"}}), flush=True)
    response = {"jsonrpc": "2.0", "id": request["id"]}
    if "_jsonrpc_error" in result:
        response["error"] = result["_jsonrpc_error"]
    else:
        response["result"] = result
    print(json.dumps(response), flush=True)
