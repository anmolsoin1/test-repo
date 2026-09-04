const { test, expect, chromium } = require('@playwright/test');

const caps = {
  browserName: 'Chrome', browserVersion: 'latest',
  'LT:Options': {
    platform: 'Windows 10',
    build: 'HE-Grid-CDP-Playground',
    name: 'Grid login test',
    user: process.env.LT_USERNAME, accessKey: process.env.LT_ACCESS_KEY,
    video: true, network: true,
  },
};

test('the-internet login via stage grid', async () => {
  const browser = await chromium.connect(
    `wss://stage-hub.lambdatestinternal.com/playwright?capabilities=${encodeURIComponent(JSON.stringify(caps))}`
  );
  const page = await browser.newPage();
  await page.goto('https://the-internet.herokuapp.com/login');
  await page.fill('#username', 'tomsmith');
  await page.fill('#password', 'SuperSecretPassword!');
  await page.click('button[type="submit"]');
  await expect(page.locator('#flash')).toContainText('You logged into a secure area!');
  await page.evaluate(() => {}, `lambdatest_action: ${JSON.stringify({ action: 'setTestStatus', arguments: { status: 'passed', remark: 'grid login ok' } })}`);
  await browser.close();
});
