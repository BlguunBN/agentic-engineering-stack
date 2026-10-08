# AGENTS.md Template for Agentic Engineering Stack
# Copy or append this to your workspace root (AGENTS.md / AGENTS.local.md / CLAUDE.md)

# Core Agent Rules
1. Work only on the requested task.
2. Inspect the minimum necessary files.
3. Prefer targeted search over broad repository reads.
4. Delegate independent bounded tasks to fresh subagents.
5. Use surgical edits with minimal diffs. Never rewrite entire files.
6. Run targeted tests before full test suites.
7. Keep responses concise and lead with findings.
8. Store durable project knowledge in files, not conversation history.

## 3-Tier Routing Architecture (Fast-Path Master Suites + JIT Specialist)

### Tier 1: Fast-Path Master Suites (Zero-Hop Direct Loading)
For standard daily engineering workflows, do not search or guess. Load and follow the Master Suite directly:
- **Bug Diagnosis & Errors**: Load `systematic-debugging-suite` (4-phase Reproduce -> Isolate -> Root Cause -> Fix; no speculative patching).
- **Writing Tests & TDD**: Load `unit-testing-suite` (routes Pytest / Vitest / Jest / JUnit 5 / Cucumber with table-driven tests & AAA pattern).
- **Code Review & Audits**: Load `code-review-standards-suite` (4 pillars: Functional Correctness, Clean Code/SOLID, Brooks Architecture, Security).
- **Git & Pull Requests**: Load `git-workflow-suite` (conventional commits, unslop/caveman formatting, conflict resolution, reviewer-friendly PR summaries).
- **Web Scraping & Data Extraction**: Load `web-scraping-suite` (routes Firecrawl for SPAs/crawls, Apify for social platforms, Skyvern behind-login).
- **Browser Automation & E2E**: Load `browser-automation-suite` (Playwright semantic locators, Cypress, Agent-Browser compact loops).
- **Docker & Containers**: Load `docker-containers-suite` (multi-stage builds, distroless minimal images, non-root users, compose healthchecks).
- **Kubernetes (K8s)**: Load `kubernetes-k8s-suite` (pod troubleshooting CrashLoopBackOff/OOMKilled, Helm charts, production manifest skeletons).
- **Terraform & Infrastructure**: Load `terraform-iac-suite` (multi-cloud remote state locking, Terragrunt DRY patterns, OpenTofu migration).
- **Office Documents**: Load `office-documents-suite` (PDF parsing/forms/OCR, Word `.docx` XML manipulation, Excel `.xlsx` formula models).
- **UI Design Systems**: Load `ui-design-systems-suite` (tokens architecture, Bento/Glass/Neobrutalism/Dark styles, anti-slop visual invariants).
- **UX & Accessibility**: Load `ux-accessibility-suite` (Nielsen 10, 4-state lifecycle, WCAG 2.2 AA/AAA compliance).
- **Figma & Prototyping**: Load `figma-design-prototyping-suite` (Figma MCP automation, design-to-code, Code Connect mappings).
- **Mobile Native UI**: Load `mobile-native-ui-suite` (iOS Apple HIG/SwiftUI, Android M3/Compose, Expo Router/NativeWind).
- **3D & Motion**: Load `creative-3d-motion-suite` (Three.js WebGL, GLSL shaders, Spline, GSAP ScrollTrigger).
- **Frontend Web Apps**: Load `frontend-webapp-design-suite` (Next.js RSC boundaries, container queries, Core Web Vitals).
- **Landing Pages & CRO**: Load `landing-page-cro-suite` (PAS/AIDA landing page architecture, onboarding UX, pricing/paywall flows).
- **Generative UI & Vibe Clean**: Load `ai-generative-ui-suite` (Stitch/AutoClaw prompt engineering, Design Lab multi-variants, prototype unslop).

### Tier 2: Specialized Local Capabilities via MCP (Just-In-Time)
When a task is outside the 18 Master Suites (bioinformatics, CAD/robotics, cloud SDK internals, specialized exploits):
1. Query `search_capabilities` on the local capability finder MCP with a short intent query.
2. Inspect the exact matching skill and read its `SKILL.md` (<500 tokens).
3. Do not search for trivial tasks, and never search twice for the same task in one session.

### Tier 3: Remote Ecosystem Fallback (`npx skills`)
If Tier 2 local search yields zero matches, search external community registries using `npx skills find [query]`.

### Engineering Discipline (Ponytail & GSD)
- **Ponytail Ladder:** Does this need to exist? -> In codebase already? -> Stdlib solves it? -> Native platform covers it? -> Existing dependency? -> One line? -> Minimum code that works.
- **GSD Phases:** Always follow `Spec / Ambiguity Scoring` -> `Plan / Research` -> `Execute / Minimal Diffs` -> `Verify / Proof`.
- **Completion Gate:** Run verification before claiming task success.

## 4-Layer Token-Saving Architecture

To minimize API cost and protect context window limits across complex engineering tasks:

### Layer 1: Input & Tool Gating
- Search exact symbols/filenames (`grep`/`find`) before opening files.
- Line-range reading enforced for files >150 lines (using `offset`/`limit`).
- Minimal surgical edits with `edit`. Never re-write entire files.
- Zero re-reads of unchanged files.

### Layer 2: Subagent Context Isolation
- When a search spans >5 candidate files or requires reading broad documentation, delegate to an isolated subagent.
- The subagent returns only the concise citation (`path:line`) to the main conversation.

### Layer 3: Output Prose Compression
- **Default Style:** Lead with results and code diffs. Eliminate conversational filler (*"Certainly!", "I'd be glad to help..."*), avoid repeating the user's prompt back, and suppress decorative markdown/ASCII banners.
- **Ultra-Efficiency Mode:** When the user requests `/caveman ultra` or `/chisle`, switch to fragment-only speech: drop articles (*a/an/the*), drop filler words, emit one-line answers, and eliminate tool narration.

### Layer 4: Context Compaction
- On tasks spanning >15 turns, checkpoint state into disk artifacts (`.planning/STATE.md` or git commits) instead of keeping multi-turn reasoning logs in context.
- When context capacity crosses 50%, run a structured summary pass to compress turn history while preserving core decisions and active checklists.
