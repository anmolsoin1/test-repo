// regression_ prefix = regression tag (tags via filename prefix).
// DELIBERATE FAILURE — asserts a success message after logging in with a
// wrong password, which the site correctly rejects. Exists to prove that a
// failing node exit code propagates to the scenario/job status.
const assert = require('assert');

module.exports = async function regressionLoginInvalidPassword(page) {
  await page.goto('https://the-internet.herokuapp.com/login', { waitUntil: 'domcontentloaded' });
  await page.type('#username', 'tomsmith');
  await page.type('#password', 'WrongPassword!');
  await page.click('button[type="submit"]');
  await page.waitForSelector('#flash', { timeout: 10000 });
  const flash = await page.$eval('#flash', (el) => el.textContent);
  // Deliberately wrong expectation: site says "Your password is invalid!".
  assert.ok(
    flash.includes('You logged into a secure area!'),
    `DELIBERATE FAILURE — expected success banner, got: ${flash.trim()}`
  );
};
