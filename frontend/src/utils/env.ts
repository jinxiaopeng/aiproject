/**
 * 获取环境变量
 * @param key 环境变量名
 * @param defaultValue 默认值
 * @returns 环境变量值
 */
export const getEnvVar = (key: string, defaultValue: string = ''): string => {
  const value = import.meta.env[key]
  return value || defaultValue
}

/**
 * 获取API基础URL
 * @returns API基础URL
 */
export const getApiBaseUrl = (): string => {
  return getEnvVar('VITE_API_BASE_URL', '/api')
}

/**
 * 获取当前环境
 * @returns 当前环境
 */
export const getEnvironment = (): string => {
  return getEnvVar('VITE_APP_ENV', 'development')
}

/**
 * 检查是否为开发环境
 * @returns 是否为开发环境
 */
export const isDevelopment = (): boolean => {
  return getEnvironment() === 'development'
}

/**
 * 检查是否为生产环境
 * @returns 是否为生产环境
 */
export const isProduction = (): boolean => {
  return getEnvironment() === 'production'
} 