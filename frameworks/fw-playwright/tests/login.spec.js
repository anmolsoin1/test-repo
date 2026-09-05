// @ts-check
const { test, expect } = require('@playwright/test');

// Locator variety spec: getByLabel, getByRole, getByText, css, xpath.
test.describe('Login form @smoke', () => {
  test('valid login shows secure area (getByLabel + getByRole)', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('tomsmith');
    await page.getByLabel('Password').fill('SuperSecretPassword!');
    await page.getByRole('button', { name: 'Login' }).click();
    await expect(page.locator('.flash.success')).toContainText('You logged into a secure area!');
    await expect(page.getByRole('link', { name: 'Logout' })).toBeVisible();
  });

  test('invalid username shows error (css locator)', async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', 'baduser');
    await page.fill('#password', 'wrongpass');
    await page.click('button[type="submit"]');
    await expect(page.locator('.flash.error')).toContainText('Your username is invalid!');
  });

  test('invalid password shows error (xpath locator)', async ({ page }) => {
    await page.goto('/login');
    await page.locator('xpath=//input[@id="username"]').fill('tomsmith');
    await page.locator('xpath=//input[@id="password"]').fill('wrongpass');
    await page.locator('xpath=//button[@type="submit"]').click();
    await expect(page.locator('xpath=//div[contains(@class,"flash error")]')).toContainText('Your password is invalid!');
  });

  test('secure area page heading via getByText + getByRole heading', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('tomsmith');
    await page.getByLabel('Password').fill('SuperSecretPassword!');
    await page.getByRole('button', { name: 'Login' }).click();
    await expect(page.getByRole('heading', { name: 'Secure Area', exact: true })).toBeVisible();
    await expect(page.getByText('Welcome to the Secure Area', { exact: false })).toBeVisible();
  });
});
