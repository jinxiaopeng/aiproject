/**
 * 获取用户头像
 * @param avatar 用户头像URL
 * @returns 完整的头像URL或默认头像
 */
export const getAvatarUrl = (avatar?: string): string => {
  if (!avatar) {
    return 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
  }
  
  if (avatar.startsWith('http')) {
    return avatar
  }
  
  return `${import.meta.env.VITE_API_BASE_URL}${avatar}`
}

/**
 * 获取用户名的第一个字符作为头像
 * @param username 用户名
 * @returns 用户名的第一个字符
 */
export const getNameAvatar = (username: string): string => {
  return username.charAt(0).toUpperCase()
}

/**
 * 生成随机颜色
 * @param seed 种子字符串
 * @returns 颜色值
 */
export const generateAvatarColor = (seed: string): string => {
  let hash = 0
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  const hue = hash % 360
  return `hsl(${hue}, 70%, 60%)`
}

/**
 * 获取用户角色标签
 * @param role 用户角色
 * @returns 角色标签
 */
export const getRoleLabel = (role: string): string => {
  const labels: Record<string, string> = {
    ADMIN: '管理员',
    USER: '普通用户',
    GUEST: '访客'
  }
  return labels[role] || role
}

/**
 * 获取用户状态标签
 * @param status 用户状态
 * @returns 状态标签
 */
export const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    ACTIVE: '正常',
    INACTIVE: '未激活',
    PENDING: '待审核',
    DELETED: '已删除'
  }
  return labels[status] || status
}

/**
 * 获取用户状态类型
 * @param status 用户状态
 * @returns 状态类型
 */
export const getStatusType = (status: string): string => {
  const types: Record<string, string> = {
    ACTIVE: 'success',
    INACTIVE: 'info',
    PENDING: 'warning',
    DELETED: 'danger'
  }
  return types[status] || ''
} 