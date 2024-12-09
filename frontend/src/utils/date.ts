import { format, formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

/**
 * 格式化日期
 * @param date - 日期字符串或Date对象
 * @param pattern - 日期格式模板，默认为'yyyy年MM月dd日 HH:mm'
 * @returns 格式化后的日期字符串
 */
export const formatDate = (date: string | Date, pattern = 'yyyy年MM月dd日 HH:mm') => {
  const d = typeof date === 'string' ? new Date(date) : date
  return format(d, pattern, { locale: zhCN })
}

/**
 * 格式化相对时间（例如：3小时前）
 * @param date - 日期字符串或Date对象
 * @returns 相对时间字符串
 */
export const formatRelativeTime = (date: string | Date) => {
  const d = typeof date === 'string' ? new Date(date) : date
  return formatDistanceToNow(d, { addSuffix: true, locale: zhCN })
}

/**
 * 格式化时长（将分钟转换为小时和分钟）
 * @param minutes - 总分钟数
 * @returns 格式化后的时长字符串
 */
export const formatDuration = (minutes: number) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  
  if (hours > 0) {
    return `${hours}小时${mins > 0 ? `${mins}分钟` : ''}`
  }
  return `${mins}分钟`
}

/**
 * 格式化视频时间（将秒数转换为分:秒格式）
 * @param seconds - 视频总秒数
 * @returns 格式化后的视频时间字符串
 */
export const formatVideoTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
} 