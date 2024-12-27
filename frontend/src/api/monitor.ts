import request from '@/utils/request'
import type { 
  MonitorStats, 
  SystemMetrics, 
  AlertTrend,
  MonitorLog,
  SecurityAlert,
  AlertAction
} from '@/types/monitor'

// 获取监控统计数据
export const getMonitorStats = () => {
  return request<MonitorStats>({
    url: '/monitor/stats',
    method: 'get'
  })
}

// 获取系统指标数据
export const getSystemMetrics = () => {
  return request<SystemMetrics>({
    url: '/monitor/metrics',
    method: 'get'
  })
}

// 获取告警趋势数据
export const getAlertTrends = (timeRange: string = 'today') => {
  return request<AlertTrend[]>({
    url: '/monitor/trends',
    method: 'get',
    params: { timeRange }
  })
}

// 获取实时日志
export const getRealtimeLogs = (limit: number = 50) => {
  return request<MonitorLog[]>({
    url: '/monitor/logs',
    method: 'get',
    params: { limit }
  })
}

// 获取告警列表
export const getAlerts = (params?: {
  severity?: string
  status?: string
  limit?: number
}) => {
  return request<SecurityAlert[]>({
    url: '/monitor/alerts',
    method: 'get',
    params
  })
}

// 处理告警
export const handleAlert = (action: AlertAction) => {
  return request({
    url: '/monitor/alerts/handle',
    method: 'post',
    data: action
  })
}

// 获取监控设置
export const getMonitorSettings = () => {
  return request({
    url: '/monitor/settings',
    method: 'get'
  })
}

// 更新监控设置
export const updateMonitorSettings = (settings: any) => {
  return request({
    url: '/monitor/settings',
    method: 'post',
    data: settings
  })
}

// 执行快速操作
export const executeQuickAction = (action: string) => {
  return request({
    url: `/monitor/quick-actions/${action}`,
    method: 'post'
  })
} 