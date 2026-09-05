// @ts-check
const { test, expect } = require('@playwright/test');

// Checkbox page with mixed locator strategies per test.
test.describe('Checkboxes @smoke', () => {
  test('checkbox toggles state (css + nth)', async ({ page }) => {
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

  test('both checkboxes found via getByRole', async ({ page }) => {
    await page.goto('/checkboxes');
    const boxes = page.getByRole('checkbox');
    await expect(boxes).toHaveCount(2);
    await boxes.first().check();
    await expect(boxes.first()).toBeChecked();
  });

  test('checkbox toggle via xpath locator', async ({ page }) => {
    await page.goto('/checkboxes');
    const second = page.locator('xpath=//form[@id="checkboxes"]/input[2]');
    await expect(second).toBeChecked(); // second box is checked by default
    await second.uncheck();
    await expect(second).not.toBeChecked();
  });
});
