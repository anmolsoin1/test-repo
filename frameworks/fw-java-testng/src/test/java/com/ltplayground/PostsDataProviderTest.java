package com.ltplayground;

import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.logging.Logger;

/**
 * DataProvider-driven test: one method, N invocations (one per post ID).
 * With discoveryType: method, each invocation is a separate scenario row
 * in HyperExecute.
 */
public class PostsDataProviderTest {
    private static final Logger log = Logger.getLogger(PostsDataProviderTest.class.getName());
    private final HttpClient client = HttpClient.newHttpClient();

    @DataProvider(name = "postIds")
    public Object[][] postIds() {
        return new Object[][]{{1}, {2}, {3}, {42}, {100}};
    }

    @Test(dataProvider = "postIds", groups = {"smoke", "regression"})
    public void postByIdHasMatchingId(int postId) throws Exception {
        log.info("GET /posts/" + postId);
        HttpResponse<String> r = client.send(
                HttpRequest.newBuilder(URI.create("https://jsonplaceholder.typicode.com/posts/" + postId)).build(),
                HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(r.statusCode(), 200, "status for post " + postId);
        Assert.assertTrue(r.body().contains("\"id\": " + postId), "id field for post " + postId);
    }
}
