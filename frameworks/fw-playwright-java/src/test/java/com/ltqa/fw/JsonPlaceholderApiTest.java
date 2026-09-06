package com.ltqa.fw;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.microsoft.playwright.APIRequest;
import com.microsoft.playwright.APIRequestContext;
import com.microsoft.playwright.APIResponse;
import com.microsoft.playwright.Playwright;
import com.microsoft.playwright.options.RequestOptions;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

/**
 * Fast API tests via Playwright's APIRequestContext — no browser download needed.
 * Target: https://jsonplaceholder.typicode.com (public fake REST API).
 */
public class JsonPlaceholderApiTest {

    private static final String BASE = "https://jsonplaceholder.typicode.com";
    private Playwright playwright;
    private APIRequestContext api;

    @BeforeClass
    public void setup() {
        playwright = Playwright.create();
        api = playwright.request().newContext(
                new APIRequest.NewContextOptions().setBaseURL(BASE));
    }

    @AfterClass
    public void teardown() {
        if (api != null) api.dispose();
        if (playwright != null) playwright.close();
    }

    @Test(groups = {"api", "smoke"})
    public void api_getPost_returns200AndExpectedShape() {
        RunLogger.log("api_getPost_returns200AndExpectedShape", "GET /posts/1");
        APIResponse res = api.get("/posts/1");
        Assert.assertTrue(res.ok(), "expected 2xx, got " + res.status());
        JsonObject body = JsonParser.parseString(res.text()).getAsJsonObject();
        Assert.assertEquals(body.get("id").getAsInt(), 1);
        Assert.assertEquals(body.get("userId").getAsInt(), 1);
        Assert.assertTrue(body.get("title").getAsString().length() > 0, "title must be non-empty");
    }

    @Test(groups = {"api"})
    public void api_listPosts_returnsHundredItems() {
        RunLogger.log("api_listPosts_returnsHundredItems", "GET /posts");
        APIResponse res = api.get("/posts");
        Assert.assertEquals(res.status(), 200);
        JsonArray body = JsonParser.parseString(res.text()).getAsJsonArray();
        Assert.assertEquals(body.size(), 100, "jsonplaceholder always returns 100 posts");
    }

    @Test(groups = {"api", "smoke"})
    public void api_createPost_echoesPayloadWith201() {
        RunLogger.log("api_createPost_echoesPayloadWith201", "POST /posts");
        APIResponse res = api.post("/posts", RequestOptions.create()
                .setHeader("Content-Type", "application/json")
                .setData("{\"title\":\"he-playwright-java\",\"body\":\"stage run\",\"userId\":7}"));
        Assert.assertEquals(res.status(), 201);
        JsonObject body = JsonParser.parseString(res.text()).getAsJsonObject();
        Assert.assertEquals(body.get("title").getAsString(), "he-playwright-java");
        Assert.assertEquals(body.get("userId").getAsInt(), 7);
        Assert.assertTrue(body.has("id"), "server must assign an id");
    }

    @Test(groups = {"api"})
    public void api_getMissingPost_returns404() {
        RunLogger.log("api_getMissingPost_returns404", "GET /posts/999999");
        APIResponse res = api.get("/posts/999999");
        Assert.assertEquals(res.status(), 404);
    }

    /** DELIBERATE FAILURE — kept to prove failure propagation to the HyperExecute UI. */
    @Test(groups = {"api"})
    public void api_DELIBERATE_FAILURE_wrongUserIdAssertion() {
        RunLogger.log("api_DELIBERATE_FAILURE_wrongUserIdAssertion", "GET /posts/1 (expecting failure)");
        APIResponse res = api.get("/posts/1");
        JsonObject body = JsonParser.parseString(res.text()).getAsJsonObject();
        Assert.assertEquals(body.get("userId").getAsInt(), 999,
                "DELIBERATE FAILURE: userId is 1, asserted 999 to demonstrate a red scenario");
    }
}
