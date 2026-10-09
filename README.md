# Agentic Engineering Stack ⚡

A collection of 18 engineering skill suites and routing guidance for AI coding agents. Host compatibility varies and is not implied by a configured installer path.

The repository describes three-tier capability routing and context-efficiency practices. Their end-to-end behavior and any token or cost savings are not yet benchmarked in this checkout.

---

## 🌟 Why This Exists

Most AI coding setups suffer from two major flaws:
1. **Tool Overload & Flakes:** Hundreds of fragmented, overlapping skills fighting for model attention or failing silently with mangled paths.
2. **Context Window Exhaustion:** AI agents dumping thousands of lines of logs, full-file reads, and conversational pleasantries into context, burning $100s/month and causing memory loss by turn 25.

**Agentic Engineering Stack** replaces ad-hoc agent behavior with a proven, disciplined architecture.

---

## 🏗️ The 3-Tier Routing Architecture

Routing profiles are executable via `routing.py`; see [routing behavior and CLI](docs/routing.md). Common tasks select one canonical suite directly; unmatched specialist tasks return a bounded Finder query, never an automatic activation. See [workflow checks](docs/workflows.md) for scope/secrets preflight, test receipts, completion gates, and explicit risky-operation approval.

```
                       User Prompt / Goal
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │ TIER 1: The Fast-Path Master Suites (~80%)   │
        │ Instant 0-hop resolution for daily dev loop.  │
        │ Pre-indexed in AGENTS.md / system prompt.    │
        └──────────────────────┬───────────────────────┘
                               │
               Is it a standard dev loop task?
               ├── YES ──► Directly invoke Master Suite:
               │           • Engineering: systematic-debugging-suite, unit-testing-suite,
               │             code-review-standards-suite, git-workflow-suite
               │           • Infrastructure: docker-containers-suite, kubernetes-k8s-suite,
               │             terraform-iac-suite
               │           • Automation: browser-automation-suite, web-scraping-suite,
               │             office-documents-suite
               │           • UI & Design: ui-design-systems-suite, ux-accessibility-suite,
               │             figma-design-prototyping-suite, frontend-webapp-design-suite,
               │             mobile-native-ui-suite, creative-3d-motion-suite,
               │             landing-page-cro-suite, ai-generative-ui-suite
               │
               └── NO (Specialized Domain / Niche Tool)
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │ TIER 2: Just-In-Time MCP Finder (~18%)       │
        │ Call `local-capability-finder` search.        │
        │ Searches 8,700+ skills in <50ms.             │
        │ Injects exact SKILL.md (<500 tokens).        │
        └──────────────────────┬───────────────────────┘
                               │
               Did Tier 2 find a local match?
               ├── YES ──► Load exact target SKILL.md
               └── NO  ──► Drop to Tier 3
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │ TIER 3: Ecosystem Fallback (`npx skills`)    │
        │ Search public community registry if local is │
        │ completely missing a brand new tool.         │
        └──────────────────────────────────────────────┘
```

---

## 📦 The 18 Master Mega-Skills (Suites)

### Core Engineering & Automation
| Master Suite | Replaces / Unifies | Purpose & Key Flow |
|---|---|---|
| **`systematic-debugging-suite`** | `debugging`, `diagnosing-bugs`, `phase-gated-debugging`, `debugger` | Enforces the strict 4-phase diagnosis loop (**Reproduce → Isolate → Root Cause → Fix**). Forbids speculative patching. |
| **`unit-testing-suite`** | `pytest`, `vitest`, `jest`, `junit-5`, `cucumber` | Language-specific routing matrix with AAA patterns, table-driven test cases, and behavioral assertions over implementation mocks. |
| **`code-review-standards-suite`** | `code-review`, `clean-code`, `uncle-bob-craft`, `brooks-review` | 4-pillar review: Functional Correctness, Clean Code / SOLID design, Architectural coupling smells, and AI slop detection. |
| **`git-workflow-suite`** | `git-workflow`, `pr-writer`, `caveman-commit`, `unslop-commit` | Conventional commits, unslop/caveman formatting, 3-way conflict resolution, and reviewer-friendly PR generation. |
| **`web-scraping-suite`** | `firecrawl`, `firecrawl-crawl`, `firecrawl-agent`, `apify`, `skyvern` | Clean markdown for single URLs (`firecrawl`), recursive crawls, social platforms (`apify`), and behind-login (`skyvern`). |
| **`browser-automation-suite`** | `playwright`, `cypress`, `puppeteer`, `selenium`, `agent-browser` | Headless navigation, semantic locator testing (`getByRole`), visual regression, and agent loops (`@e1` refs). |
| **`docker-containers-suite`** | `docker-expert`, `dockerfile-generator`, `docker-compose`, `container-hardening` | Multi-stage caching, distroless minimal runners, non-root users, security hardening, and Docker Compose orchestration. |
| **`kubernetes-k8s-suite`** | `kubernetes-ops`, `k8s-debug`, `helm-generator`, `k8s-manifests` | Pod diagnostics (`CrashLoopBackOff`, `OOMKilled`, `Pending`), Helm chart authoring, and production manifest skeletons. |
| **`terraform-iac-suite`** | `terraform-engineer`, `terragrunt-generator`, `opentofu-migration` | Multi-cloud IaC with remote state locking, provider constraints, Terragrunt DRY layouts, and OpenTofu compatibility. |
| **`office-documents-suite`** | `pdf`, `docx`, `xlsx`, `spreadsheets` | Format-accurate document engines: PDF parsing/tables (`pdfplumber`/`reportlab`), Word XML editing (`docx`), and Excel formula models (`openpyxl`). |

### UI/UX, Frontend & Creative Design
| Master Suite | Replaces / Unifies | Purpose & Key Flow |
|---|---|---|
| **`ui-design-systems-suite`** | `design-system`, `shadcn`, `tailwind`, `bento-ui`, `glassmorphism`, `anti-ui-slop`, `impeccable` | Complete design tokens architecture, style archetypes (Bento, Glass, Neobrutalism, Minimalist, Dark), component library standards, and anti-slop visual invariants. |
| **`ux-accessibility-suite`** | `accessibility-compliance`, `wcag`, `accesslint`, `ux-audit`, `ux-flow`, `uxui-principles` | Usability heuristics (Nielsen 10, 168 cognitive laws), mandatory 4-state lifecycle (Loading, Empty, Error, Success), and strict WCAG 2.2 AA/AAA compliance. |
| **`figma-design-prototyping-suite`** | `figma`, `figma-design-to-code`, `figma-code-connect`, `figma-use`, `wireframe-sketch` | Programmatic Figma MCP automation, bidirectional design-to-code translation, `.figma.tsx` Code Connect mappings, and design token synchronization. |
| **`mobile-native-ui-suite`** | `apple-hig`, `swiftui-design`, `android-jetpack-compose-expert`, `expo-ui`, `react-native-design` | Native mobile UI across iOS (Apple HIG, SwiftUI Liquid Glass), Android (Material Design 3, Jetpack Compose), and Universal Cross-Platform (Expo Router, NativeWind). |
| **`creative-3d-motion-suite`** | `threejs`, `3d-web-experience`, `spline-3d-integration`, `gsap-scrolltrigger`, `emil-design-eng` | Interactive 3D WebGL scenes (Three.js), custom GLSL shaders, Spline integration, GSAP ScrollTrigger timeline choreography, and spring micro-interactions. |
| **`frontend-webapp-design-suite`** | `frontend-developer`, `react-ui-patterns`, `react-best-practices`, `vue-expert`, `sveltekit` | Server vs Client component boundaries (Next.js RSC), fluid responsive layouts, container queries, and Core Web Vitals performance optimization. |
| **`landing-page-cro-suite`** | `landing-page-generator`, `website-builder`, `page-cro`, `signup-flow-cro`, `onboarding-cro` | High-converting landing page architecture (PAS/AIDA), frictionless signup and onboarding UX, transparent pricing tables, and paywall upgrade flows. |
| **`ai-generative-ui-suite`** | `stitch-ui-design`, `autoclaw-design-capability`, `design-lab`, `vibe-code-cleanup`, `unship` | Prompt engineering for UI generative models (Stitch, AutoClaw), Design Lab multi-variant testing, and turning vibe-coded prototypes into production code. |

---

## 💰 4-Layer Token-Saving Architecture

These are workflow recommendations, not measured guarantees. No reproducible provider-accounted benchmark is currently included; see [the current-state baseline](docs/current-state.md).

1. **Layer 1: Input & Tool Gating (`low-token-bilgu` / `ponytail`)**
   - Search exact symbols before opening files.
   - Line-range reading enforced for files >150 lines (using `offset`/`limit`).
   - Minimal surgical edits with `edit` rather than whole-file rewrites.
2. **Layer 2: Subagent Context Isolation (`cavecrew`)**
   - Heavy exploration spanning >5 files runs in isolated child subagents.
   - Only compact findings (`path:line`) return to the main thread, keeping 20+ file reads out of memory.
3. **Layer 3: Output Prose Compression (`caveman` / `sharp-coder`)**
   - Eliminates conversational filler, throat-clearing, and prompt repeating.
   - Switchable to `/caveman ultra` or `/chisle` for instant telegram-terse responses under tight budgets.
4. **Layer 4: Context Compaction (`context-compression`)**
   - Checkpoints state into disk artifacts (`.planning/STATE.md` or git commits) on marathons >15 turns.
   - Structured compaction triggers before crossing 50% context window capacity.

---

## 🚀 Quickstart & Installation

### Option 1: Universal Installer (Python)
Clone this repository and run the installer:

```bash
git clone https://github.com/BlguunBN/agentic-engineering-stack.git
cd agentic-engineering-stack
python install.py --dry-run
python install.py
```

Without `--skills`, the standalone fallback installs only the four core suites into detected configured roots, rather than all 18. Existing unrelated destinations are never overwritten. Use `--skills <suite>...` for an explicit subset. Finder remains the intended discovery and lifecycle owner; this fallback does not register sources with Finder. Configured host paths are not verified against host versions; review `install.py` and the [compatibility baseline](docs/compatibility.md) before installing.

### Option 2: Selective Agent Installation
To install only for specific agents:
```bash
python install.py --agents claude codex pi --skills systematic-debugging-suite unit-testing-suite
```

### Option 3: Manual Integration
Copy `templates/AGENTS.md` into your project root as `AGENTS.md` (or `AGENTS.local.md`) and copy only task-relevant suite folders into your agent's skills directory.

The versioned [`stack.manifest.json`](stack.manifest.json) lists all 18 canonical IDs. The six JSON profiles in `profiles/` describe routing defaults; they do not instruct agents to preload every tagged suite. The standalone installer is intentionally a limited fallback and does not provide update/remove/rollback ownership. Use Finder for managed lifecycle operations once its public integration contract is available.

---

## 📜 License
MIT License. See [LICENSE](LICENSE).
