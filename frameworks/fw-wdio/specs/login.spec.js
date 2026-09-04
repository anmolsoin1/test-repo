describe('the-internet login (wdio via stage grid)', () => {
  it('logs in with valid credentials @smoke', async () => {
    await browser.url('https://the-internet.herokuapp.com/login');
    await $('#username').setValue('tomsmith');
    await $('#password').setValue('SuperSecretPassword!');
    await $('button[type="submit"]').click();
    await expect($('#flash')).toHaveTextContaining('You logged into a secure area!');
  });
  it('rejects invalid credentials @regression', async () => {
    await browser.url('https://the-internet.herokuapp.com/login');
    await $('#username').setValue('tomsmith');
    await $('#password').setValue('wrong-password');
    await $('button[type="submit"]').click();
    // explicit wait: #flash only exists after the navigation settles on the grid
    const flash = await $('#flash');
    await flash.waitForExist({ timeout: 15000 });
    await expect(flash).toHaveTextContaining('Your password is invalid!');
  });
});
