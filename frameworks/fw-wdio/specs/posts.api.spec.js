const assert = require('assert');
describe('JSONPlaceholder posts API', () => {
  it('lists 100 posts', async () => {
    const r = await fetch('https://jsonplaceholder.typicode.com/posts');
    assert.strictEqual(r.status, 200);
    const posts = await r.json();
    assert.strictEqual(posts.length, 100);
  });
  it('fetches a single post with expected shape', async () => {
    const r = await fetch('https://jsonplaceholder.typicode.com/posts/1');
    const post = await r.json();
    assert.ok(post.id === 1 && post.title && post.userId);
  });
});
