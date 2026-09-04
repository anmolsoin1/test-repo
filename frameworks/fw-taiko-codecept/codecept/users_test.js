Feature('JSONPlaceholder users API');

Scenario('GET /users/1 returns the expected user @smoke @regression', async ({ I }) => {
  await I.sendGetRequest('/users/1');
  I.seeResponseCodeIs(200);
  I.seeResponseContainsJson({ id: 1, username: 'Bret' });
});

Scenario('GET /todos/1 returns a todo for user 1 @regression', async ({ I }) => {
  await I.sendGetRequest('/todos/1');
  I.seeResponseCodeIs(200);
  I.seeResponseContainsJson({ userId: 1, id: 1, completed: false });
});
