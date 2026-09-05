#!/usr/bin/env bash
# Downloads a pinned Chrome-for-Testing build AND its matching chromedriver
# into ./browsers/ so nightwatch can launch a fully local, version-matched
# headless Chrome on the HyperExecute runner (no grid, no system Chrome).
set -euo pipefail

CHROME_VERSION="152.0.7977.82"

npx @puppeteer/browsers install "chrome@${CHROME_VERSION}" --path browsers
npx @puppeteer/browsers install "chromedriver@${CHROME_VERSION}" --path browsers

echo "Installed chrome + chromedriver ${CHROME_VERSION} under ./browsers"
