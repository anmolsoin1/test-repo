package com.ltplayground;

import org.testng.Assert;
import org.testng.annotations.Test;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.logging.Logger;

/**
 * Flaky-by-design: fails on the first invocation, passes on retry
 * (RetryAnalyzer allows up to 2 retries). Proves retryAnalyzer wiring
 * and shows how retried attempts appear in HyperExecute scenario history.
 */
public class FlakyRetryTest {
    private static final Logger log = Logger.getLogger(FlakyRetryTest.class.getName());
    private static final AtomicInteger attempts = new AtomicInteger(0);

    @Test(groups = {"regression"}, retryAnalyzer = RetryAnalyzer.class)
    public void flakyPassesOnRetry() {
        int attempt = attempts.incrementAndGet();
        log.info("flakyPassesOnRetry attempt " + attempt);
        Assert.assertTrue(attempt > 1, "deliberately flaky: fails on first attempt, passes on retry");
    }
}
