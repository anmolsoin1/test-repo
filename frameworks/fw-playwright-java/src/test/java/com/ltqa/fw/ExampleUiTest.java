package com.ltqa.fw;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

/**
 * UI smoke against a local headless chromium (installed in the HyperExecute pre
 * step via the Playwright CLI). No LambdaTest grid session is created — this
 * intentionally proves local-browser execution inside the HE VM.
 */
public class ExampleUiTest {

    private Playwright playwright;
    private Browser browser;

    @BeforeClass
    public void setup() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
                new BrowserType.LaunchOptions().setHeadless(true));
    }

    @AfterClass
    public void teardown() {
        if (browser != null) browser.close();
        if (playwright != null) playwright.close();
    }

    @Test(groups = {"ui", "smoke"})
    public void ui_exampleCom_titleAndHeading() {
        RunLogger.log("ui_exampleCom_titleAndHeading", "navigate example.com");
        Page page = browser.newPage();
        page.navigate("https://example.com");
        Assert.assertEquals(page.title(), "Example Domain");
        // locator variety: xpath heading, css paragraph
        Assert.assertEquals(page.locator("//h1").innerText(), "Example Domain");
        // text-content assertion on the paragraph (css locator); example.com's
        // current copy says "documentation examples" (was "illustrative examples"
        // before the 2025 redesign — cost us two failed runs to learn)
        String paragraph = page.locator("p").first().innerText();
        RunLogger.log("ui_exampleCom_titleAndHeading", "paragraph text: " + paragraph);
        Assert.assertTrue(paragraph.contains("documentation examples"),
                "unexpected example.com copy: " + paragraph);
        page.close();
    }

    @Test(groups = {"ui"})
    public void ui_exampleCom_moreInfoLinkNavigates() {
        RunLogger.log("ui_exampleCom_moreInfoLinkNavigates", "follow 'Learn more' link");
        Page page = browser.newPage();
        page.navigate("https://example.com");
        // locator variety: role-based link by accessible name, then explicit URL wait
        page.getByRole(com.microsoft.playwright.options.AriaRole.LINK,
                new Page.GetByRoleOptions().setName("Learn more")).click();
        page.waitForURL(url -> url.contains("iana.org"),
                new Page.WaitForURLOptions().setTimeout(15000));
        Assert.assertTrue(page.url().contains("iana.org"), "expected iana.org, got " + page.url());
        page.close();
    }
}
