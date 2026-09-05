import { Selector } from 'testcafe';

const BASE = 'https://the-internet.herokuapp.com';

const usernameInput = Selector('#username');
const passwordInput = Selector('#password');
const loginButton   = Selector('button.radius');
const flashMessage  = Selector('#flash');

fixture `The Internet — login (DELIBERATE FAILURE)`
    .page `${BASE}/login`;

// DELIBERATE FAILURE: wrong password is used, then the test asserts a
// success banner — the app correctly shows an error, so this test must fail.
// Kept to prove HyperExecute surfaces per-scenario failure for TestCafe.
test('regression: invalid password must NOT log in (expects failure)', async t => {
    await t
        .typeText(usernameInput, 'tomsmith')
        .typeText(passwordInput, 'WrongPassword123')
        .click(loginButton);

    await t.wait(1000);

    const flash = flashMessage.with({ timeout: 10000 });
    await t.expect(flash.exists).ok('flash banner should appear');

    // This assertion is WRONG on purpose: with a bad password the flash says
    // "Your password is invalid!", so expecting the success text fails here.
    await t
        .expect(flash.innerText)
        .contains('You logged into a secure area!', 'DELIBERATE FAILURE — invalid password should not produce a success banner');
});
