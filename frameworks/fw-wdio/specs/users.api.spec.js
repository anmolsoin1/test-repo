const assert = require('assert');
describe('JSONPlaceholder users API', () => {
  it('lists 10 users', async () => {
    const r = await fetch('https://jsonplaceholder.typicode.com/users');
    const users = await r.json();
    assert.strictEqual(users.length, 10);
  });
  it('DELIBERATE FAILURE: expects user 999 to exist', async () => {
    const r = await fetch('https://jsonplaceholder.typicode.com/users/999');
    assert.strictEqual(r.status, 200, 'user 999 should exist');
  });
});
