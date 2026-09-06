package stepdefs;

/** Holds the current scenario name so steps can lazily create the driver. */
public final class ScenarioContext {

    private static String scenarioName = "unknown";

    private ScenarioContext() {
    }

    public static void setName(String name) {
        scenarioName = name;
    }

    public static String name() {
        return scenarioName;
    }
}
