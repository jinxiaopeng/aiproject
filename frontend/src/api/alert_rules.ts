import request from '@/utils/request'
import type { AlertRule, AlertRuleCreate, AlertRuleUpdate } from '@/types/alert'

// 创建预警规则
export function createAlertRule(data: AlertRuleCreate) {
  return request({
    url: '/monitor/alert-rules',
    method: 'post',
    data
  })
}

// 获取预警规则列表
export function getAlertRules(params: {
  page?: number
  pageSize?: number
  metricType?: string
  enabled?: boolean
}) {
  return request({
    url: '/monitor/alert-rules',
    method: 'get',
    params
  })
}

// 获取单个预警规则
export function getAlertRule(ruleId: number) {
  return request({
    url: `/monitor/alert-rules/${ruleId}`,
    method: 'get'
  })
}

// 更新预警规则
export function updateAlertRule(ruleId: number, data: AlertRuleUpdate) {
  return request({
    url: `/monitor/alert-rules/${ruleId}`,
    method: 'put',
    data
  })
}

// 删除预警规则
export function deleteAlertRule(ruleId: number) {
  return request({
    url: `/monitor/alert-rules/${ruleId}`,
    method: 'delete'
  })
}

// 获取预警规则的触发历史
export function getAlertRuleHistory(ruleId: number, params: {
  page?: number
  pageSize?: number
  startTime?: string
  endTime?: string
}) {
  return request({
    url: `/monitor/alert-rules/${ruleId}/history`,
    method: 'get',
    params
  })
}

// 启用预警规则
export function enableAlertRule(ruleId: number) {
  return request({
    url: `/monitor/alert-rules/${ruleId}/enable`,
    method: 'post'
  })
}

// 禁用预警规则
export function disableAlertRule(ruleId: number) {
  return request({
    url: `/monitor/alert-rules/${ruleId}/disable`,
    method: 'post'
  })
} 