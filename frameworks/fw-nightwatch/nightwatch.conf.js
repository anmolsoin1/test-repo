// Nightwatch 3.x configuration for HyperExecute.
// Conventions follow LambdaTest/Hyperexecute-Nightwatch-Sample, but instead of
// the LambdaTest grid this config launches a LOCAL headless Chrome on the
// runner: scripts/setup-chrome.sh downloads a pinned Chrome-for-Testing build
// plus its exact-matching chromedriver into ./browsers/ (see README.md).
const fs = require('fs');
const path = require('path');

// Find a binary installed by `npx @puppeteer/browsers install <tool>@<ver>`
// under browsers/<tool>/*/<platform-dir>/<binary-name>. Globs cover linux
// runners and local mac runs.
// Recursively search for the first file whose basename matches one of
// binaryNames (chrome lives inside a .app bundle on mac, plain dir on linux).
function findBrowserBinary(tool, binaryNames) {
  const root = path.join(__dirname, 'browsers', tool);
  if (!fs.existsSync(root)) {
    throw new Error(
      `${tool} not found under ${root}. Run \`npm run setup:chrome\` first.`
    );
  }
  const stack = [root];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        stack.push(full);
      } else if (binaryNames.includes(entry.name)) {
        return full;
      }
    }
  }
  throw new Error(`No ${binaryNames.join('/')} binary found under ${root}`);
}

module.exports = {
  src_folders: ['tests'],
  output_folder: 'reports',

  page_objects_path: [],
  custom_commands_path: [],
  custom_assertions_path: [],
  plugins: [],
  globals_path: '',

  test_workers: {
    enabled: false
  },

  test_settings: {
    default: {
      disable_error_log: false,
      launch_url: 'https://the-internet.herokuapp.com',
      screenshots: {
        enabled: true,
        path: 'screens',
        on_failure: true
      }
    },

    local: {
      webdriver: {
        start_process: true,
        server_path: findBrowserBinary('chromedriver', ['chromedriver']),
        port: 9515,
        timeout_options: {
          timeout: 60000,
          retry_attempts: 2
        }
      },

      desiredCapabilities: {
        browserName: 'chrome',
        'goog:chromeOptions': {
          binary: findBrowserBinary('chrome', ['chrome', 'Google Chrome for Testing']),
          args: [
            '--headless=new',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--window-size=1280,800'
          ]
        }
      }
    }
  }
};
