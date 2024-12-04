interface Config {
  baseUrl: string
  apiTimeout: number
}

interface Configs {
  development: Config
  production: Config
}

const config: Configs = {
  development: {
    baseUrl: '',
    apiTimeout: 5000
  },
  production: {
    baseUrl: 'http://api.wsirp.com',
    apiTimeout: 10000
  }
}

const env = (process.env.NODE_ENV || 'development') as keyof Configs
export default config[env] 