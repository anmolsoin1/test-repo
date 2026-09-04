// Minimal hand-rolled JUnit XML writer — no dependencies.
// Demonstrates that any framework can emit a <testsuite> document that
// HyperExecute can pick up via partialReports.

function escapeXml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * results: [{ name, classname, timeSeconds, failure?: { message, stack } }]
 * Returns a JUnit-style XML string.
 */
function buildTestsuiteXml(suiteName, results) {
  const failures = results.filter((r) => r.failure).length;
  const time = results.reduce((acc, r) => acc + r.timeSeconds, 0).toFixed(3);
  const cases = results
    .map((r) => {
      const attrs = `name="${escapeXml(r.name)}" classname="${escapeXml(r.classname)}" time="${r.timeSeconds.toFixed(3)}"`;
      if (!r.failure) return `    <testcase ${attrs}/>`;
      return [
        `    <testcase ${attrs}>`,
        `      <failure message="${escapeXml(r.failure.message)}">${escapeXml(r.failure.stack || r.failure.message)}</failure>`,
        `    </testcase>`,
      ].join('\n');
    })
    .join('\n');
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    `<testsuites>`,
    `  <testsuite name="${escapeXml(suiteName)}" tests="${results.length}" failures="${failures}" errors="0" skipped="0" time="${time}">`,
    cases,
    `  </testsuite>`,
    `</testsuites>`,
    '',
  ].join('\n');
}

module.exports = { buildTestsuiteXml };
