// @ts-check
const { test, expect } = require('@playwright/test');

// Wait-strategy spec: explicit waits (locator.waitFor) and API-based waits
// (page.waitForResponse) against pages built for async-loading demos.
test.describe('Dynamic loading waits', () => {
  test('example 1: hidden element becomes visible (explicit waitFor)', async ({ page }) => {
    await page.goto('/dynamic_loading/1');
    // Element exists in DOM but is hidden; explicit wait for the visible state.
    const finish = page.locator('#finish h4');
    await expect(finish).toHaveText('Hello World!');
    await expect(finish).toBeHidden();
    await page.getByRole('button', { name: 'Start' }).click();
    await finish.waitFor({ state: 'visible', timeout: 15000 });
    await expect(finish).toHaveText('Hello World!');
    // Loading bar disappears once done.
    await page.locator('#loading').waitFor({ state: 'hidden', timeout: 15000 });
  });

  test('example 2: element rendered after the fact (waitFor attached)', async ({ page }) => {
    await page.goto('/dynamic_loading/2');
    // Element does NOT exist in the DOM until the loader finishes.
    const finish = page.locator('#finish h4');
    await expect(finish).toHaveCount(0);
    await page.getByRole('button', { name: 'Start' }).click();
    await finish.waitFor({ state: 'attached', timeout: 15000 });
    await expect(finish).toHaveText('Hello World!');
  });

  test('API-based wait: page document response is captured (waitForResponse)', async ({ page }) => {
    // Race the navigation against a response predicate — genuine API-based wait.
    const responsePromise = page.waitForResponse(
      (resp) => resp.url().includes('/dynamic_loading/2') && resp.status() === 200
    );
    await page.goto('/dynamic_loading/2');
    const response = await responsePromise;
    expect(response.ok()).toBeTruthy();
    expect(response.request().resourceType()).toBe('document');
  });

  test('polling wait: start button re-enabled state via expect.poll', async ({ page }) => {
    await page.goto('/dynamic_loading/1');
    await page.getByRole('button', { name: 'Start' }).click();
    // Poll until the finish text is rendered — demonstrates expect.poll.
    await expect
      .poll(async () => page.locator('#finish h4').isVisible(), { timeout: 15000 })
      .toBe(true);
  });
});
