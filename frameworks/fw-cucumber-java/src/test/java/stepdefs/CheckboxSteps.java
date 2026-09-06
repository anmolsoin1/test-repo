package stepdefs;

import java.time.Duration;
import java.util.List;

import io.cucumber.java.en.And;
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
 * Checkbox steps for the-internet.herokuapp.com/checkboxes.
 * Locator variety: By.xpath (indexed + attribute), By.cssSelector, By.id.
 */
public class CheckboxSteps {

    private static final String BASE = "https://the-internet.herokuapp.com";

    private WebDriver driver() {
        return DriverFactory.getDriver(ScenarioContext.name());
    }

    private WebDriverWait waitFor() {
        return new WebDriverWait(driver(), Duration.ofSeconds(20));
    }

    private List<WebElement> checkboxes() {
        return waitFor().until(ExpectedConditions.visibilityOfAllElementsLocatedBy(
                By.xpath("//form[@id='checkboxes']/input[@type='checkbox']")));
    }

    @Given("the checkboxes page is opened")
    public void openCheckboxesPage() {
        driver().get(BASE + "/checkboxes");
        waitFor().until(ExpectedConditions.visibilityOfElementLocated(
                By.cssSelector("#checkboxes")));
        RunLog.info("Checkboxes page loaded, count=" + checkboxes().size());
    }

    @When("the user checks the first checkbox")
    public void checkFirst() {
        WebElement first = checkboxes().get(0);
        if (!first.isSelected()) {
            first.click();
        }
        RunLog.info("First checkbox checked=" + first.isSelected());
    }

    @And("the user unchecks the second checkbox")
    public void uncheckSecond() {
        WebElement second = checkboxes().get(1);
        if (second.isSelected()) {
            second.click();
        }
        RunLog.info("Second checkbox checked=" + second.isSelected());
    }

    @Then("the first checkbox is selected")
    public void firstSelected() {
        Assert.assertTrue(checkboxes().get(0).isSelected(),
                "first checkbox should be selected");
    }

    @Then("the second checkbox is selected by default")
    public void secondSelectedByDefault() {
        Assert.assertTrue(checkboxes().get(1).isSelected(),
                "second checkbox should be selected by default");
    }

    @And("the second checkbox is not selected")
    public void secondNotSelected() {
        Assert.assertFalse(checkboxes().get(1).isSelected(),
                "second checkbox should not be selected");
    }

    @Then("the promo banner with id {string} is displayed")
    public void promoBannerDisplayed(String id) {
        // DELIBERATE FAILURE: no such element exists on the page.
        WebElement banner = waitFor().until(
                ExpectedConditions.visibilityOfElementLocated(By.id(id)));
        Assert.assertTrue(banner.isDisplayed());
    }
}
