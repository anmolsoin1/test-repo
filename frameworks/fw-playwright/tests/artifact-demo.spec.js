// @ts-check
const { test, expect } = require('@playwright/test');

// Intentionally failing test: demonstrates failure screenshots + junit failure
// reporting + artifact upload on the HyperExecute UI.
test.describe('Artifact demo', () => {
  test('deliberate failure captures screenshot', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('h2')).toHaveText('This heading does not exist');
  });
});
