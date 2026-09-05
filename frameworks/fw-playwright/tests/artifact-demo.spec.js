// @ts-check
const { test, expect } = require('@playwright/test');

// DELIBERATE FAILURE — this is the one intentional red test of the suite.
// It exists to demonstrate failure screenshots + junit failure reporting +
// artifact upload on the HyperExecute UI. Everything else must pass.
test.describe('Artifact demo', () => {
  test('DELIBERATE-FAILURE: captures screenshot on wrong heading assertion', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('h2')).toHaveText('This heading does not exist');
  });
});
