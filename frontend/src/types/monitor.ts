// 安全告警类型
export interface SecurityAlert {
  id: string
  type: 'login' | 'injection' | 'xss' | 'file_access' | 'privilege'
  level: 'low' | 'medium' | 'high' | 'critical'
  source: string
  timestamp: string
  details: {
    ip?: string
    user?: string
    action?: string
    payload?: string
    location?: string
    userAgent?: string
  }
  status: 'pending' | 'processing' | 'resolved'
}

// 实验环境告警
export interface LabAlert {
  id: string
  type: 'env_error' | 'resource_limit' | 'timeout' | 'attack_detected'
  labId: string
  labName: string
  userId: string
  username: string
  timestamp: string
  details: {
    error?: string
    resource?: string
    current?: number
    limit?: number
    duration?: number
    attackType?: string
  }
  status: 'active' | 'resolved'
}

// 系统指标
export interface SystemMetrics {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  network: {
    incoming: number
    outgoing: number
  }
  response_time: number
  error_rate: number
  active_users: number
  active_labs: number
  timestamp: string
}

// 统计数据
export interface MonitorStats {
  security: {
    total_alerts: number
    pending_alerts: number
    critical_alerts: number
    recent_attacks: number
    blocked_ips: number
  }
  lab: {
    total_labs: number
    active_labs: number
    error_labs: number
    resource_usage: number
  }
  system: {
    uptime: number
    total_users: number
    active_sessions: number
    avg_response_time: number
  }
}

// 告警趋势数据
export interface AlertTrend {
  timestamp: string
  security_alerts: number
  lab_alerts: number
  system_alerts: number
}

// 实时日志
export interface MonitorLog {
  id: string
  type: 'security' | 'lab' | 'system'
  level: 'info' | 'warning' | 'error' | 'critical'
  message: string
  timestamp: string
  details?: Record<string, any>
}

// 监控规则
export interface MonitorRule {
  id: string
  name: string
  type: 'security' | 'lab' | 'system'
  condition: {
    metric: string
    operator: '>' | '<' | '==' | '!=' | '>=' | '<='
    threshold: number
    duration?: number
  }
  actions: {
    notify: boolean
    notifyChannels: ('email' | 'sms' | 'webhook')[]
    autoHandle: boolean
    handleAction?: 'block_ip' | 'reset_password' | 'disable_user' | 'restart_lab' | 'notify_admin'
  }
  enabled: boolean
  createdAt: string
  updatedAt: string
}

// 告警处理动作
export interface AlertAction {
  type: 'block_ip' | 'reset_password' | 'disable_user' | 'restart_lab' | 'notify_admin'
  alertId: string
  comment?: string
  parameters?: Record<string, any>
} 