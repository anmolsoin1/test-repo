// Tiny runner: node runner.js <spec-file> [more-spec-files...]
// Launches one headless Chromium, gives each spec a fresh page, times it,
// writes a hand-rolled JUnit XML per run into reports/, and exits non-zero
// if any spec failed (drives scenario status via scenarioCommandStatusOnly).
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const { buildTestsuiteXml } = require('./lib/junit');

async function main() {
  const specs = process.argv.slice(2);
  if (specs.length === 0) {
    console.error('usage: node runner.js <spec-file> [...]');
    process.exit(2);
  }

  fs.mkdirSync(path.join(__dirname, 'reports'), { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const results = [];
  for (const spec of specs) {
    const specPath = path.resolve(spec);
    const specName = path.basename(spec);
    const testFn = require(specPath);
    const start = Date.now();
    const page = await browser.newPage();
    try {
      console.log(`[RUN ] ${specName}`);
      await testFn(page);
      console.log(`[PASS] ${specName} (${Date.now() - start}ms)`);
      results.push({ name: specName, classname: 'puppeteer', timeSeconds: (Date.now() - start) / 1000 });
    } catch (err) {
      console.error(`[FAIL] ${specName}: ${err.message}`);
      results.push({
        name: specName,
        classname: 'puppeteer',
        timeSeconds: (Date.now() - start) / 1000,
        failure: { message: err.message, stack: err.stack },
      });
    } finally {
      await page.close();
    }
  }

  await browser.close();

  const xml = buildTestsuiteXml('fw-puppeteer', results);
  const out = path.join(__dirname, 'reports', 'puppeteer-results.xml');
  fs.writeFileSync(out, xml);
  console.log(`junit xml written: ${out}`);

  const failed = results.filter((r) => r.failure).length;
  process.exit(failed === 0 ? 0 : 1);
}

main().catch((err) => {
  console.error('runner crashed:', err);
  process.exit(2);
});
