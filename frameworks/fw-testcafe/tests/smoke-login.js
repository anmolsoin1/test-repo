import { Selector } from 'testcafe';

const BASE = 'https://the-internet.herokuapp.com';

// Selector variety: by id, by css class, by visible text
const usernameInput = Selector('#username');               // by id
const passwordInput = Selector('#password');               // by id
const loginButton   = Selector('button.radius');           // by css class
const flashMessage  = Selector('#flash');                  // by id
const logoutButton  = Selector('a.button.secondary.radius'); // by css
const subHeader     = Selector('.subheader');              // by css

// Poll an assertion condition manually until timeout (polling assertion loop).
async function pollUntil(check, timeoutMs, intervalMs = 500) {
    const start = Date.now();
    let last;
    while (Date.now() - start < timeoutMs) {
        last = await check();
        if (last) return true;
        await new Promise(r => setTimeout(r, intervalMs));
    }
    return false;
}

fixture `The Internet — login (passing)`
    .page `${BASE}/login`;

test('smoke: valid login reaches secure area', async t => {
    await t
        .typeText(usernameInput, 'tomsmith')
        .typeText(passwordInput, 'SuperSecretPassword!')
        .click(loginButton);

    // Explicit wait: fixed pause to let navigation settle
    await t.wait(1000);

    // Explicit wait: Selector.with({ timeout }) — wait up to 10s for element
    const secureFlash = flashMessage.with({ timeout: 10000 });
    await t.expect(secureFlash.exists).ok('flash banner should appear after login');
    await t
        .expect(secureFlash.innerText)
        .contains('You logged into a secure area!', 'success banner text');

    // Polling assertion loop: wait until subheader contains "Secure Area"
    const found = await pollUntil(
        async () => (await subHeader.innerText).includes('Secure Area'),
        10000
    );
    await t.expect(found).ok('subheader should read "Secure Area" within 10s (polled)');

    // Text-based selector inside a click action
    await t.click(logoutButton);
    await t.expect(Selector('h2').withText('Login Page').with({ timeout: 10000 }).exists)
        .ok('should be back on Login Page after logout');
});
