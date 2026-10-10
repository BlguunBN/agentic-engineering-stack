# Current State Baseline

Baseline captured from the repository before implementation changes, 2026-09-29.

## Inventory and context

- 18 canonical suites exist under `suites/`, with matching `name` frontmatter and folder names.
- Combined suite bodies: 65,678 Unicode characters / 66,509 UTF-8 bytes. `characters / 4` gives a rough 16,419-token estimate only; it is not provider/tokenizer accounting.
- The installer's `templates/AGENTS.md` names all 18 suites in its Tier 1 routing instructions. Its body is a routing/instruction index, not the suite bodies themselves.
- Each suite currently lives in one `SKILL.md`; no suite-local reference links were found in the baseline scan. No test suite, CI workflow, package/test configuration, manifest, profile or routing implementation existed.
- Suites are broadly YAML-frontmattered, but required sections and description quality are not consistently linted. Some suites include long framework recipes inline.

## Baseline route cases

These are expected human-readable routes from the existing template, not measured classifier accuracy. Tier 1 maps task intents directly to suite folder names; niche capabilities fall through to Finder search, then optional external discovery.

| Task example | Baseline Tier 1 selection / fallback |
|---|---|
| Diagnose a crashing API regression | `systematic-debugging-suite` |
| Add regression tests for a bug | `unit-testing-suite` |
| Review a pull request for correctness/security | `code-review-standards-suite` |
| Resolve a merge conflict and prepare a commit | `git-workflow-suite` |
| Build a responsive Next.js page | `frontend-webapp-design-suite` |
| Audit a form for WCAG keyboard access | `ux-accessibility-suite` |
| Select design tokens and component primitives | `ui-design-systems-suite` |
| Automate a browser flow with Playwright | `browser-automation-suite` |
| Harden a container image | `docker-containers-suite` |
| Diagnose a Kubernetes CrashLoopBackOff | `kubernetes-k8s-suite` |
| Review remote Terraform state locking | `terraform-iac-suite` |
| Extract structured tables from a PDF | `office-documents-suite` |
| Crawl a public documentation site | `web-scraping-suite` |
| Prototype a Figma-to-code component | `figma-design-prototyping-suite` |
| Implement platform-specific mobile navigation | `mobile-native-ui-suite` |
| Refine a landing-page signup flow | `landing-page-cro-suite` |
| Build an interactive Three.js scene | `creative-3d-motion-suite` |
| Find a specialist bioinformatics capability | Finder Tier 2 search; optional external discovery only if no suitable result |

## Installer baseline and risk

`install.py` currently maps 12 agent aliases to static paths, discovers roots by parent/root existence, links or copies all 18 suites, and optionally copies `AGENTS.local.md`. Existing suite destinations are silently skipped; it has no dry-run, lifecycle verification, explicit empty/unknown-agent validation, update/remove/rollback operation, or tests. On link failure it falls back to copying. The default install may affect multiple detected home directories, so changes must be tested in disposable homes before release. No installation was run during this baseline.

README currently makes numeric token/cost-saving claims (including 83.6%) without benchmark code or reproducible provider accounting in this checkout. These claims are not validated baseline results and must not be repeated as facts.

## Baseline verification

Run `python -m unittest discover -s tests -v`. The initial suite checks preserve the 18 names and simple frontmatter identity. Installer behavior will receive isolated disposable-home tests alongside S1 changes; this baseline did not execute installation.
