exports.config = {
  tests: './codecept/*_test.js',
  output: './reports',
  helpers: {
    REST: {
      endpoint: 'https://jsonplaceholder.typicode.com',
      timeout: 15000,
    },
    JSONResponse: {},
  },
  name: 'fw-taiko-codecept',
  plugins: {
    retryFailedStep: { enabled: false },
  },
};
