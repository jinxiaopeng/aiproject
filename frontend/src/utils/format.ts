import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'

// 设置语言为中文
dayjs.locale('zh-cn')

/**
 * 格式化日期
 * @param date 日期字符串或时间戳
 * @param format 格式化模板
 * @returns 格式化后的日期字符串
 */
export function formatDate(
  date: string | number | Date | undefined,
  format: string = 'YYYY-MM-DD HH:mm:ss'
): string {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * 格式化相对时间
 * @param date 日期字符串或时间戳
 * @returns 相对时间字符串
 */
export function formatRelativeTime(date: string | number | Date | undefined): string {
  if (!date) return '-'
  const now = dayjs()
  const target = dayjs(date)
  const diff = now.diff(target, 'minute')
  
  if (diff < 1) return '刚刚'
  if (diff < 60) return `${diff}分钟前`
  
  const hours = Math.floor(diff / 60)
  if (hours < 24) return `${hours}小时前`
  
  const days = Math.floor(hours / 24)
  if (days < 30) return `${days}天前`
  
  const months = Math.floor(days / 30)
  if (months < 12) return `${months}个月前`
  
  return `${Math.floor(months / 12)}年前`
}

/**
 * 格式化持续时间
 * @param minutes 分钟数
 * @returns 格式化后的持续时间字符串
 */
export function formatDuration(minutes: number): string {
  if (minutes < 60) return `${minutes}分钟`
  
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  
  if (hours < 24) {
    return remainingMinutes > 0
      ? `${hours}小时${remainingMinutes}分钟`
      : `${hours}小时`
  }
  
  const days = Math.floor(hours / 24)
  const remainingHours = hours % 24
  
  let result = `${days}天`
  if (remainingHours > 0) result += `${remainingHours}小时`
  if (remainingMinutes > 0) result += `${remainingMinutes}分钟`
  
  return result
} 