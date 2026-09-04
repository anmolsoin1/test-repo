// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Login form @smoke', () => {
  test('valid login shows secure area @smoke', async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', 'tomsmith');
    await page.fill('#password', 'SuperSecretPassword!');
    await page.click('button[type="submit"]');
    await expect(page.locator('.flash.success')).toContainText('You logged into a secure area!');
    await expect(page.locator('a.button.secondary.radius')).toBeVisible();
  });

  test('invalid login shows error', async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', 'baduser');
    await page.fill('#password', 'wrongpass');
    await page.click('button[type="submit"]');
    await expect(page.locator('.flash.error')).toContainText('Your username is invalid!');
  });
});
