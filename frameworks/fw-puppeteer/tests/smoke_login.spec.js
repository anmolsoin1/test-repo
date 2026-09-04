// smoke_ prefix = smoke tag (tags via filename prefix).
// Real login flow against https://the-internet.herokuapp.com/login.
const assert = require('assert');

module.exports = async function smokeLogin(page) {
  await page.goto('https://the-internet.herokuapp.com/login', { waitUntil: 'domcontentloaded' });
  await page.type('#username', 'tomsmith');
  await page.type('#password', 'SuperSecretPassword!');
  await page.click('button[type="submit"]');
  await page.waitForSelector('#flash', { timeout: 10000 });
  const flash = await page.$eval('#flash', (el) => el.textContent);
  assert.ok(flash.includes('You logged into a secure area!'), `unexpected flash: ${flash}`);
  const url = page.url();
  assert.ok(url.includes('/secure'), `expected /secure, got ${url}`);
};
