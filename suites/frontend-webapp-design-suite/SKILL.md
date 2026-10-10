---
name: frontend-webapp-design-suite
description: "Master unified Frontend Web & WebApp Engineering suite. Integrates React Server Components, Next.js App Router UI patterns, Vue 3 Composition patterns, SvelteKit, responsive multi-breakpoint layouts, and production component engineering."
use_when: "Building or changing frontend pages, components, routing, or responsive behavior."
avoid_when: "Working only on backend, infrastructure, or visual concept generation."
entry_inputs: "Framework/version, existing page and components, design target, and user states."
workflow: "Follow project conventions, implement responsive components and states, verify behavior."
verification: "Run relevant tests and inspect accessibility, responsive layout, and performance."
exit_output: "Frontend changes with test and UI verification evidence."
category: "software-engineering"
tools:
  - react
  - nextjs
  - vue
---

# Frontend Web & WebApp Design Suite (Unified Master Skill)

A comprehensive guide for building scalable, responsive, high-performance web applications and component architectures across modern frontend frameworks.

---

## 1. Framework Architecture Ladder

```
[Web Application Feature]
   │
   ├──> React 19 / Next.js 15 App Router?
   │       └──> Server vs Client Boundary Split
   │            Default to Server Components (RSC) for data fetching; isolate interactive widgets with `'use client'`.
   │
   ├──> Vue 3 / Nuxt 3 application?
   │       └──> Composition API & Script Setup (`vue-expert`)
   │            Typed props/emits, reusable composables (`useFetch`, `useAuth`), Pinia reactive stores.
   │
   ├──> Svelte 5 / SvelteKit application?
   │       └──> Runes & Signals (`sveltekit`, `markstream-svelte`)
   │            Fine-grained reactivity (`$state`, `$derived`, `$effect`), zero virtual-DOM overhead.
   │
   └──> Complex Data Grid / Data-Heavy Dashboard?
           └──> Virtualized Rows, Skeleton Loading, Server Pagination
                TanStack Table or virtualized list virtualization to render 10,000+ records seamlessly.
```

---

## 2. Server vs Client Component Architecture (Next.js App Router)

```tsx
// app/dashboard/page.tsx (Server Component - Zero client JS bundle)
import { Suspense } from 'react';
import { MetricsGrid } from '@/components/dashboard/metrics-grid';
import { InteractiveFilterBar } from '@/components/dashboard/filter-bar'; // Client component
import { SkeletonGrid } from '@/components/ui/skeletons';

export default async function DashboardPage() {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          Platform Analytics
        </h1>
        <InteractiveFilterBar />
      </div>

      <Suspense fallback={<SkeletonGrid />}>
        <MetricsGrid />
      </Suspense>
    </main>
  );
}
```

---

## 3. Responsive Layout & Container Queries

1. **Fluid Multi-Breakpoint Design:**
   - Mobile: `sm: 640px` (single column, full-width cards).
   - Tablet: `md: 768px` (2-column grid, compact sidebar/bottom bar).
   - Laptop: `lg: 1024px` (3-column layout, fixed persistent navigation).
   - Ultra-wide: `xl: 1280px` / `2xl: 1536px` (centered container with max-width limits).

2. **Container Queries for Reusable Widgets:**
   Use `@container` queries so components respond to their container width, not the entire browser window:
   ```html
   <div class="@container">
     <div class="flex flex-col @md:flex-row @lg:grid @lg:grid-cols-3 gap-4">
       <!-- Card adapts whether placed in a sidebar or full-width main view -->
     </div>
   </div>
   ```

---

## 4. Web Performance Invariants (Core Web Vitals)

- **Largest Contentful Paint (LCP < 2.5s):** Preload hero images using `<link rel="preload" as="image">`. Use modern formats (`.webp`, `.avif`).
- **Interaction to Next Paint (INP < 200ms):** Debounce heavy search filters (`useDeferredValue` or `useDebounce`). Avoid long tasks on the main thread.
- **Cumulative Layout Shift (CLS < 0.1):** Always set explicit `width` and `height` (or aspect ratios) on images, banners, and video players.

---

## 5. Frontend Quality Gate

- [ ] Zero hydration mismatch warnings in the console.
- [ ] Error boundaries (`error.tsx`) catch child rendering failures gracefully.
- [ ] Responsive navigation verified across 375px (iPhone), 768px (iPad), and 1440px (Desktop).
- [ ] No layout shifts during image or font loading.
