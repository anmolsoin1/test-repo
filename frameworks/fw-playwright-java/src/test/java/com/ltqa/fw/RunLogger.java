package com.ltqa.fw;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalTime;

/** Minimal file logger so every run leaves a readable artefact at target/test-run.log. */
public final class RunLogger {
    private static final Path LOG = Paths.get("target", "test-run.log");

    private RunLogger() {}

    public static synchronized void log(String testName, String message) {
        try {
            Files.createDirectories(LOG.getParent());
            Files.writeString(LOG,
                    LocalTime.now() + " [" + testName + "] " + message + System.lineSeparator(),
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (IOException e) {
            throw new RuntimeException("failed to write test-run.log", e);
        }
    }
}
