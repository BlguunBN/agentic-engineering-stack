# Joint compatibility matrix

This matrix separates repository/contract tests from native host support. A configured MCP server path is not proof that a host discovers tools, presents approvals correctly, or executes skills safely.

## Repository and protocol coverage

| Surface | Evidence | Status |
|---|---|---|
| Stack standalone | Stack unit tests, manifest/lint/routing/handoff checks | Hosted Windows and Ubuntu CI passed for Python 3.11 and 3.12 on Stack review HEAD `da171055763c7808182a3d8167fe3966d2afef24`, including the joint pin. |
| Finder standalone | Finder unit tests and portable retrieval evaluation | Hosted Windows and Ubuntu CI passed for Python 3.11, 3.12, and 3.13 on Finder review HEAD `1886809b5fce5e340251ca533e1dea89cdf2d50f`. |
| Finder package | CLI syntax, package contents, installed-package/MCP smoke checks | Hosted Ubuntu and Windows package jobs passed for Finder review HEAD `1886809b5fce5e340251ca533e1dea89cdf2d50f`. |
| Stack + Finder Contract v1 | Stack workflow checks out the exact Finder SHA above; live stdio tests exercise registration, exact-ID search/load, personal-skill fallback, and approved activation/deactivation in a disposable home | Passed hosted Windows/Ubuntu Python 3.11/3.12 matrix; see the linked run in [release validation](release-validation.md). |
| MCP protocol compatibility | Finder contract handshake and stdio wire fixtures | Contract v1 is distinct from transport protocol version. The Stack rejects missing/incompatible contracts and retains deterministic Tier 1 behavior. |

All hosted results are evidence for the cited review snapshots, not a published release or a claim of universal compatibility.

## Agent hosts

| Host/surface | What was exercised | What remains unverified |
|---|---|---|
| OMP 18.4.4 | Project MCP config connection; a real model session searched and loaded one exact Finder skill and fixed a disposable fixture with passing regressions. | Native profile discovery and approval UX remain unverified; activation was tested separately via Finder CLI in a disposable home. See [session evidence](evidence/omp-finder-contract-v1-session.md). |
| Pi session | One isolated worker returned a schema-valid compact handoff; coordinator inspected its findings and validated the report | No Stack-distributed Pi adapter, native approval flow, or general concurrency/budget enforcement. |
| Other MCP clients | Finder exposes a stdio server using the documented contract | Host-specific configuration, tool discovery, approval prompts, and execution are not certified here. |
| Static skill-directory installer mappings | Isolated Stack installer tests | These do not establish that each agent host discovers or applies skills. |

Use the host's current MCP configuration documentation and keep activation disabled unless the exact skill and target are explicitly reviewed. See [host compatibility and delegation evidence](host-compatibility.md).
