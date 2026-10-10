# Joint compatibility matrix

This matrix separates repository/contract tests from native host support. A configured MCP server path is not proof that a host discovers tools, presents approvals correctly, or executes skills safely.

## Repository and protocol coverage

| Surface | Evidence | Status |
|---|---|---|
| Stack standalone | Stack unit tests, manifest/lint/routing/handoff checks | Hosted Windows and Ubuntu CI passed for Python 3.11 and 3.12 on Stack review revision `8b88eae12f9dd5a1d73118d062c14bf795954010`. |
| Finder standalone | Finder unit tests and portable retrieval evaluation | Hosted Windows and Ubuntu CI passed for Python 3.11, 3.12, and 3.13 on Finder review revision `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76`. |
| Finder package | CLI syntax, package contents, installed-package/MCP smoke checks | Hosted Ubuntu and Windows package jobs passed for Finder review revision `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76`. |
| Stack + Finder Contract v1 | Stack workflow checks out the exact Finder SHA above; live stdio tests exercise registration, exact-ID search/load, personal-skill fallback, and approved activation/deactivation in a disposable home | Joint hosted result is gated on the Stack CI run for the pin; see [release validation](release-validation.md). |
| MCP protocol compatibility | Finder contract handshake and stdio wire fixtures | Contract v1 is distinct from transport protocol version. The Stack rejects missing/incompatible contracts and retains deterministic Tier 1 behavior. |

All hosted results are evidence for the cited review snapshots, not a published release or a claim of universal compatibility.

## Agent hosts

| Host/surface | What was exercised | What remains unverified |
|---|---|---|
| OMP 18.4.4 | Local MCP config discovery/connection and exposure of all nine Finder Contract v1 tools | No model-driven search/load, activation workflow, native approval UX, or coding task was run. |
| Pi session | One isolated worker returned a schema-valid compact handoff; coordinator inspected its findings and validated the report | No Stack-distributed Pi adapter, native approval flow, or general concurrency/budget enforcement. |
| Other MCP clients | Finder exposes a stdio server using the documented contract | Host-specific configuration, tool discovery, approval prompts, and execution are not certified here. |
| Static skill-directory installer mappings | Isolated Stack installer tests | These do not establish that each agent host discovers or applies skills. |

Use the host's current MCP configuration documentation and keep activation disabled unless the exact skill and target are explicitly reviewed. See [host compatibility and delegation evidence](host-compatibility.md).
