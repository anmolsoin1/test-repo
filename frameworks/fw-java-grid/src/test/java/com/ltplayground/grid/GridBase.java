package com.ltplayground.grid;

import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

import java.io.IOException;
import java.net.URL;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Base class: every test method gets a REAL LambdaTest grid session created
 * from INSIDE the HyperExecute VM against the CANONICAL hub host
 * (https://<user>:<key>@hub.lambdatest.com/wd/hub). This is what makes the
 * HE job's `Frameworks` field populate with ['selenium'] (the Se logo in the
 * UI). Direct stage-hub hosts bypass detection — do not use them here.
 *
 * HE injects LT_USERNAME / LT_ACCESS_KEY into the VM environment; the yaml
 * also sets them as literals, and the constants below are the last fallback.
 */
public abstract class GridBase {

    private static final String FALLBACK_USER = "anmolsoin";
    private static final String FALLBACK_KEY = "LT_GsJOkDD7fZFOAaA0AMBVK2muSGFuiz6BysimcQeReBnfK8m";
    private static final Path LOG_FILE = Paths.get("target", "grid-run.log");

    protected RemoteWebDriver driver;

    protected static void log(String msg) {
        String line = LocalDateTime.now() + " " + msg + "\n";
        System.out.print("[grid] " + line);
        try {
            Files.createDirectories(LOG_FILE.getParent());
            Files.write(LOG_FILE, line.getBytes(),
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (IOException e) {
            System.out.println("[grid] log write failed: " + e.getMessage());
        }
    }

    @BeforeMethod
    public void startSession(java.lang.reflect.Method method) throws Exception {
        String user = System.getenv().getOrDefault("LT_USERNAME", FALLBACK_USER);
        String key = System.getenv().getOrDefault("LT_ACCESS_KEY", FALLBACK_KEY);
        String hub = "https://" + user + ":" + key + "@hub.lambdatest.com/wd/hub";

        ChromeOptions options = new ChromeOptions();
        options.setPlatformName("Windows 11");
        options.setBrowserVersion("latest");

        Map<String, Object> ltOptions = new HashMap<>();
        ltOptions.put("build", "HE-fw-java-grid");
        ltOptions.put("name", getClass().getSimpleName() + "." + method.getName());
        ltOptions.put("project", "he-playground");
        ltOptions.put("selenium_version", "4.25.0");
        ltOptions.put("w3c", true);
        ltOptions.put("console", true);
        options.setCapability("LT:Options", ltOptions);

        log("creating RemoteWebDriver session on canonical hub for "
                + getClass().getSimpleName() + "." + method.getName());
        driver = new RemoteWebDriver(new URL(hub), options);
        log("session created: " + driver.getSessionId());
    }

    @AfterMethod(alwaysRun = true)
    public void stopSession() {
        if (driver != null) {
            try {
                log("quitting session " + driver.getSessionId());
                driver.quit();
            } catch (Exception e) {
                log("quit failed: " + e.getMessage());
            }
        }
    }
}
