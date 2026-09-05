// @ts-check
const { test, expect } = require('@playwright/test');

// Dynamic controls (/dynamic_controls): remove/add + enable/disable flows,
// mixing explicit waits, polling waits, and locator variety.
// NOTE: the-internet.herokuapp.com has no data-testid attributes, so the
// playwright config sets testIdAttribute: 'id' and getByTestId targets ids —
// documented here as the standard workaround for legacy sites.
test.describe('Dynamic controls', () => {
  test('checkbox can be removed and added back (explicit waits)', async ({ page }) => {
    await page.goto('/dynamic_controls');
    const checkbox = page.locator('#checkbox input[type="checkbox"]');
    await expect(checkbox).toBeVisible();

    await page.getByRole('button', { name: 'Remove' }).click();
    await checkbox.waitFor({ state: 'detached', timeout: 15000 });
    await expect(page.locator('#message')).toHaveText("It's gone!");

    await page.getByRole('button', { name: 'Add' }).click();
    // Re-added markup differs (input may BE #checkbox); accept either shape.
    const back = page.locator('#checkbox input[type="checkbox"], input#checkbox');
    await back.waitFor({ state: 'attached', timeout: 15000 });
    await expect(page.locator('#message')).toHaveText("It's back!");
  });

  test('text input enables after clicking Enable (expect.poll on editable)', async ({ page }) => {
    await page.goto('/dynamic_controls');
    const input = page.locator('#input-example input[type="text"]');
    await expect(input).toBeDisabled();
    await page.getByRole('button', { name: 'Enable' }).click();
    await expect
      .poll(async () => input.isEditable(), { timeout: 15000 })
      .toBe(true);
    await expect(page.locator('#message')).toHaveText("It's enabled!");
    await input.fill('hello he');
    await expect(input).toHaveValue('hello he');
  });

  test('getByTestId via testIdAttribute=id workaround', async ({ page }) => {
    await page.goto('/dynamic_controls');
    // testIdAttribute is set to "id" in playwright.config.js.
    await expect(page.getByTestId('checkbox-example')).toBeVisible();
    await expect(page.getByTestId('input-example')).toBeVisible();
  });
});
