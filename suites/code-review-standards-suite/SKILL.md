---
name: code-review-standards-suite
description: "Master unified code review and standards suite. Integrates general code review, Uncle Bob's Clean Code (SOLID/DRY), Fred Brooks architectural smell analysis (coupling/decay), and AI slop detection into a multi-pillar review protocol."
use_when: "Reviewing a proposed diff for correctness, security, maintainability, or architecture."
avoid_when: "Implementing a change without a review request or reviewable diff."
entry_inputs: "Diff, relevant surrounding code, intended behavior, and test evidence."
workflow: "Inspect context, check correctness and risks, prioritize evidence-backed findings."
verification: "Validate each finding against code and tests; avoid speculative issues."
exit_output: "Severity-ranked findings with file/line evidence, or no findings."
category: "software-engineering"
---

# Code Review & Standards Suite (Unified Master Skill)

A comprehensive code review framework combining correctness, clean code design, architectural integrity, and security.

## 1. Multi-Pillar Review Framework

When reviewing any diff or PR, evaluate across 4 distinct pillars:

### Pillar 1: Correctness & Logic (`code-review`)
- Does the code fulfill the functional requirement without side effects?
- Are boundary conditions, null/undefined states, and error paths handled?
- Are there unhandled async rejections or resource leaks?

### Pillar 2: Clean Code & Simplicity (`clean-code` & `ponytail`)
- **YAGNI / Ponytail Check:** Is there speculative abstraction, unnecessary interfaces, or premature generalization?
- **DRY & Single Responsibility:** Does each function or component do exactly one thing?
- **Naming & Intent:** Are variable and function names descriptive, unambiguous, and intention-revealing?

### Pillar 3: Architectural Health (`brooks-review`)
- **Coupling & Cohesion:** Does this change create hidden cross-module dependencies?
- **Module Seams:** Does new business logic belong in domain services rather than controllers/UI?
- **Technical Debt:** Will this change increase maintenance friction for future developers?

### Pillar 4: Security & Hygiene (`security-review` & `unslop-review`)
- Input validation, parameterized queries, and safe credential handling.
- Elimination of AI boilerplate / slop comments (e.g. "This function performs X...").

## 2. Review Output Format

Structure all code reviews into a prioritized, actionable checklist:

```markdown
### Code Review Summary

#### 🔴 Critical / Blocker
- `path/to/file.ts:42`: Potential null dereference when `user.profile` is missing.
  - **Remedy:** Guard with optional chaining: `user?.profile?.id`.

#### 🟡 Maintainability & Design (Clean Code)
- `path/to/service.ts:110`: 120-line function mixes DB access and email delivery.
  - **Remedy:** Extract email notification into a separate helper.

#### 🟢 Suggestions & Polish
- `path/to/util.ts:15`: Can use `Array.prototype.find()` instead of manual loop.
```
