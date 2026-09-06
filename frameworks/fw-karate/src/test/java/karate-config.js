function fn() {
  var config = {
    baseUrl: 'https://jsonplaceholder.typicode.com'
  };
  karate.configure('connectTimeout', 10000);
  karate.configure('readTimeout', 10000);
  karate.log('karate-config loaded, baseUrl =', config.baseUrl);
  return config;
}
