// the-internet.herokuapp.com — Form Authentication
// Real end-to-end flow against the public test site: open the login page,
// submit valid credentials, assert the secure area loads.
module.exports = {
  '@tags': ['the-internet', 'login'],

  'successful login lands on the secure area': function (browser) {
    browser
      .url('https://the-internet.herokuapp.com/login')
      .waitForElementVisible('#username', 10000)
      .setValue('#username', 'tomsmith')
      .setValue('#password', 'SuperSecretPassword!')
      .click('button[type="submit"]')
      .waitForElementVisible('#flash', 10000)
      .assert.textContains('#flash', 'You logged into a secure area!')
      .assert.urlContains('/secure')
      // End the session so the next test case in this file starts with a
      // clean browser (session state between test cases made setValue flaky).
      .end();
  },

  'logout returns to the login page': function (browser) {
    browser
      .url('https://the-internet.herokuapp.com/login')
      .waitForElementVisible('#username', 10000)
      .setValue('#username', 'tomsmith')
      .setValue('#password', 'SuperSecretPassword!')
      .click('button[type="submit"]')
      .waitForElementVisible('#flash', 10000)
      .waitForElementVisible('a[href="/logout"]', 10000)
      .click('a[href="/logout"]')
      // Wait for a NEW-page marker before reading #flash — #flash also exists
      // on /secure, so waiting on #flash itself catches the stale element.
      .waitForElementVisible('#username', 10000)
      .assert.textContains('#flash', 'You logged out of the secure area!');
  }
};
