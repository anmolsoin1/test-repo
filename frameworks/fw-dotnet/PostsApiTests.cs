using NUnit.Framework;

namespace FwDotnet.Tests;

[TestFixture]
[Category("Posts")]
public class PostsApiTests
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
    public async Task GetPosts_ReturnsListOf100()
    {
        TestContext.Out.WriteLine("GET /posts");
        var response = await _client.GetAsync("/posts");
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        var posts = System.Text.Json.JsonDocument.Parse(body).RootElement;
        Assert.That(posts.GetArrayLength(), Is.EqualTo(100));
    }

    [Test]
    [Category("Smoke"), Category("Single")]
    public async Task GetPostById_ReturnsExpectedPost()
    {
        TestContext.Out.WriteLine("GET /posts/1");
        var response = await _client.GetAsync("/posts/1");
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        var post = System.Text.Json.JsonDocument.Parse(body).RootElement;
        Assert.Multiple(() =>
        {
            Assert.That(post.GetProperty("id").GetInt32(), Is.EqualTo(1));
            Assert.That(post.GetProperty("userId").GetInt32(), Is.EqualTo(1));
            Assert.That(post.GetProperty("title").GetString(), Is.Not.Empty);
        });
    }
}
