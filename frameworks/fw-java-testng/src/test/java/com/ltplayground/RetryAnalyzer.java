package com.ltplayground;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;
import java.util.logging.Logger;

/**
 * Retries a failed test up to MAX_RETRIES times within the same TestNG run.
 * Attach via @Test(retryAnalyzer = RetryAnalyzer.class).
 * On retry, TestNG marks the failed attempt SKIPPED (retried) and the
 * final attempt keeps its real status — HyperExecute surfaces these as
 * separate history entries for the scenario.
 */
public class RetryAnalyzer implements IRetryAnalyzer {
    private static final Logger log = Logger.getLogger(RetryAnalyzer.class.getName());
    private static final int MAX_RETRIES = 2;
    private int count = 0;

    @Override
    public boolean retry(ITestResult result) {
        if (count < MAX_RETRIES) {
            count++;
            log.info("Retrying " + result.getMethod().getMethodName() + " attempt " + (count + 1));
            return true;
        }
        return false;
    }
}
