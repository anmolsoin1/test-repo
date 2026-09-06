package stepdefs;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/** Appends timestamped lines to stdout and target/cucumber-reports/execution.log. */
public final class RunLog {

    private static final Path LOG_FILE =
            Paths.get("target", "cucumber-reports", "execution.log");
    private static final DateTimeFormatter TS =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    private RunLog() {
    }

    public static synchronized void info(String message) {
        String line = LocalDateTime.now().format(TS) + " [INFO] " + message;
        System.out.println(line);
        try {
            Files.createDirectories(LOG_FILE.getParent());
            Files.write(LOG_FILE, (line + System.lineSeparator())
                            .getBytes(StandardCharsets.UTF_8),
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (IOException e) {
            System.out.println("RunLog write failed: " + e.getMessage());
        }
    }
}
