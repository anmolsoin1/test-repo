const BASE = 'https://jsonplaceholder.typicode.com';

describe('JSONPlaceholder Users API', () => {
  describe('GET /users', () => {
    test('returns 10 users', async () => {
      const res = await fetch(`${BASE}/users`);
      expect(res.status).toBe(200);
      const users = await res.json();
      expect(users.length).toBe(10);
    });

    test('user 1 is Leanne Graham', async () => {
      const res = await fetch(`${BASE}/users/1`);
      expect(res.status).toBe(200);
      const user = await res.json();
      expect(user.name).toBe('Leanne Graham');
    });
  });

  describe('negative / mixed status examples', () => {
    test('unknown user id returns 404', async () => {
      const res = await fetch(`${BASE}/users/999`);
      expect(res.status).toBe(404);
    });

    // Deliberate failure: jsonplaceholder actually returns 404 for this id.
    test('DELIBERATE FAIL - expects 200 for a user id that does not exist', async () => {
      const res = await fetch(`${BASE}/users/999`);
      expect(res.status).toBe(200);
    });
  });
});
