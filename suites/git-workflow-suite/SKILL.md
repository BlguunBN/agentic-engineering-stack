---
name: git-workflow-suite
description: "Master unified Git and Pull Request suite. Handles branch lifecycle, conventional commit formatting, AI slop removal, merge conflict resolution, and reviewer-ready PR generation."
use_when: "Managing Git changes, resolving conflicts, preparing commits, or writing a pull request."
avoid_when: "A task does not require repository history or collaboration workflow."
entry_inputs: "Working-tree state, intended commit scope, branch/base, and verification evidence."
workflow: "Inspect status and diff, stage scoped files, verify, then summarize the change."
verification: "Review staged paths and commit contents; never stage unrelated user changes."
exit_output: "Scoped commit/PR summary and exact verification results."
category: "software-engineering"
tools:
  - git
  - gh
---

# Git Workflow & Pull Request Suite (Unified Master Skill)

A streamlined workflow for Git operations, commit discipline, and pull request delivery.

## 1. End-to-End Workflow Flowchart (GSD & Ponytail)

```
[New Feature / Bugfix]
   │
   ▼
[1. Branch Creation] ──> feature/<issue-id>-<short-description>
   │
   ▼
[2. Surgical Commits] ──> Conventional commits (<50 chars, no AI slop buzzwords)
   │
   ▼
[3. Conflict Check]   ──> Rebase cleanly onto target branch (`git fetch && git rebase origin/main`)
   │
   ▼
[4. PR Generation]    ──> Run `pr-writer` to generate structured, reviewer-friendly PR summary
   │
   ▼
[5. Landing Verification] ──> CI green, self-review diff, merge
```

## 2. Commit Message Disciplines

Choose the style matching project preferences:

### Standard Conventional Commits (`git-workflow`)
Format: `<type>(<scope>): <short imperative subject>`
- `feat(auth): add OAuth2 refresh token rotation`
- `fix(parser): handle empty JSON payload on webhook intake`
- `test(billing): add test cases for prorated refunds`

### Unslop Commit (`unslop-commit`)
- **Avoid:** *"Refactor codebase to seamlessly enhance and optimize robust error-handling infrastructure"*
- **Write:** *"fix: retry transient 503 errors on payment gateway"*

### Caveman / Token-Saving Mode (`caveman-commit`)
- Under constrained token environments, emit ultra-compact, informative lines:
  `fix(db): prevent null connection leak on pool timeout`

## 3. Pull Request Template (`pr-writer`)

When opening or updating a PR:
```markdown
## Summary
Brief 1-2 sentence description of what changed and why.

## Changes
- Concise list of key modifications.

## Verification
- [x] Unit tests passing (`npm test` / `pytest`)
- [x] Tested locally against reproduction scenario
```
