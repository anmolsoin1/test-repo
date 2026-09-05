// the-internet.herokuapp.com — Dynamic Loading (Example 2: element rendered
// after the fact). Exercises Nightwatch's explicit-wait APIs:
// waitForElementVisible for the hidden->visible swap and waitUntil +
// perform-based polling for the final text.
module.exports = {
  '@tags': ['the-internet', 'dynamic-loading'],

  'hello world text appears after the loader finishes': async function (browser) {
    await browser.url('https://the-internet.herokuapp.com/dynamic_loading/2');
    await browser.waitForElementVisible('#start button', 10000);
    await browser.click('#start button');

    // #finish exists in the DOM but is hidden until the ~5s loader completes.
    await browser.waitForElementVisible('#finish', 15000);

    // waitUntil + perform-based polling: keep reading the element text until
    // it settles to the expected value (guards against mid-render reads).
    await browser.waitUntil(async function () {
      const result = await browser.getText('#finish');
      await browser.perform(function (done) {
        // perform hook runs each poll iteration — log the current text.
        console.log(`polling #finish, current text: "${result}"`);
        done();
      });
      return result === 'Hello World!';
    }, { timeout: 15000, retryInterval: 500 });

    await browser.assert.textContains('#finish', 'Hello World!');
  },

  'loader bar appears and then disappears once rendering completes': async function (browser) {
    await browser.url('https://the-internet.herokuapp.com/dynamic_loading/2');
    await browser.click('#start button');
    // Immediately after clicking Start the loading bar must be visible...
    await browser.waitForElementVisible('#loading', 5000);
    // ...then it disappears once the element finishes rendering.
    await browser.waitForElementNotVisible('#loading', 15000);
    // And the rendered element is now visible with the final text.
    await browser.waitForElementVisible('#finish', 15000);
    await browser.assert.textContains('#finish', 'Hello World!');
  }
};
