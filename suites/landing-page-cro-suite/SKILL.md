---
name: landing-page-cro-suite
description: "Master unified Landing Page & Conversion Rate Optimization (CRO) suite. Integrates high-converting SaaS landing page architectures (AIDA/PAS), frictionless signup and onboarding UX, pricing tables, form optimization, and upgrade paywall flows."
use_when: "Designing a landing page, signup, onboarding, pricing, or conversion flow."
avoid_when: "Implementing a general product screen unrelated to conversion goals."
entry_inputs: "Audience, product value, conversion goal, constraints, and available evidence."
workflow: "Clarify funnel goal, reduce friction, implement states, evaluate accessibility and usability."
verification: "Check responsive flow, form errors, keyboard use, and analytics/event assumptions."
exit_output: "Conversion-focused UI changes and evidence; do not claim lift without measurement."
category: "business-and-marketing"
tools:
  - cro
  - landing-page-generator
---

# Landing Page & CRO Suite (Unified Master Skill)

A battle-tested framework for building high-converting landing pages, optimizing signup funnels, increasing trial-to-paid conversions, and removing friction from checkout flows.

---

## 1. Funnel Optimization Ladder

```
[Conversion Optimization Objective]
   │
   ├──> Building a new SaaS landing page from scratch?
   │       └──> High-Conversion Page Architecture (Section 2: Hero → Proof → Demo → Pricing → FAQ).
   │
   ├──> High drop-off during user registration?
   │       └──> Frictionless Signup Flow (`signup-flow-cro`)
   │            One-click OAuth (Google/GitHub), inline email validation, deferred profile setup.
   │
   ├──> Low user activation after signup?
   │       └──> First-Run Activation UX (`onboarding-cro`)
   │            Progress bar, clear "Aha!" moment checklist, pre-populated templates.
   │
   ├──> Users bouncing on lead/contact forms?
   │       └──> Form CRO Protocol (`form-cro`)
   │            Single-column layout, smart defaults, input masking, progressive disclosure.
   │
   └──> Monetization & plan upgrades?
           └──> Pricing & Paywall Architecture (`paywall-upgrade-cro`)
                Clear recommended tier, annual discount toggle, feature comparison table.
```

---

## 2. High-Converting Landing Page Anatomy (PAS / AIDA)

Every landing page must follow a rigorous narrative sequence:

### Section 1: The Hero Header (Above the Fold)
- **Primary Benefit Headline (H1):** Clear, punchy statement of the outcome (not feature list).
- **Sub-headline (H2):** One sentence explaining how it works and who it is for.
- **Dual CTA:** Primary high-intent button ("Start Free Trial" or "Get Started") + Secondary low-friction action ("Watch 2-min Demo").
- **Social Proof Snippet:** "Trusted by 10,000+ developers" or customer avatars.
- **Hero Visual:** High-fidelity interactive UI screenshot, video, or Bento grid preview.

### Section 2: Social Proof & Logos
- Monochrome logo marquee of respected companies or press mentions.

### Section 3: The Problem vs. Solution (Pain-Agitate-Solve)
- Highlight the painful manual workflow before vs. the seamless automated workflow after.

### Section 4: Feature Deep-Dive (Bento Grid)
- Interactive tabs or visual cards showcasing 3–4 core capabilities with realistic data.

### Section 5: Transparent Pricing Table
- Monthly vs. Annual toggle (highlighting "Save 20%").
- Clear visual hierarchy: Center "Pro" tier highlighted with accent badge ("Most Popular").
- Feature checklists with clear tooltips.

### Section 6: FAQ & Objection Handling
- Accordion addressing data security, cancellation policies, setup time, and integrations.

### Section 7: Final Sticky Call-to-Action
- Final focused closing banner with zero distraction.

---

## 3. High-Converting Pricing Table Template

An illustrative React pricing-card example is in [references/pricing-cards.tsx](references/pricing-cards.tsx). Replace its sample tiers and claims with validated product details; do not imply conversion lift without measurement.

---

## 4. CRO Quality Gate

- [ ] Clear value proposition readable within 5 seconds without scrolling.
- [ ] No generic stock illustrations; UI screenshot or interactive preview front-and-center.
- [ ] Signup form asks only for minimum viable fields (Email + Password or OAuth).
- [ ] Friction-free cancellation and security guarantees stated near conversion triggers.
