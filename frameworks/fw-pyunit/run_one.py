"""Per-file unittest runner for HyperExecute (stdlib only).

Usage: python run_one.py tests/test_login.py

- Loads the test file as a module, runs it with unittest.
- If the TAG env var is set, only tests whose id() contains the tag run
  (tag-filtered variant: hyperexecute-smoke.yaml sets TAG=smoke).
- Writes a JUnit XML report to reports/junit-<name>.xml so HE partialReports
  can upload it, and mirrors verbose output to stdout.
- Exit code follows the test result (scenarioCommandStatusOnly: true).
"""
import importlib.util
import os
import sys
import time
import unittest
from unittest.runner import _WritelnDecorator
from xml.sax.saxutils import escape, quoteattr


class RecordingResult(unittest.TextTestResult):
    def __init__(self, stream, verbosity):
        super().__init__(stream, True, verbosity)
        self.records = []  # (test_id, status, detail, seconds)
        self._starts = {}

    def startTest(self, test):
        self._starts[test.id()] = time.time()
        super().startTest(test)

    def _record(self, test, status, detail=""):
        secs = time.time() - self._starts.get(test.id(), time.time())
        self.records.append((test.id(), status, detail, secs))

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "passed")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "failure", self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "error", self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._record(test, "skipped", reason)

    def addSubTest(self, test, subtest, err):
        # subTest failures bypass addFailure and land directly in
        # self.failures — record them explicitly.
        super().addSubTest(test, subtest, err)
        if err is not None:
            status = "failure" if issubclass(err[0], test.failureException) else "error"
            self._record(subtest, status, self._exc_info_to_string(err, test))


def iter_tests(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


def filter_suite(suite, tag):
    keep = unittest.TestSuite()
    for test in iter_tests(suite):
        if tag in test.id():
            keep.addTest(test)
    return keep


def write_junit(result, name, path):
    failures = sum(1 for r in result.records if r[1] == "failure")
    errors = sum(1 for r in result.records if r[1] == "error")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<testsuite name=%s tests="%d" failures="%d" errors="%d">'
        % (quoteattr(name), len(result.records), failures, errors),
    ]
    for test_id, status, detail, secs in result.records:
        classname, _, method = test_id.rpartition(".")
        lines.append(
            '  <testcase classname=%s name=%s time="%.3f">'
            % (quoteattr(classname), quoteattr(method), secs)
        )
        if status in ("failure", "error"):
            tag = "failure" if status == "failure" else "error"
            lines.append(
                "    <%s>%s</%s>" % (tag, escape(detail[-2000:]), tag)
            )
        elif status == "skipped":
            lines.append('    <skipped message=%s/>' % quoteattr(detail))
        lines.append("  </testcase>")
    lines.append("</testsuite>")
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    path = sys.argv[1]
    name = os.path.splitext(os.path.basename(path))[0]
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    tag = os.environ.get("TAG", "").strip()
    if tag:
        suite = filter_suite(suite, tag)
        print("TAG filter active: %s" % tag)

    result = RecordingResult(_WritelnDecorator(sys.stdout), 2)
    start = time.time()
    suite.run(result)
    result.printErrors()
    print("Ran %d tests in %.2fs" % (result.testsRun, time.time() - start))

    os.makedirs("reports", exist_ok=True)
    xml_path = os.path.join("reports", "junit-%s.xml" % name)
    write_junit(result, name, xml_path)
    print("JUnit report: %s" % xml_path)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
