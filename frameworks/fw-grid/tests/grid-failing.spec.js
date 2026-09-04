const { test, expect, chromium } = require('@playwright/test');

const caps = {
  browserName: 'Chrome', browserVersion: 'latest',
  'LT:Options': {
    platform: 'Windows 10',
    build: 'HE-Grid-CDP-Playground',
    name: 'Grid DELIBERATE failure',
    user: process.env.LT_USERNAME, accessKey: process.env.LT_ACCESS_KEY,
  },
};

test('deliberate failure via stage grid', async () => {
  const browser = await chromium.connect(
    `wss://stage-hub.lambdatestinternal.com/playwright?capabilities=${encodeURIComponent(JSON.stringify(caps))}`
  );
  const page = await browser.newPage();
  await page.goto('https://the-internet.herokuapp.com/');
  await expect(page).toHaveTitle('This Title Does Not Exist');
  await browser.close();
});
