---
name: figma-design-prototyping-suite
description: "Master unified Figma & design-to-code suite. Integrates Figma MCP automation, Code Connect component mapping, bidirectional design translation, tokens extraction, and rapid wireframing."
category: "design-and-ux"
tools:
  - figma
---

# Figma & Prototyping Suite (Unified Master Skill)

A unified workflow for automating Figma, creating design systems, connecting design components to codebases, and converting visual mockups into clean production code.

---

## 1. Figma Workflow Ladder

```
[Figma & Prototyping Task]
   │
   ├──> Reading and converting a Figma design into frontend code?
   │       └──> Design-to-Code Workflow (`figma-design-to-code`)
   │            Extract node context, identify nested auto-layouts, map tokens, generate semantic JSX/CSS.
   │
   ├──> Syncing existing codebase components with Figma UI kit?
   │       └──> Figma Code Connect (`figma-code-connect`, `figma-code-connect-components`)
   │            Author .figma.tsx definitions to link props, variants, and live code snippets.
   │
   ├──> Generating or updating frames, screens, or libraries in Figma via MCP?
   │       └──> Programmatic Figma Authoring (`figma-use`, `figma-generate-design`, `figma-generate-library`)
   │            Use Auto-Layout frames, variables for colors/spacing, and component variant sets.
   │
   └──> Low-fidelity exploration or architecture diagrams?
           └──> FigJam & Diagram Generation (`figma-generate-diagram`, `wireframe-sketch`)
                Flowcharts, ERDs, and user journeys rendered with clean visual hierarchy.
```

---

## 2. Design-to-Code Protocol (`figma-design-to-code`)

When translating any Figma node into React/Vue/HTML:

### Step 1: Deconstruct Auto-Layout & Constraints
- Map horizontal Auto-Layout to `flex flex-row items-... justify-...`.
- Map vertical Auto-Layout to `flex flex-col gap-...`.
- Map Fill Container to `w-full` / `flex-1`.
- Map Hug Contents to `w-auto` / `h-auto`.

### Step 2: Extract & Replace Tokens
- Never output raw hex values like `#1E293B` or arbitary pixels like `14.23px`.
- Match Figma Color Variables to project design tokens (`bg-slate-900`, `text-primary`).
- Match corner radius to token scale (`rounded-lg`, `rounded-2xl`).

### Step 3: Interactive Component Extraction
- Identify interactive elements (buttons, inputs, toggles, dialogs) and map them to the project's component library (`@/components/ui/button`, `@/components/ui/dialog`).

---

## 3. Figma Code Connect Template (`.figma.tsx`)

Map production React components directly to Figma components:

```tsx
import React from 'react';
import figma from '@figma/code-connect';
import { Button } from '@/components/ui/button';

figma.connect(
  Button,
  'https://www.figma.com/design/YOUR_FILE_KEY/Design-System?node-id=123-456',
  {
    props: {
      variant: figma.enum('Variant', {
        Primary: 'default',
        Secondary: 'secondary',
        Destructive: 'destructive',
        Ghost: 'ghost',
      }),
      size: figma.enum('Size', {
        Small: 'sm',
        Medium: 'default',
        Large: 'lg',
      }),
      disabled: figma.boolean('Disabled'),
      label: figma.string('Label'),
    },
    example: ({ variant, size, disabled, label }) => (
      <Button variant={variant} size={size} disabled={disabled}>
        {label}
      </Button>
    ),
  }
);
```

---

## 4. Programmatic Figma Authoring Principles (`figma-use`)

When writing to Figma through MCP or Plugin APIs:
1. **Always Use Auto-Layout:** Set `layoutMode: "VERTICAL"` or `"HORIZONTAL"` for all container frames. Never position layout items with absolute X/Y coordinates unless designing freeform background illustrations.
2. **Bind Variables First:** Create local variable collections for Colors and Spacing before creating components, then bind them using `setBoundVariable()`.
3. **Component Sets for Variants:** Group interactive states (`Default`, `Hover`, `Pressed`, `Disabled`) into a single ComponentSetNode.
4. **Load Fonts Before Text Mutation:** Always call `await figma.loadFontAsync(textNode.fontName)` before modifying `characters`.

---

## 5. Verification Checklist

- [ ] Figma node auto-layout translates cleanly to responsive Flexbox/Grid.
- [ ] Text styles map to standard typography scale (e.g. `text-sm font-medium`).
- [ ] Code Connect definitions validated with `npx figma-connect publish` or local lint.
- [ ] Assets and icons exported as clean, optimized SVGs without inline pixel dimensions.
