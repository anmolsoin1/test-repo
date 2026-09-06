package com.ltplayground.grid;

import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.time.Duration;

/**
 * the-internet.herokuapp.com/checkboxes + /dynamic_loading/1 — checkbox state
 * toggling and FluentWait (polling) against a real grid session.
 */
@Test(groups = {"smoke", "regression"})
public class CheckboxesTest extends GridBase {

    private static final String BASE = "https://the-internet.herokuapp.com";

    public void toggleBothCheckboxes() {
        driver.get(BASE + "/checkboxes");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.xpath("//form[@id='checkboxes']")));

        WebElement cb1 = driver.findElement(By.xpath("//form[@id='checkboxes']/input[1]"));
        WebElement cb2 = driver.findElement(By.cssSelector("#checkboxes input:nth-of-type(2)"));

        Assert.assertFalse(cb1.isSelected(), "checkbox 1 starts unchecked");
        Assert.assertTrue(cb2.isSelected(), "checkbox 2 starts checked");

        cb1.click();
        cb2.click();

        Assert.assertTrue(cb1.isSelected(), "checkbox 1 checked after click");
        Assert.assertFalse(cb2.isSelected(), "checkbox 2 unchecked after click");
        log("both checkboxes toggled and state asserted");
    }

    public void fluentWaitForDynamicLoadingElement() {
        driver.get(BASE + "/dynamic_loading/1");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        WebElement start = wait.until(ExpectedConditions.elementToBeClickable(
                By.xpath("//div[@id='start']/button")));
        start.click();

        FluentWait<org.openqa.selenium.remote.RemoteWebDriver> fluent =
                new FluentWait<>(driver)
                        .withTimeout(Duration.ofSeconds(20))
                        .pollingEvery(Duration.ofMillis(500))
                        .ignoring(NoSuchElementException.class);

        WebElement hello = fluent.until(d -> {
            WebElement el = d.findElement(By.cssSelector("#finish h4"));
            return el.isDisplayed() ? el : null;
        });

        Assert.assertEquals(hello.getText(), "Hello World!");
        log("FluentWait polling verified dynamic element text");
    }
}
