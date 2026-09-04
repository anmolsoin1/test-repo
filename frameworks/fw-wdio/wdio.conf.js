exports.config = {
  user: process.env.LT_USERNAME,
  key: process.env.LT_ACCESS_KEY,
  hostname: 'stage-hub.lambdatestinternal.com',
  protocol: 'https',
  port: 443,
  path: '/wd/hub',
  specs: ['./specs/*.spec.js'],
  framework: 'mocha',
  mochaOpts: { timeout: 90000 },
  reporters: ['spec'],
  logLevel: 'warn',
  capabilities: [{
    browserName: 'Chrome',
    'LT:Options': {
      platform: 'Windows 10',
      build: 'HE-WDIO-Playground',
      name: 'wdio grid test',
      video: true,
      network: true,
    },
  }],
};
