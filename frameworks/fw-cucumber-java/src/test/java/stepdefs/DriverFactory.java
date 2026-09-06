package stepdefs;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.RemoteWebDriver;

/**
 * Creates RemoteWebDriver sessions against the canonical LambdaTest hub
 * host (hub.lambdatest.com/wd/hub). Inside the HyperExecute VM this host
 * is resolved internally and the session is what makes the job's
 * Frameworks field (framework logo in the UI) populate.
 *
 * LT_USERNAME / LT_ACCESS_KEY are auto-injected by the HE VM.
 */
public final class DriverFactory {

    private static WebDriver driver;

    private DriverFactory() {
    }

    public static WebDriver getDriver(String scenarioName) {
        if (driver == null) {
            String user = System.getenv("LT_USERNAME");
            String key = System.getenv("LT_ACCESS_KEY");
            if (user == null || key == null) {
                throw new IllegalStateException(
                        "LT_USERNAME / LT_ACCESS_KEY env vars are not set");
            }

            ChromeOptions options = new ChromeOptions();
            options.setBrowserVersion("latest");

            Map<String, Object> ltOptions = new HashMap<>();
            ltOptions.put("platformName", "Windows 10");
            ltOptions.put("build", "HE-Playground-CucumberJVM");
            ltOptions.put("name", scenarioName);
            ltOptions.put("w3c", true);
            ltOptions.put("selenium_version", "4.25.0");
            options.setCapability("LT:Options", ltOptions);

            String gridUrl = "https://" + user + ":" + key
                    + "@hub.lambdatest.com/wd/hub";
            RunLog.info("Creating RemoteWebDriver via canonical hub host for scenario: "
                    + scenarioName);
            try {
                driver = new RemoteWebDriver(new URL(gridUrl), options);
            } catch (MalformedURLException e) {
                throw new IllegalStateException("Bad grid URL", e);
            }
            RunLog.info("Grid session created: "
                    + ((RemoteWebDriver) driver).getSessionId());
        }
        return driver;
    }

    /** Returns the live driver without creating one, or null. */
    public static WebDriver peek() {
        return driver;
    }

    public static void quitDriver() {
        if (driver != null) {
            try {
                driver.quit();
            } catch (Exception e) {
                RunLog.info("driver.quit() failed: " + e.getMessage());
            }
            driver = null;
        }
    }
}
