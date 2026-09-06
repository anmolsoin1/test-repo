package runners;

import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class JsonPlaceholderRunner {

    @Test
    void run() {
        String path = System.getProperty("FeaturePath", "classpath:jsonplaceholder");
        String tags = System.getProperty("KarateTags");
        Runner.Builder builder = Runner.path(path);
        if (tags != null && !tags.isEmpty()) {
            builder.tags(tags);
        }
        Results results = builder
                .outputCucumberJson(true)
                .outputJunitXml(true)
                .reportDir("target/karate-reports")
                .parallel(1);
        assertEquals(0, results.getFailCount(), results.getErrorMessages());
    }
}
