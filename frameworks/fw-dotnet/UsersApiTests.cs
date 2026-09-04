using NUnit.Framework;

namespace FwDotnet.Tests;

[TestFixture]
[Category("Users")]
public class UsersApiTests
{
    private HttpClient _client = null!;

    [SetUp]
    public void SetUp()
    {
        _client = new HttpClient { BaseAddress = new Uri("https://jsonplaceholder.typicode.com") };
    }

    [TearDown]
    public void TearDown() => _client.Dispose();

    [Test]
    [Category("Smoke"), Category("List")]
    public async Task GetUsers_ReturnsListOf10()
    {
        TestContext.Out.WriteLine("GET /users");
        var response = await _client.GetAsync("/users");
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        var users = System.Text.Json.JsonDocument.Parse(body).RootElement;
        Assert.That(users.GetArrayLength(), Is.EqualTo(10));
    }

    // DELIBERATE FAILURE: asserts a status code the API will not return,
    // to prove failed tests surface correctly in HyperExecute v0.2 dotnet mode.
    [Test]
    [Category("DeliberateFailure")]
    public async Task GetUserById_DELIBERATE_FAILURE_Expects404ForExistingUser()
    {
        TestContext.Out.WriteLine("GET /users/1 — deliberately asserting 404 on a user that exists");
        var response = await _client.GetAsync("/users/1");
        Assert.That((int)response.StatusCode, Is.EqualTo(404),
            "DELIBERATE FAILURE — /users/1 actually returns 200");
    }
}
