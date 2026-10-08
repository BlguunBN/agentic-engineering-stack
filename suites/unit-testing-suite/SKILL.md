---
name: unit-testing-suite
description: "Master unified unit testing suite. Routes across modern test runners (Pytest, Vitest, Jest, JUnit 5, TestNG, Cucumber/BDD). Provides standards for test fixtures, mocking boundaries, table-driven tests, and red-green-refactor TDD cycles."
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

### Pytest (Python)
```python
import pytest
from my_module import calculate_discount

@pytest.mark.parametrize("price, tier, expected", [
    (100.0, "standard", 100.0),
    (100.0, "gold", 80.0),
    (0.0, "gold", 0.0),
])
def test_calculate_discount(price, tier, expected):
    assert calculate_discount(price, tier) == expected
```

### Vitest (TypeScript)
```typescript
import { describe, it, expect } from 'vitest';
import { parseUserRole } from './auth';

describe('parseUserRole', () => {
  it.each([
    ['ADMIN', 'admin'],
    ['USER', 'user'],
    ['UNKNOWN', 'guest'],
  ])('maps %s to %s', (input, expected) => {
    expect(parseUserRole(input)).toBe(expected);
  });
});
```
