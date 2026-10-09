---
name: browser-automation-suite
description: "Master unified browser automation & E2E testing suite. Consolidates Playwright, Cypress, Puppeteer, Selenium, and Agent-Browser. Provides clear decision trees for headless automation, visual regression, snapshot testing, and cross-browser CI."
use_when: "Automating browser interactions or testing user-visible web flows."
avoid_when: "Testing isolated logic that needs no browser or DOM runtime."
entry_inputs: "App URL, user journey, supported browsers, test environment, and assertions."
workflow: "Select existing browser stack, isolate state, use semantic locators, assert outcomes."
verification: "Run the targeted browser checks and retain failure evidence."
exit_output: "Automation changes and reproducible browser-test results."
category: "software-engineering"
tools:
  - playwright
  - cypress
  - puppeteer
  - selenium
---

# Browser Automation Suite (Unified Master Skill)

A unified guide and control layer for driving browsers, taking screenshots, and running automated end-to-end tests.

## 1. Tool Selection Ladder (Ponytail / YAGNI Principle)

```
[Need browser automation or web test]
   |
   +---> Is this an autonomous AI agent loop exploring/verifying UI?
   |        └──> Use `agent-browser` (compact snapshot references like @e1, @e2).
   |
   +---> Is this automated E2E testing or general scripting?
   |        └──> Use `playwright` (industry standard, fast, multi-tab, network mocking).
   |
   +---> Is the project already committed to Cypress in package.json?
   |        └──> Use `cypress-skill` (runs inside existing Cypress setup).
   |
   +---> Is this an older legacy enterprise codebase with existing Grid?
   |        └──> Use `selenium-skill` or `webdriverio-skill`.
   |
   +---> Is it single-page PDF generation or lightweight Chrome DevTools scripting?
            └──> Use `puppeteer-skill` or Playwright PDF generator.
```

## 2. GSD Execution Flow

- **Phase 1 (Target Verification):** Confirm the app is running locally (e.g. `localhost:3000`) before launching browsers. Never test against a cold server.
- **Phase 2 (Minimal Locators):** Prefer user-facing semantic locators (`getByRole`, `getByText`, `getByLabel`) over fragile CSS/XPath selectors.
- **Phase 3 (Network & State Isolation):** Clear cookies, isolate auth storage, and mock unstable third-party APIs.
- **Phase 4 (Assertion & Evidence):** Every test step must assert an explicit consequence (visible URL change, rendered element, or toast notification). Save screenshots only on failure.

## 3. Best Practices (Playwright First)

Prefer semantic locators and assert a user-visible consequence. A focused login example is in [references/playwright-login.md](references/playwright-login.md). Use test-only credentials and isolated state.
