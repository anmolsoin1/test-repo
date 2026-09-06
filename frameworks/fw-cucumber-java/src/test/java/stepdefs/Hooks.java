package stepdefs;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

public class Hooks {

    @Before
    public void beforeScenario(Scenario scenario) {
        ScenarioContext.setName(scenario.getName());
        RunLog.info("=== Scenario start: " + scenario.getName()
                + " | tags: " + scenario.getSourceTagNames() + " ===");
    }

    @After
    public void afterScenario(Scenario scenario) {
        WebDriver driver = DriverFactory.peek();
        try {
            if (scenario.isFailed() && driver != null) {
                byte[] shot = ((TakesScreenshot) driver)
                        .getScreenshotAs(OutputType.BYTES);
                scenario.attach(shot, "image/png", "failure-screenshot");
            }
        } catch (Exception e) {
            RunLog.info("Screenshot attach failed: " + e.getMessage());
        }
        RunLog.info("=== Scenario end: " + scenario.getName()
                + " | status: " + scenario.getStatus() + " ===");
        DriverFactory.quitDriver();
    }
}
