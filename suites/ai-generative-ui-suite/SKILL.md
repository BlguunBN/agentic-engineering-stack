---
name: ai-generative-ui-suite
description: "Master unified AI Generative UI & Vibe-Coding Refinement suite. Integrates Google Stitch prompt engineering, autonomous AutoClaw design pipelines, Design Lab multi-variant testing, vibe-code production cleanup, and infinite canvas deliverables."
category: "ai-agents-and-ml"
tools:
  - stitch
  - autoclaw
  - design-lab
---

# AI Generative UI & Refinement Suite (Unified Master Skill)

A comprehensive toolkit for prompting generative UI models (Google Stitch, AutoClaw), generating multi-variant design testbeds, converting rapidly "vibe-coded" prototypes into production code, and delivering interactive design systems.

---

## 1. Generative UI Workflow Ladder

```
[AI Design & Prototyping Task]
   │
   ├──> Crafting high-fidelity UI prompts for Stitch or AutoClaw?
   │       └──> Prompt Structuring Architecture (Section 2: Domain, Tokens, Archetype, Components).
   │
   ├──> Exploring 3–5 distinct visual directions before building?
   │       └──> Design Lab Exploration (`design-lab`)
   │            Spin up a temporary testbed with 5 styled variations (A/B/C/D/E) for user selection.
   │
   ├──> Reviewing or cleaning up a rapidly generated "vibe-coded" app?
   │       └──> Vibe-Code Hardening Pipeline (`vibe-code-cleanup`, `vibe-code-auditor`)
   │            Strip hallucinated imports, replace mock APIs with real contracts, normalize CSS tokens.
   │
   └──> Delivering comprehensive design deliverables to stakeholders?
           └──> Infinite Canvas Delivery (`infinite-canvas-output`)
                Single-file HTML with 3 layers: Project Brief, Design System tokens, and Interactive Prototype.
```

---

## 2. Generative UI Prompting Architecture (Stitch & AutoClaw)

Generative AI models produce generic "slop" when prompts lack structural constraints. Always structure generative UI prompts with these 5 mandatory anchors:

1. **Aesthetic Archetype:** Explicitly declare the aesthetic (e.g. "Linear-style dark Bento grid", "Warm editorial minimalist", "Chunky neo-brutalist").
2. **Color Science & Gamut:** Specify background elevation steps and high-gamut accent hex codes (e.g. `Canvas: #09090b, Surface: #18181b, Accent: OKLCH vibrant electric indigo`).
3. **Typography DNA:** Name real typeface pairings (e.g. `Display: Syne / Plus Jakarta Sans, Body: Inter`).
4. **Concrete Component Manifest:** List exact component states and realistic domain data (never "Lorem Ipsum" or "User 1").
5. **Micro-details:** Specify borders (`1px solid rgba(255,255,255,0.08)`), blur filters, and subtle shadows.

---

## 3. Vibe-Code Production Hardening Pipeline

When refactoring AI-generated prototypes (`vibe-code-cleanup`):

### Step 1: Dependency & Scaffolding Pruning
- Remove unused icons, dead imports, and redundant wrapper `<div>`s.
- Eliminate duplicated styles or inline Tailwind overrides that contradict the design system.

### Step 2: Component Decoupling
- Extract massive 800-line single-file components into modular atomic units (`MetricCard`, `UserRow`, `FilterPill`).

### Step 3: Real State & Data Boundaries
- Replace hardcoded fake timers (`setTimeout`) with proper query hooks (`useQuery`, `fetch`).
- Provide fallback skeletons and real error boundaries.

---

## 4. Design Lab Multi-Variant Testing Protocol (`design-lab`)

When a user or team is undecided on visual direction:
1. Generate **Variant A (Conservative / Enterprise):** Clean, spacious, high readability, subtle slate blues.
2. Generate **Variant B (Modern Bento / Dark):** High contrast, dark mode elevation, glowing border highlights.
3. Generate **Variant C (Editorial / Minimal):** Monochromatic, serif or high-character typography, generous margins.
4. Compare all variants side-by-side in a single navigable preview before committing to code.

---

## 5. Verification Checklist

- [ ] Generative prompts produce zero generic purple gradients or AI-hallucinated icons.
- [ ] Vibe-coded components verified to compile with 0 TypeScript/ESLint warnings.
- [ ] No hardcoded mock objects left in production component trees.
- [ ] Deliverable includes exported `DESIGN.md` documenting visual choices.
