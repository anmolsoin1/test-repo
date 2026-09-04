// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Dynamic loading', () => {
  test('element rendered after the fact appears', async ({ page }) => {
    await page.goto('/dynamic_loading/2');
    await page.click('#start button');
    await expect(page.locator('#finish h4')).toHaveText('Hello World!', { timeout: 15000 });
  });
});
