package stepdefs;

import java.time.Duration;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;

/**
 * Login steps for the-internet.herokuapp.com/login.
 * Locator variety: By.id, By.cssSelector, By.xpath, By.linkText.
 */
public class LoginSteps {

    private static final String BASE = "https://the-internet.herokuapp.com";

    private WebDriver driver() {
        return DriverFactory.getDriver(
                ScenarioContext.name());
    }

    private WebDriverWait waitFor() {
        return new WebDriverWait(driver(), Duration.ofSeconds(20));
    }

    @Given("the login page is opened")
    public void openLoginPage() {
        driver().get(BASE + "/login");
        waitFor().until(ExpectedConditions.visibilityOfElementLocated(By.id("username")));
        RunLog.info("Login page loaded, title=" + driver().getTitle());
    }

    @When("the user logs in with username {string} and password {string}")
    public void login(String username, String password) {
        RunLog.info("Logging in as " + username);
        driver().findElement(By.id("username")).sendKeys(username);
        driver().findElement(By.cssSelector("input#password")).sendKeys(password);
        driver().findElement(By.xpath("//button[@type='submit']")).click();
        waitFor().until(ExpectedConditions.visibilityOfElementLocated(By.id("flash")));
    }

    @Then("the login flash message contains {string}")
    public void flashContains(String expected) {
        WebElement flash = waitFor().until(
                ExpectedConditions.visibilityOfElementLocated(By.id("flash")));
        String text = flash.getText();
        RunLog.info("Flash message: " + text.trim());
        Assert.assertTrue(text.contains(expected),
                "Expected flash to contain '" + expected + "' but was: " + text);
    }

    @Then("the secure area heading is displayed")
    public void secureAreaHeading() {
        WebElement heading = waitFor().until(ExpectedConditions.visibilityOfElementLocated(
                By.xpath("//h2[contains(text(),'Secure Area')]")));
        Assert.assertTrue(heading.isDisplayed());
    }

    @When("the user clicks the Logout link")
    public void clickLogout() {
        waitFor().until(ExpectedConditions.elementToBeClickable(By.linkText("Logout")))
                .click();
        waitFor().until(ExpectedConditions.visibilityOfElementLocated(By.id("flash")));
    }
}
