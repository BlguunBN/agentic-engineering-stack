# Pricing Cards Example

Illustrative structure only. Replace sample tiers, prices, claims, and styles with validated product data and the project's existing components.

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
