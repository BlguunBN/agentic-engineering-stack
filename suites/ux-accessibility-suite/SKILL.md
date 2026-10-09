---
name: ux-accessibility-suite
description: "Master unified UX & Accessibility suite. Integrates Nielsen's 10 usability heuristics, 168 cognitive UX laws, interaction design, microcopy feedback loops, and WCAG 2.2 AA/AAA accessibility compliance & automated audits."
use_when: "Auditing or implementing usability, semantics, keyboard access, or WCAG requirements."
avoid_when: "Changing visual styling with no user-impact or accessibility scope."
entry_inputs: "User flows, target conformance level, components, assistive-technology needs."
workflow: "Inspect interaction and content, identify barriers, make semantic fixes, re-audit."
verification: "Test keyboard/focus, semantics, contrast, states, and automated checks."
exit_output: "Prioritized issues or fixes with concrete verification evidence."
category: "design-and-ux"
tools:
  - accesslint
  - wcag
---

# UX & Accessibility Suite (Unified Master Skill)

A comprehensive guide for delivering intuitive user experiences, frictionless user flows, and verifiable WCAG 2.2 accessibility compliance.

---

## 1. UX & Usability Decision Tree

```
[UX Assessment / Flow Design]
   │
   ├──> Auditing an existing UI or reviewing PR changes?
   │       └──> Run the Heuristic & Cognitive Law Audit (Section 2).
   │
   ├──> Designing feedback, state transitions, or microcopy?
   │       └──> Apply Complete State Lifecycle (Loading, Empty, Error, Success).
   │
   ├──> Auditing compliance or preparing for accessibility review?
   │       └──> Execute WCAG 2.2 Protocol (Section 3) & automated lint checks.
   │
   └──> Optimizing keyboard navigation & screen readers?
           └──> Implement ARIA, Focus Traps, and Landmark Roles (Section 4).
```

---

## 2. Core Usability Heuristics & UX Laws

When reviewing or crafting any interaction flow, evaluate against these essential benchmarks:

### A. The 4 Essential UX States
Never leave an interface in an undefined state. Every async or data-dependent component must provide:
1. **Loading State:** Skeleton screens that match the final shape (avoid full-screen blocking spinners).
2. **Empty State:** Clear friendly illustration/icon, explanation of why it's empty, and a primary CTA to create/import data.
3. **Error State:** Human-readable explanation of what went wrong, guidance on how to fix it, and an actionable retry action.
4. **Success State:** Instant visual feedback (optimistic update, checkmark toast, clear confirmation).

### B. Cognitive Ergonomics (`uxui-principles`)
- **Fitts's Law:** Interactive touch targets must be at least **44x44px** (iOS) or **48x48px** (Android/Web), placed within easy reach.
- **Hick's Law:** Break complex decisions into bite-sized steps (progressive disclosure, multi-step wizards) rather than overwhelming forms.
- **Jakob's Law:** Adhere to established platform conventions (logo links to home, top-right avatar for profile/account, bottom navigation for mobile).
- **Peak-End Rule:** Make the final completion step of a task satisfying with clear confirmation.

---

## 3. WCAG 2.2 AA Accessibility Protocol

Ensure all interfaces are perceivable, operable, understandable, and robust:

### A. Color & Contrast Ratios
- **Normal Text (< 18pt / < 14pt bold):** Minimum contrast ratio of **4.5:1** against the background.
- **Large Text (>= 18pt / >= 14pt bold):** Minimum contrast ratio of **3:1**.
- **Interactive UI Components & Borders:** Minimum contrast ratio of **3:1** for active control borders and focus rings.
- **Non-Color Reliance:** Never use color alone to convey meaning (always pair colored error text with an alert icon).

### B. Keyboard Navigation & Focus Management
- **Logical Tab Order:** DOM source order must match visual reading order.
- **Visible Focus Rings:** Never set `outline: none` without providing an alternative focus ring (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- **Modal Focus Trapping:** Dialogs and drawers must trap Tab focus inside the active modal and restore focus to the trigger on close.
- **Escape Key Dismissal:** All overlays, dropdowns, and dialogs must close on `Escape`.

---

## 4. Semantic HTML & ARIA Implementation Reference

```html
<!-- Accessible Form Control with Associated Labels and Error Announcement -->
<div class="form-group">
  <label for="workspace-name" class="font-medium text-sm text-slate-700">
    Workspace Name <span aria-hidden="true" class="text-rose-500">*</span>
  </label>
  <input
    id="workspace-name"
    name="workspaceName"
    type="text"
    required
    aria-required="true"
    aria-invalid="true"
    aria-describedby="workspace-name-error"
    class="border border-rose-500 rounded-lg px-3 py-2 focus-visible:ring-2 focus-visible:ring-rose-500"
  />
  <p id="workspace-name-error" role="alert" class="text-xs text-rose-600 mt-1">
    Workspace name is required and must be unique.
  </p>
</div>

<!-- Accessible Icon-Only Button -->
<button
  type="button"
  aria-label="Close dialog"
  class="p-2 rounded-md hover:bg-slate-100 focus-visible:ring-2 focus-visible:ring-slate-900"
>
  <svg aria-hidden="true" class="w-5 h-5">...</svg>
</button>
```

---

## 5. Pre-Ship UX & A11y Quality Gate

- [ ] Every image contains meaningful `alt` text or `alt=""` if purely decorative.
- [ ] Automated scan with `accesslint` or Axe returns 0 critical or serious violations.
- [ ] The entire flow is navigable using only `Tab`, `Shift+Tab`, `Enter`, and `Space`.
- [ ] Microcopy uses clear, empathetic voice without technical jargon or blame.
- [ ] Screen readers announce dynamic alerts via `aria-live="polite"` or `role="status"`.
