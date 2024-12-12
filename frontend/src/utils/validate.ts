/**
 * 验证邮箱
 * @param email 邮箱地址
 * @returns 是否有效
 */
export const validateEmail = (email: string): boolean => {
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return pattern.test(email)
}

/**
 * 验证密码强度
 * @param password 密码
 * @returns 是否有效
 */
export const validatePassword = (password: string): boolean => {
  // 至少8位，包含大小写字母和数字
  const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
  return pattern.test(password)
}

/**
 * 验证用户名
 * @param username 用户名
 * @returns 是否有效
 */
export const validateUsername = (username: string): boolean => {
  // 4-20位字母、数字或下划线
  const pattern = /^[a-zA-Z0-9_]{4,20}$/
  return pattern.test(username)
}

/**
 * 验证手机号
 * @param phone 手机号
 * @returns 是否有效
 */
export const validatePhone = (phone: string): boolean => {
  const pattern = /^1[3-9]\d{9}$/
  return pattern.test(phone)
}

/**
 * 验证URL
 * @param url URL地址
 * @returns 是否有效
 */
export const validateUrl = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * 验证身份证号
 * @param idCard 身份证号
 * @returns 是否有效
 */
export const validateIdCard = (idCard: string): boolean => {
  const pattern = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
  return pattern.test(idCard)
}

/**
 * 验证是否为空
 * @param value 值
 * @returns 是否为空
 */
export const isEmpty = (value: any): boolean => {
  if (value === null || value === undefined) {
    return true
  }
  if (typeof value === 'string') {
    return value.trim() === ''
  }
  if (Array.isArray(value)) {
    return value.length === 0
  }
  if (typeof value === 'object') {
    return Object.keys(value).length === 0
  }
  return false
}

/**
 * 验证是否为数字
 * @param value 值
 * @returns 是否为数字
 */
export const isNumber = (value: any): boolean => {
  if (typeof value === 'number') {
    return !isNaN(value)
  }
  if (typeof value === 'string') {
    return !isNaN(Number(value))
  }
  return false
}

/**
 * 验证是否为整数
 * @param value 值
 * @returns 是否为整数
 */
export const isInteger = (value: any): boolean => {
  if (!isNumber(value)) {
    return false
  }
  return Number.isInteger(Number(value))
}

/**
 * 验证是否为正数
 * @param value 值
 * @returns 是否为正数
 */
export const isPositive = (value: any): boolean => {
  if (!isNumber(value)) {
    return false
  }
  return Number(value) > 0
}
