Feature('JSONPlaceholder posts API');

Scenario('GET /posts/1 returns the expected post @smoke', async ({ I }) => {
  const res = await I.sendGetRequest('/posts/1');
  I.seeResponseCodeIs(200);
  I.seeResponseContainsJson({ id: 1, userId: 1 });
});

Scenario('POST /posts creates a resource @smoke', async ({ I }) => {
  await I.sendPostRequest('/posts', { title: 'he-playground', body: 'codeceptjs', userId: 1 });
  I.seeResponseCodeIs(201);
  I.seeResponseContainsJson({ title: 'he-playground', userId: 1 });
});
