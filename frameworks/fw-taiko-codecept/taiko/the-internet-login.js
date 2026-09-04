// Taiko REPL-style script — run with: npx taiko taiko/the-internet-login.js
// Taiko globals (goto, write, click, text, ...) are injected by the taiko runner.
const assert = require('assert');

(async () => {
  await openBrowser({ args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] });
  await goto('https://the-internet.herokuapp.com/login', { navigationTimeout: 90000 });
  await write('tomsmith', into(textBox({ id: 'username' })));
  await write('SuperSecretPassword!', into(textBox({ id: 'password' })));
  await click(button('Login'), { waitForNavigation: false });
  await text('You logged into a secure area!').exists();
  assert.ok(await text('You logged into a secure area!').exists());
  console.log('TAIKO-ASSERT: secure-area flash message visible');

  await click(link('Logout'), { waitForNavigation: false });
  assert.ok(await text('You logged out of the secure area!').exists());
  console.log('TAIKO-ASSERT: logged out');
  await closeBrowser();
})();
