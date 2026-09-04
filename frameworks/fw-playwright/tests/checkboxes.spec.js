// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Checkboxes @smoke', () => {
  test('checkbox toggles state @smoke', async ({ page }) => {
    await page.goto('/checkboxes');
    const boxes = page.locator('#checkboxes input');
    const first = boxes.nth(0);
    const second = boxes.nth(1);
    await expect(first).not.toBeChecked();
    await first.check();
    await expect(first).toBeChecked();
    await second.uncheck();
    await expect(second).not.toBeChecked();
  });
});
