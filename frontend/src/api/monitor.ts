import request from '@/utils/request'

// 监控统计数据接口
export interface MonitorStats {
  loginAlerts: number
  loginPending: number
  loginHandled: number
  operationAlerts: number
  operationPending: number
  operationHandled: number
  securityAlerts: number
  securityPending: number
  securityHandled: number
}

// 获取监控统计数据
export const getMonitorStats = () => {
  return request.get<MonitorStats>('/monitor/stats')
}

// 监控设置接口
export interface MonitorSettings {
  loginAlert: boolean
  operationAlert: boolean
  securityAlert: boolean
  notifyMethods: string[]
}

// 获取监控设置
export const getMonitorSettings = () => {
  return request.get<MonitorSettings>('/monitor/settings')
}

// 更新监控设置
export const updateMonitorSettings = (data: MonitorSettings) => {
  return request.put('/monitor/settings', data)
}

// 预警记录接口
export interface Alert {
  id: number
  time: string
  type: string
  content: string
  status: string
}

export interface AlertListParams {
  page: number
  pageSize: number
  timeRange: string
  alertType?: string
  status?: string[]
}

export interface AlertListResponse {
  items: Alert[]
  total: number
}

// 获取预警记录列表
export const getAlertList = (params: AlertListParams) => {
  return request.get<AlertListResponse>('/monitor/alerts', { params })
}

// 处理预警
export const handleAlertItem = (alertId: number) => {
  return request.put(`/monitor/alerts/${alertId}/handle`)
} 