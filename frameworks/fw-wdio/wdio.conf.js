exports.config = {
  runner: 'local',
  specs: ['./specs/*.spec.js'],
  framework: 'mocha',
  mochaOpts: { timeout: 60000 },
  reporters: [],
  logLevel: 'warn',
};
