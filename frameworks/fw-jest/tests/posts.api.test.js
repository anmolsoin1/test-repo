const BASE = 'https://jsonplaceholder.typicode.com';

describe('JSONPlaceholder Posts API', () => {
  describe('GET /posts', () => {
    test('returns a list of 100 posts', async () => {
      const res = await fetch(`${BASE}/posts`);
      expect(res.status).toBe(200);
      const posts = await res.json();
      expect(Array.isArray(posts)).toBe(true);
      expect(posts.length).toBe(100);
    });

    test('a single post has the expected shape', async () => {
      const res = await fetch(`${BASE}/posts/1`);
      expect(res.status).toBe(200);
      const post = await res.json();
      expect(post).toMatchObject({ id: 1, userId: 1 });
      expect(typeof post.title).toBe('string');
      expect(typeof post.body).toBe('string');
    });
  });

  describe('POST /posts', () => {
    test('creating a post echoes it back with an id', async () => {
      const res = await fetch(`${BASE}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'he-jest', body: 'api test', userId: 7 }),
      });
      expect(res.status).toBe(201);
      const created = await res.json();
      expect(created).toMatchObject({ title: 'he-jest', userId: 7 });
      expect(created.id).toBeDefined();
    });
  });
});
