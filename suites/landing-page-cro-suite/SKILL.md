---
name: landing-page-cro-suite
description: "Master unified Landing Page & Conversion Rate Optimization (CRO) suite. Integrates high-converting SaaS landing page architectures (AIDA/PAS), frictionless signup and onboarding UX, pricing tables, form optimization, and upgrade paywall flows."
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

```tsx
export function PricingCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto items-stretch">
      {/* Tier 1: Starter */}
      <div className="rounded-2xl p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">Starter</h3>
          <p className="text-sm text-slate-500 mt-1">For individuals and experiments</p>
          <div className="mt-6 flex items-baseline">
            <span className="text-4xl font-extrabold text-slate-900 dark:text-white">$0</span>
            <span className="text-sm text-slate-500 ml-1">/month</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-slate-600 dark:text-slate-300">
            <li className="flex items-center gap-2">✓ Up to 3 projects</li>
            <li className="flex items-center gap-2">✓ Community support</li>
          </ul>
        </div>
        <button className="mt-8 w-full py-3 rounded-xl border border-slate-300 dark:border-slate-700 font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800">
          Get Started
        </button>
      </div>

      {/* Tier 2: Pro (Highlighted) */}
      <div className="rounded-2xl p-8 bg-slate-900 text-white dark:bg-blue-950 border-2 border-blue-500 relative shadow-2xl flex flex-col justify-between scale-105 z-10">
        <span className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-blue-500 text-white text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full shadow">
          Most Popular
        </span>
        <div>
          <h3 className="text-xl font-bold">Professional</h3>
          <p className="text-sm text-slate-400 mt-1">For growing teams and businesses</p>
          <div className="mt-6 flex items-baseline">
            <span className="text-4xl font-extrabold">$29</span>
            <span className="text-sm text-slate-400 ml-1">/month</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-slate-300">
            <li className="flex items-center gap-2">✓ Unlimited projects</li>
            <li className="flex items-center gap-2">✓ Advanced analytics & exports</li>
            <li className="flex items-center gap-2">✓ Priority 24/7 support</li>
          </ul>
        </div>
        <button className="mt-8 w-full py-3 rounded-xl bg-blue-500 hover:bg-blue-600 font-semibold text-white shadow-lg shadow-blue-500/25">
          Start 14-Day Free Trial
        </button>
      </div>

      {/* Tier 3: Enterprise */}
      <div className="rounded-2xl p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">Enterprise</h3>
          <p className="text-sm text-slate-500 mt-1">For organizations requiring compliance</p>
          <div className="mt-6 flex items-baseline">
            <span className="text-4xl font-extrabold text-slate-900 dark:text-white">Custom</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-slate-600 dark:text-slate-300">
            <li className="flex items-center gap-2">✓ Dedicated account manager</li>
            <li className="flex items-center gap-2">✓ Custom SLAs & SSO/SAML</li>
          </ul>
        </div>
        <button className="mt-8 w-full py-3 rounded-xl border border-slate-300 dark:border-slate-700 font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800">
          Contact Sales
        </button>
      </div>
    </div>
  );
}
```

---

## 4. CRO Quality Gate

- [ ] Clear value proposition readable within 5 seconds without scrolling.
- [ ] No generic stock illustrations; UI screenshot or interactive preview front-and-center.
- [ ] Signup form asks only for minimum viable fields (Email + Password or OAuth).
- [ ] Friction-free cancellation and security guarantees stated near conversion triggers.
