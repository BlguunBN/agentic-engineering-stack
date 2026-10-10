# Playwright Login-Flow Example

Keep credentials test-only and configure a deterministic local or test environment.

```typescript
import { test, expect } from '@playwright/test';

test('login flow verifies user dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('secret');
  await page.getByRole('button', { name: 'Sign in' }).click();

  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible();
});
```
