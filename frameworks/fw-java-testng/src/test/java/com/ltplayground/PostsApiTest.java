package com.ltplayground;

import org.testng.Assert;
import org.testng.annotations.Test;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.logging.Logger;

public class PostsApiTest {
    private static final Logger log = Logger.getLogger(PostsApiTest.class.getName());
    private final HttpClient client = HttpClient.newHttpClient();

    private HttpResponse<String> get(String path) throws Exception {
        log.info("GET " + path);
        return client.send(HttpRequest.newBuilder(URI.create("https://jsonplaceholder.typicode.com" + path)).build(),
                HttpResponse.BodyHandlers.ofString());
    }

    @Test(groups = {"smoke"})
    public void listPostsReturns100() throws Exception {
        HttpResponse<String> r = get("/posts");
        Assert.assertEquals(r.statusCode(), 200, "status");
        Assert.assertTrue(r.body().contains("\"userId\""), "payload shape");
    }

    @Test(groups = {"smoke", "regression"})
    public void singlePostHasFields() throws Exception {
        HttpResponse<String> r = get("/posts/1");
        Assert.assertEquals(r.statusCode(), 200);
        Assert.assertTrue(r.body().contains("\"id\": 1"), "post id");
    }

    @Test(groups = {"regression"})
    public void createPostReturns201() throws Exception {
        log.info("POST /posts");
        HttpResponse<String> r = client.send(
                HttpRequest.newBuilder(URI.create("https://jsonplaceholder.typicode.com/posts"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString("{\"title\":\"he-playground\",\"body\":\"x\",\"userId\":1}"))
                        .build(), HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(r.statusCode(), 201, "create status");
    }
}
