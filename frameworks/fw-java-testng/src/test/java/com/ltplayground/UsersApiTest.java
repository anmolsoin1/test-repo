package com.ltplayground;

import org.testng.Assert;
import org.testng.annotations.Test;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.logging.Logger;

public class UsersApiTest {
    private static final Logger log = Logger.getLogger(UsersApiTest.class.getName());

    @Test(groups = {"smoke"})
    public void listUsersReturns10() throws Exception {
        log.info("GET /users");
        HttpResponse<String> r = HttpClient.newHttpClient().send(
                HttpRequest.newBuilder(URI.create("https://jsonplaceholder.typicode.com/users")).build(),
                HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(r.statusCode(), 200);
        Assert.assertTrue(r.body().contains("\"email\""), "users have emails");
    }

    @Test(groups = {"regression"})
    public void deliberateFailure_user999() throws Exception {
        log.info("GET /users/999 (deliberate failure)");
        HttpResponse<String> r = HttpClient.newHttpClient().send(
                HttpRequest.newBuilder(URI.create("https://jsonplaceholder.typicode.com/users/999")).build(),
                HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(r.statusCode(), 200, "user 999 should exist");
    }
}
