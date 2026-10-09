# Pytest and Vitest Patterns

Use the project's existing test runner. These are compact examples; adapt names and assertions to the behavior under test.

## Pytest

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

## Vitest

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
