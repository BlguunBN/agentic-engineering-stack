---
name: ui-design-systems-suite
description: "Master unified UI & Design Systems suite. Consolidates design systems (Tailwind v4, shadcn/ui, Radix), token architecture, visual styles (Bento, Glassmorphism, Neobrutalism, Minimalist, Swiss, Dark Mode), and anti-slop visual polish into an end-to-end design foundation."
use_when: "Defining or applying design tokens, component primitives, or a visual system."
avoid_when: "Implementing a one-off screen with no reusable system needs."
entry_inputs: "Existing tokens/components, brand direction, target framework, and constraints."
workflow: "Choose coherent visual direction, define tokens, compose reusable primitives, refine."
verification: "Check contrast, states, responsive behavior, consistency, and implementation fit."
exit_output: "Design-system changes with accessible visual examples."
category: "design-and-ux"
tools:
  - tailwind
  - shadcn
  - radix-ui
---

# UI & Design Systems Suite (Unified Master Skill)

A comprehensive foundation for designing, tokenizing, and crafting modern, distinct, production-grade user interfaces without generic AI design artifacts.

---

## 1. Aesthetic Selection Ladder

Before building any UI component or layout, choose an intentional aesthetic archetype instead of default generic styling:

```
[UI Design Objective]
   │
   ├──> High-density dashboard, analytics, product preview?
   │       └──> BENTO GRID (`bento-ui`)
   │            Asymmetric card layout, subtle 1px borders, muted backgrounds, contextual metrics.
   │
   ├──> Modern macOS / iOS look, floating overlays, luxury / modern SaaS?
   │       └──> GLASSMORPHISM (`glassmorphism`)
   │            Translucent background (rgba/hsla), backdrop-blur (12-24px), 1px white highlight border.
   │
   ├──> Developer tools, playful creative products, rebellious SaaS?
   │       └──> NEO-BRUTALISM (`neo-brutalism`)
   │            High-contrast solid borders (2-3px black), hard dropped shadows (no blur: 4px 4px 0px #000), bold vibrant accents.
   │
   ├──> Typography-centric, editorial, deep-read content, luxury minimal?
   │       └──> MINIMALIST / SWISS (`minimalism`, `swiss-design`, `typography-first`)
   │            Strict typographic hierarchy, generous whitespace, monochrome base with one surgical accent, zero visual fluff.
   │
   └──> Professional dark-themed control centers & developer platforms?
           └──> POLISHED DARK MODE (`dark-mode`, `frontend-ui-dark-ts`)
                Layered surface elevation (#0a0a0b → #121214 → #18181b), OKLCH high-gamut accents, contrast-compliant muted text.
```

---

## 2. Token Architecture Blueprint (CSS Variables / Tailwind v4)

Define semantic tokens instead of hardcoded hex values:

```css
:root {
  /* Surface hierarchy */
  --bg-canvas: #ffffff;
  --bg-surface: #f8fafc;
  --bg-card: #ffffff;
  --bg-subtle: #f1f5f9;

  /* Typography */
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --text-inverted: #f8fafc;

  /* Brand & Functional Accents */
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-subtle: #eff6ff;
  --destructive: #ef4444;
  --success: #10b981;

  /* Borders & Separation */
  --border-subtle: rgba(15, 23, 42, 0.08);
  --border-strong: rgba(15, 23, 42, 0.16);

  /* Elevation Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

.dark {
  --bg-canvas: #09090b;
  --bg-surface: #121214;
  --bg-card: #18181b;
  --bg-subtle: #27272a;

  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;
  --text-inverted: #09090b;

  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);
}
```

---

## 3. Style Archetypes: Implementation Recipes

### A. Bento Grid Architecture
- Use CSS Grid with varying column and row spans: `grid-cols-1 md:grid-cols-3 gap-4`.
- Each card has high internal padding (`p-6`), rounded corners (`rounded-2xl`), and subtle borders (`border border-border-subtle bg-bg-card`).
- Emphasize visual rhythm: 1 Hero card (2x2), 2 secondary cards (1x2), and supporting metric chips.

### B. Glassmorphism Recipe
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.06);
}
.dark .glass-panel {
  background: rgba(24, 24, 27, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
}
```

### C. Neo-Brutalism Recipe
```css
.neo-card {
  background: #ffffff;
  border: 3px solid #000000;
  box-shadow: 5px 5px 0px 0px #000000;
  border-radius: 8px;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.neo-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 7px 7px 0px 0px #000000;
}
```

---

## 4. Component Architecture with shadcn/ui & Radix

When building or reviewing component libraries:
1. **Headless Primitive First:** Use Radix UI primitives (`@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-popover`) for accessible keyboard navigation, ARIA attributes, and focus trapping.
2. **Compound Component Pattern:** Prefer composable subcomponents over massive prop bundles:
   ```tsx
   <Card>
     <CardHeader>
       <CardTitle>Usage Metrics</CardTitle>
       <CardDescription>Real-time compute overview</CardDescription>
     </CardHeader>
     <CardContent>...</CardContent>
     <CardFooter>...</CardFooter>
   </Card>
   ```
3. **Variants via `class-variance-authority` (cva):** Manage state variations cleanly with type-safe `cva` definitions.

---

## 5. Anti-Slop Visual Checklist (`impeccable-polish`)

- [ ] **No Hardcoded Hex Colors:** Every color references semantic CSS variables or Tailwind tokens.
- [ ] **Contrast Verification:** Text-to-background contrast ratio meets minimum 4.5:1 (WCAG AA).
- [ ] **Rhythmic Spacing:** Margin and padding adhere strictly to the 4px/8px grid (4, 8, 12, 16, 24, 32, 48, 64px).
- [ ] **Micro-Elevation Hierarchy:** Modals > Dropdowns/Tooltips > Cards > Canvas background.
- [ ] **Active & Interactive States:** Every button and interactive control defines `:hover`, `:active`, and `:focus-visible` states.
