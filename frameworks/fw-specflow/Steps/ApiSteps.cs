using System.Net;
using System.Text.Json;
using NUnit.Framework;
using TechTalk.SpecFlow;

namespace FwSpecflow.Steps;

[Binding]
public class ApiSteps
{
    private const string BaseUrl = "https://jsonplaceholder.typicode.com";
    private static readonly string LogDir = Path.Combine(Directory.GetCurrentDirectory(), "logs");

    private readonly HttpClient _http = new();
    private HttpResponseMessage? _response;
    private JsonDocument? _body;

    private static void Log(string message)
    {
        Directory.CreateDirectory(LogDir);
        File.AppendAllText(Path.Combine(LogDir, "execution.log"),
            $"{DateTime.UtcNow:O} [specflow] {message}{Environment.NewLine}");
    }

    private async Task GetAsync(string path)
    {
        Log($"GET {BaseUrl}{path}");
        _response = await _http.GetAsync($"{BaseUrl}{path}");
        var text = await _response.Content.ReadAsStringAsync();
        _body = JsonDocument.Parse(text);
        Log($"status={(int)_response.StatusCode} bytes={text.Length}");
    }

    [When(@"I request the posts list")]
    public Task WhenIRequestThePostsList() => GetAsync("/posts");

    [When(@"I request the users list")]
    public Task WhenIRequestTheUsersList() => GetAsync("/users");

    [When(@"I request post (\d+)")]
    public Task WhenIRequestPost(int id) => GetAsync($"/posts/{id}");

    [When(@"I request user (\d+)")]
    public Task WhenIRequestUser(int id) => GetAsync($"/users/{id}");

    [Then(@"the response status should be (\d+)")]
    public void ThenTheResponseStatusShouldBe(int expected)
    {
        Assert.That(_response, Is.Not.Null);
        Log($"assert status expected={expected} actual={(int)_response!.StatusCode}");
        Assert.That((int)_response!.StatusCode, Is.EqualTo(expected));
    }

    [Then(@"the posts list should contain (\d+) items")]
    public void ThenPostsListCount(int expected) =>
        Assert.That(_body!.RootElement.GetArrayLength(), Is.EqualTo(expected));

    [Then(@"the users list should contain (\d+) items")]
    public void ThenUsersListCount(int expected) =>
        Assert.That(_body!.RootElement.GetArrayLength(), Is.EqualTo(expected));

    [Then(@"the post should have id (\d+)")]
    public void ThenPostId(int expected) =>
        Assert.That(_body!.RootElement.GetProperty("id").GetInt32(), Is.EqualTo(expected));

    [Then(@"the post should have userId (\d+)")]
    public void ThenPostUserId(int expected) =>
        Assert.That(_body!.RootElement.GetProperty("userId").GetInt32(), Is.EqualTo(expected));

    [Then(@"the user should have username ""(.*)""")]
    public void ThenUsername(string expected) =>
        Assert.That(_body!.RootElement.GetProperty("username").GetString(), Is.EqualTo(expected));
}
