package com.ltplayground.grid;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.time.Duration;

/**
 * Deliberate-failure class: exactly ONE test fails on purpose (wrong expected
 * heading) to prove failure propagation (exit code -> HE scenario status).
 * The other test passes. Not part of the smoke group.
 */
@Test(groups = {"regression"})
public class DeliberateFailureTest extends GridBase {

    private static final String BASE = "https://the-internet.herokuapp.com";

    public void homePageHeadingMatches() {
        driver.get(BASE + "/");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        WebElement heading = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.tagName("h1")));
        Assert.assertEquals(heading.getText(), "Welcome to the-internet");
        log("home page heading verified");
    }

    public void testDeliberateFailure_wrongHeading() {
        driver.get(BASE + "/");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        WebElement heading = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.tagName("h1")));
        // DELIBERATE FAILURE: the real heading is "Welcome to the-internet".
        Assert.assertEquals(heading.getText(), "Welcome to the-internet (staging)",
                "INTENTIONAL FAILURE for HE failure-propagation proof");
    }
}
