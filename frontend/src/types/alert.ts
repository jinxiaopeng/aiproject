// 指标类型
export enum MetricType {
  CPU = 'cpu',
  MEMORY = 'memory',
  DISK = 'disk',
  NETWORK = 'network',
  SYSTEM_LOAD = 'system_load',
  PROCESS = 'process'
}

// 比较运算符
export enum ComparisonOperator {
  GT = '>',
  GTE = '>=',
  LT = '<',
  LTE = '<=',
  EQ = '==',
  NEQ = '!='
}

// 预警级别
export enum AlertLevel {
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

// 预警状态
export enum AlertStatus {
  NEW = 'new',
  PROCESSING = 'processing',
  HANDLED = 'handled',
  IGNORED = 'ignored'
}

// 通知方式
export type NotifyMethod = 'email' | 'web' | 'sms'

// 预警规则基础接口
export interface AlertRuleBase {
  name: string
  description?: string
  metricType: MetricType
  operator: ComparisonOperator
  threshold: number
  duration: number
  enabled: boolean
  notifyMethods: NotifyMethod[]
  cooldown: number
}

// 创建预警规则请求
export type AlertRuleCreate = AlertRuleBase

// 更新预警规则请求
export type AlertRuleUpdate = Partial<AlertRuleBase>

// 预警规则响应
export interface AlertRule extends AlertRuleBase {
  id: number
  userId: number
  lastTriggered?: string
  createdAt: string
  updatedAt: string
}

// 预警记录
export interface Alert {
  id: number
  userId: number
  ruleId: number
  level: AlertLevel
  title: string
  content: string
  status: AlertStatus
  createdAt: string
  updatedAt: string
  handledAt?: string
}

// 预警规则列表响应
export interface AlertRuleListResponse {
  total: number
  items: AlertRule[]
}

// 预警历史列表响应
export interface AlertHistoryResponse {
  total: number
  items: Alert[]
} 