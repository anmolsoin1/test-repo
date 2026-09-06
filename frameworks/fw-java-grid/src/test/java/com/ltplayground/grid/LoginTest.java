package com.ltplayground.grid;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.time.Duration;

/**
 * the-internet.herokuapp.com/login — form authentication via a real grid
 * session. Locator variety: By.id, By.cssSelector, By.xpath, By.linkText.
 * Explicit waits via WebDriverWait.
 */
@Test(groups = {"smoke", "regression"})
public class LoginTest extends GridBase {

    private static final String BASE = "https://the-internet.herokuapp.com";

    public void validLoginLandsInSecureArea() {
        driver.get(BASE + "/login");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username")));

        driver.findElement(By.id("username")).sendKeys("tomsmith");
        driver.findElement(By.cssSelector("input#password")).sendKeys("SuperSecretPassword!");
        driver.findElement(By.xpath("//button[@type='submit']")).click();

        WebElement flash = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#flash")));
        Assert.assertTrue(flash.getText().contains("You logged into a secure area!"),
                "success flash expected, got: " + flash.getText());

        WebElement heading = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[@id='content']//h2")));
        Assert.assertEquals(heading.getText(), "Secure Area");
        log("valid login OK, secure area heading verified");
    }

    public void invalidLoginShowsErrorFlash() {
        driver.get(BASE + "/login");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username")));

        driver.findElement(By.id("username")).sendKeys("notauser");
        driver.findElement(By.id("password")).sendKeys("wrongpass");
        driver.findElement(By.xpath("//button[contains(@class,'radius')]")).click();

        WebElement flash = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("flash")));
        Assert.assertTrue(flash.getText().contains("Your username is invalid!"),
                "error flash expected, got: " + flash.getText());
        log("invalid login error flash verified");
    }

    public void logoutViaLinkTextReturnsToLoginPage() {
        driver.get(BASE + "/login");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username")));

        driver.findElement(By.id("username")).sendKeys("tomsmith");
        driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
        driver.findElement(By.cssSelector("button.radius")).click();

        WebElement logout = wait.until(
                ExpectedConditions.elementToBeClickable(By.linkText("Logout")));
        logout.click();

        WebElement flash = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#flash")));
        Assert.assertTrue(flash.getText().contains("You logged out of the secure area!"),
                "logout flash expected, got: " + flash.getText());
        Assert.assertTrue(driver.findElements(By.id("username")).size() > 0,
                "username field should be back after logout");
        log("logout flow verified via linkText locator");
    }
}
