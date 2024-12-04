const config = {
  development: {
    baseUrl: 'http://localhost:3000',
    apiTimeout: 5000
  },
  production: {
    baseUrl: 'http://api.wsirp.com',
    apiTimeout: 10000
  }
}

export default config[process.env.NODE_ENV || 'development'] 