// Per-scenario runner: locates a Chrome binary and runs one TestCafe
// fixture file headless against it. Exit code follows TestCafe's result.
// Usage: node runner.js <fixture-file> [chrome-binary-override]
const { execFileSync, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const fixture = process.argv[2];
if (!fixture) {
    console.error('usage: node runner.js <fixture-file>');
    process.exit(2);
}

function findChrome() {
    // 1. explicit override (local dev): CHROME_BIN env or argv
    if (process.env.CHROME_BIN) return process.env.CHROME_BIN;
    if (process.argv[3]) return process.argv[3];
    // 2. chrome installed by `npx @puppeteer/browsers install chrome@stable`
    //    during the HyperExecute `pre` step (linux runner layout)
    const roots = ['chrome', path.join(process.env.HOME || '', 'chrome')];
    for (const root of roots) {
        if (!root || !fs.existsSync(root)) continue;
        const hits = execFileSync('find', [root, '-name', 'chrome', '-type', 'f'], { encoding: 'utf8' })
            .split('\n').filter(p => p.includes('chrome-linux64/chrome'));
        if (hits.length) return hits[0].trim();
    }
    // 3. fall back to system chrome on PATH
    for (const name of ['google-chrome', 'chrome', 'chromium', 'chromium-browser']) {
        try { return execSync(`command -v ${name}`, { encoding: 'utf8' }).trim(); } catch { /* next */ }
    }
    return null;
}

const chrome = findChrome();
if (!chrome) {
    console.error('no chrome binary found — install one in pre (npx @puppeteer/browsers install chrome@stable)');
    process.exit(2);
}
console.log(`[runner] fixture=${fixture}`);
console.log(`[runner] chrome=${chrome}`);

fs.mkdirSync('reports', { recursive: true });
const reportName = path.basename(fixture).replace(/\.js$/, '') + '.xml';

try {
    execFileSync('npx', [
        'testcafe',
        // NB: `path:<bin>:headless` breaks testcafe's path parsing; headless
        // must be passed as a chrome cmd arg instead. --no-sandbox is needed
        // when running as root on the HyperExecute linux runner.
        `path:${chrome} --headless=new --no-sandbox --disable-dev-shm-usage`,
        fixture,
        '--reporter', `spec,xunit:reports/${reportName}`,
        '--screenshots', 'path=reports/screenshots,takeOnFails=true',
        '--quarantine-mode', 'off',
    ], { stdio: 'inherit' });
    console.log('[runner] PASS');
} catch (e) {
    console.error(`[runner] FAIL (testcafe exit ${e.status})`);
    process.exit(e.status || 1);
}
