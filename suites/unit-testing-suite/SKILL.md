---
name: unit-testing-suite
description: "Master unified unit testing suite. Routes across modern test runners (Pytest, Vitest, Jest, JUnit 5, TestNG, Cucumber/BDD). Provides standards for test fixtures, mocking boundaries, table-driven tests, and red-green-refactor TDD cycles."
use_when: "Writing or changing unit, integration, or regression tests."
avoid_when: "Reviewing code without test-writing scope or replacing project test conventions."
entry_inputs: "Behavior contract, test runner, existing fixtures, and edge cases."
workflow: "Choose native runner, write behavior-level tests, isolate inputs, iterate red-green-refactor."
verification: "Run focused tests and confirm assertions detect the intended behavior."
exit_output: "Focused test changes and exact command/result."
category: "software-engineering"
---

# Unit Testing Suite (Unified Master Skill)

A comprehensive guide for generating, structuring, and running high-confidence unit and integration tests.

## 1. Framework Routing Matrix

```
[Need to write or fix unit tests]
   |
   +---> Python project?
   |        └──> Use `pytest-skill` (fixtures, `@pytest.mark.parametrize`, `conftest.py`).
   |
   +---> Modern JS/TS project (Vite / Next.js / Nuxt)?
   |        └──> Use `vitest-skill` (fast, native ESM, Jest-compatible API).
   |
   +---> Classic Node/React project (Create-React-App, older setups)?
   |        └──> Use `jest-skill` (standard mocks, snapshot testing).
   |
   +---> Java / Spring Boot project?
   |        └──> Use `junit-5-skill` (`@ParameterizedTest`, Mockito, AssertJ).
   |
   +---> Non-technical stakeholder BDD requirements?
            └──> Use `cucumber-skill` (Gherkin Feature/Scenario/Given-When-Then).
```

## 2. Universal Testing Invariants (Ponytail & Clean Code)

1. **Test Behavior, Not Implementation:** Test public interfaces, inputs, and outputs. Do not test private variables or internal call counts unless mocking external side-effects.
2. **Deterministic & Isolated:** Tests must never depend on execution order or live network calls. Use factories and in-memory test doubles.
3. **AAA Pattern:** Every test must clearly separate **Arrange**, **Act**, and **Assert**.
4. **Table-Driven / Parameterized:** Instead of writing 10 repetitive test functions, write 1 parameterized test covering edge cases (empty string, boundary numbers, nulls, special characters).

## 3. Quick Reference Templates

Framework-specific Pytest and Vitest examples are available in [references/pytest-vitest.md](references/pytest-vitest.md). Use project-native fixtures and assert observable behavior.
