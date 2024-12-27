# 监控预警系统优化方案

## 一、前端模块化优化

### 1. 组件结构优化
```
src/views/monitor/
├── index.vue                 # 监控预警主页面
├── components/              
│   ├── MonitorOverview/      # 监控概览模块
│   │   ├── index.vue         # 概览主组件
│   │   ├── StatCard.vue      # 统计卡片组件
│   │   └── TrendChart.vue    # 趋势图表组件
│   ├── AlertList/            # 预警列表模块
│   │   ├── index.vue         # 列表主组件
│   │   ├── TableView.vue     # 表格视图组件
│   │   ├── CardView.vue      # 卡片视图组件
│   │   └── FilterBar.vue     # 过滤栏组件
│   ├── AlertDetail/          # 预警详情模块
│   │   ├── index.vue         # 详情主组件
│   │   ├── BasicInfo.vue     # 基本信息组件
│   │   ├── Timeline.vue      # 处理时间线组件
│   │   └── RelatedInfo.vue   # 关联信息组件
│   └── MonitorSettings/      # 监控设置模块
│       ├── index.vue         # 设置主组件
│       ├── RuleForm.vue      # 规则表单组件
│       └── NotifyConfig.vue  # 通知配置组件
└── hooks/                    # 可复用的业务逻辑
    ├── useAlertData.ts       # 预警数据处理钩子
    ├── useMonitorStats.ts    # 监控统计数据钩子
    └── useChartOption.ts     # 图表配置钩子
```

### 2. 状态管理优化
```typescript
// src/store/modules/monitor.ts
interface MonitorState {
  stats: MonitorStats;
  settings: MonitorSettings;
  alerts: Alert[];
  loading: boolean;
}

const monitorStore = defineStore('monitor', {
  state: (): MonitorState => ({
    stats: defaultStats,
    settings: defaultSettings,
    alerts: [],
    loading: false
  }),
  
  actions: {
    async fetchStats() {
      // 获取监控统计数据
    },
    async fetchAlerts() {
      // 获取预警列表数据
    },
    async updateSettings() {
      // 更新监控设置
    }
  }
});
```

### 3. 通用组件抽取
```typescript
// src/components/common/
// AlertTag.vue - 预警标签组件
export interface AlertTagProps {
  type: 'login' | 'operation' | 'security';
  level: 'info' | 'warning' | 'error' | 'critical';
}

// TimeRangePicker.vue - 时间范围选择器
export interface TimeRange {
  start: Date;
  end: Date;
}
```

## 二、模拟数据实现方案

### 1. 模拟数据服务
```typescript
// src/services/mockMonitorService.ts
export class MockMonitorService {
  private lastCpuUsage: number = 35;
  private lastMemoryUsage: number = 45;
  private lastDiskUsage: number = 65;
  private dayStartTime: Date;
  
  constructor() {
    this.dayStartTime = new Date();
    this.dayStartTime.setHours(0, 0, 0, 0);
  }

  // 生成监控统计数据
  async getMonitorStats(): Promise<MonitorStats> {
    const currentHour = new Date().getHours();
    const isWorkHours = currentHour >= 9 && currentHour < 18;
    const isLunchTime = currentHour >= 12 && currentHour < 14;

    return {
      // 登录预警数据 - 工作时间较多，非工作时间较少
      loginAlerts: this.generateLoginAlerts(isWorkHours),
      loginPending: this.generatePendingAlerts(isWorkHours, 'login'),
      loginHandled: this.generateHandledAlerts(isWorkHours, 'login'),
      
      // 操作预警数据 - 主要在工作时间产生
      operationAlerts: this.generateOperationAlerts(isWorkHours, isLunchTime),
      operationPending: this.generatePendingAlerts(isWorkHours, 'operation'),
      operationHandled: this.generateHandledAlerts(isWorkHours, 'operation'),
      
      // 安全预警数据 - 非工作时间偏多
      securityAlerts: this.generateSecurityAlerts(isWorkHours),
      securityPending: this.generatePendingAlerts(!isWorkHours, 'security'),
      securityHandled: this.generateHandledAlerts(!isWorkHours, 'security')
    };
  }

  private generateLoginAlerts(isWorkHours: boolean): number {
    // 工作时间：10-50，非工作时间：5-20
    return isWorkHours 
      ? this.randomNumber(10, 50)
      : this.randomNumber(5, 20);
  }

  private generateOperationAlerts(isWorkHours: boolean, isLunchTime: boolean): number {
    if (!isWorkHours) return this.randomNumber(3, 10);
    if (isLunchTime) return this.randomNumber(5, 15);
    return this.randomNumber(15, 60);
  }

  private generateSecurityAlerts(isWorkHours: boolean): number {
    // 非工作时间安全预警更多
    return isWorkHours
      ? this.randomNumber(5, 20)
      : this.randomNumber(15, 40);
  }

  private generatePendingAlerts(isActive: boolean, type: string): number {
    const base = isActive ? 0.3 : 0.5; // 活跃时间未处理率较低
    const total = this.getAlertsByType(type);
    return Math.floor(total * base);
  }

  private generateHandledAlerts(isActive: boolean, type: string): number {
    const base = isActive ? 0.6 : 0.4; // 活跃时间处理率较高
    const total = this.getAlertsByType(type);
    return Math.floor(total * base);
  }

  private getAlertsByType(type: string): number {
    switch(type) {
      case 'login': return this.generateLoginAlerts(this.isWorkHours());
      case 'operation': return this.generateOperationAlerts(this.isWorkHours(), this.isLunchTime());
      case 'security': return this.generateSecurityAlerts(this.isWorkHours());
      default: return 0;
    }
  }

  // 生成预警列表数据
  async getAlertList(params: AlertListParams): Promise<AlertListResponse> {
    const alerts = this.generateMockAlerts(params);
    return {
      items: alerts,
      total: this.calculateTotalAlerts(params)
    };
  }

  private generateMockAlerts(params: AlertListParams): Alert[] {
    const isWorkHours = this.isWorkHours();
    const currentTime = new Date();
    
    return Array(params.pageSize).fill(null).map((_, index) => ({
      id: this.generateAlertId(params.page, index),
      type: this.getAlertTypeByTime(isWorkHours),
      level: this.getAlertLevelByType(isWorkHours),
      content: this.generateAlertContent(isWorkHours),
      status: this.getAlertStatus(isWorkHours),
      time: this.generateAlertTime(currentTime, params.timeRange),
      handleTime: this.generateHandleTime(currentTime),
      source: this.generateAlertSource(),
      impact: this.generateAlertImpact(),
      handler: this.generateHandler(isWorkHours)
    }));
  }

  private getAlertTypeByTime(isWorkHours: boolean): string {
    const weights = isWorkHours
      ? { login: 0.4, operation: 0.4, security: 0.2 }
      : { login: 0.2, operation: 0.1, security: 0.7 };
    
    const rand = Math.random();
    if (rand < weights.login) return 'login';
    if (rand < weights.login + weights.operation) return 'operation';
    return 'security';
  }

  private getAlertLevelByType(isWorkHours: boolean): string {
    const weights = isWorkHours
      ? { info: 0.4, warning: 0.3, error: 0.2, critical: 0.1 }
      : { info: 0.2, warning: 0.3, error: 0.3, critical: 0.2 };

    const rand = Math.random();
    if (rand < weights.info) return 'info';
    if (rand < weights.info + weights.warning) return 'warning';
    if (rand < weights.info + weights.warning + weights.error) return 'error';
    return 'critical';
  }

  private generateAlertContent(isWorkHours: boolean): string {
    const type = this.getAlertTypeByTime(isWorkHours);
    const contents = {
      login: [
        `检测到异常登录，IP: ${this.randomIP()}, 尝试次数: ${this.randomNumber(5, 15)}次`,
        `发现暴力破解尝试，IP: ${this.randomIP()}, 影响账户数: ${this.randomNumber(3, 8)}`,
        `异地登录，位置: ${this.randomLocation()}, IP: ${this.randomIP()}`,
        `连续登录失败，用户: ${this.randomUsername()}, 失败次��: ${this.randomNumber(3, 10)}`
      ],
      operation: [
        `用户 ${this.randomUsername()} 批量删除了 ${this.randomNumber(100, 1000)} 条记录`,
        `检测到敏感配置修改，修改人: ${this.randomUsername()}, 影响范围: ${this.randomScope()}`,
        `高危操作执行，操作人: ${this.randomUsername()}, 操作类型: ${this.randomOperation()}`,
        `未经授权的数据导出，用户: ${this.randomUsername()}, 数据量: ${this.randomNumber(1000, 5000)}条`
      ],
      security: [
        `检测到可疑的网络扫描，来源IP: ${this.randomIP()}, 扫描端口数: ${this.randomNumber(20, 100)}`,
        `发现未授权的API访问尝试，接口: ${this.randomAPI()}, IP: ${this.randomIP()}`,
        `检测到SQL注入尝试，来源IP: ${this.randomIP()}, 目标: ${this.randomTable()}`,
        `可疑文件上传，用户: ${this.randomUsername()}, 文件类型: ${this.randomFileType()}`
      ]
    };

    const contentList = contents[type];
    return contentList[Math.floor(Math.random() * contentList.length)];
  }

  private randomLocation(): string {
    const locations = [
      '北京市', '上海市', '广州市', '深圳市', '杭州市',
      '美国-加利福尼亚', '英国-伦敦', '日本-东京', '新加坡',
      '俄罗斯-莫斯科', '德国-柏林', '加拿大-多伦多'
    ];
    return locations[Math.floor(Math.random() * locations.length)];
  }

  private randomScope(): string {
    const scopes = [
      '系统核心配置', '用户权限设置', '安全策略配置', '网络设置',
      '数据库配置', '缓存配置', '日志级别设置', '告警规则设置'
    ];
    return scopes[Math.floor(Math.random() * scopes.length)];
  }

  private randomOperation(): string {
    const operations = [
      '数据库备份删除', '用户权限变更', '系统配置重置', '防火墙规则修改',
      '服务器重启', '密钥轮换', '证书更新', '路由规则变更'
    ];
    return operations[Math.floor(Math.random() * operations.length)];
  }

  private randomAPI(): string {
    const apis = [
      '/api/admin/users', '/api/system/config', '/api/security/rules',
      '/api/data/export', '/api/logs/clear', '/api/backup/delete',
      '/api/auth/keys', '/api/monitor/disable'
    ];
    return apis[Math.floor(Math.random() * apis.length)];
  }

  private randomTable(): string {
    const tables = [
      'users', 'permissions', 'audit_logs', 'system_config',
      'sensitive_data', 'financial_records', 'customer_info', 'employee_data'
    ];
    return tables[Math.floor(Math.random() * tables.length)];
  }

  private randomFileType(): string {
    const types = [
      '.php', '.jsp', '.asp', '.exe', '.sh', '.bat',
      '.dll', '.so', '.cmd', '.msi'
    ];
    return types[Math.floor(Math.random() * types.length)];
  }

  private isWorkHours(): boolean {
    const hour = new Date().getHours();
    return hour >= 9 && hour < 18;
  }

  private isLunchTime(): boolean {
    const hour = new Date().getHours();
    return hour >= 12 && hour < 14;
  }

  // ... [其他辅助方法保持不变]
}
```

### 2. 资源监控模拟
```typescript
// src/services/mockResourceMonitor.ts
export class MockResourceMonitor {
  private baseMemoryUsage: number = 45;
  private baseCpuUsage: number = 30;
  private baseDiskUsage: number = 65;
  private lastUpdateTime: Date = new Date();
  private systemStartTime: Date = new Date();
  private processCount: number = 120;
  private historicalData: Map<string, Array<{ time: Date, value: number }>> = new Map();

  constructor() {
    // 初始化历史数据存储
    ['cpu', 'memory', 'disk', 'network'].forEach(metric => {
      this.historicalData.set(metric, []);
    });
  }

  // 模拟资源使用数据
  async getResourceUsage(): Promise<ResourceUsage> {
    const currentTime = new Date();
    const isWorkHours = this.isWorkHours();
    const isHighLoadTime = this.isHighLoadTime();
    
    const usage = {
      cpu: this.generateCpuUsage(isWorkHours, isHighLoadTime),
      memory: this.generateMemoryUsage(isWorkHours),
      disk: this.generateDiskUsage(),
      network: this.generateNetworkUsage(isWorkHours, isHighLoadTime),
      process: this.generateProcessStats(),
      system: this.generateSystemStats()
    };

    // 更新历史数据
    this.updateHistoricalData(usage);
    
    return usage;
  }

  private generateCpuUsage(isWorkHours: boolean, isHighLoad: boolean): CpuUsage {
    let baseLoad = isWorkHours ? 40 : 25;
    if (isHighLoad) baseLoad += 20;

    // 生成每个核心的使用率
    const cores = Array(8).fill(0).map(() => {
      let coreUsage = baseLoad + (Math.random() * 30 - 15);
      if (Math.random() < 0.1) { // 10%概率出现峰值
        coreUsage = Math.random() * 15 + 80;
      }
      return Math.min(Math.max(coreUsage, 0), 100);
    });

    // 计算系统负载
    const loadAvg = [
      baseLoad / 25 + Math.random(), // 1分钟负载
      baseLoad / 30 + Math.random(), // 5分钟负载
      baseLoad / 35 + Math.random()  // 15分钟负载
    ];

    return {
      total: cores.reduce((a, b) => a + b, 0) / cores.length,
      cores: cores,
      loadAvg: loadAvg,
      processes: {
        running: this.randomNumber(3, 8),
        sleeping: this.randomNumber(100, 150),
        stopped: this.randomNumber(0, 2),
        zombie: Math.random() < 0.05 ? 1 : 0 // 5%概率出现僵尸进程
      }
    };
  }

  private generateMemoryUsage(isWorkHours: boolean): MemoryUsage {
    // 基础内存使用率在工作时间较高
    const baseUsage = isWorkHours ? 45 : 35;
    
    // 内存使用缓慢变化
    this.baseMemoryUsage += (Math.random() - 0.5) * 2;
    this.baseMemoryUsage = Math.min(Math.max(this.baseMemoryUsage, baseUsage - 10, 40), baseUsage + 20, 75);

    const totalMemory = 16 * 1024; // 16GB
    const usedMemory = Math.floor(totalMemory * (this.baseMemoryUsage / 100));

    return {
      total: totalMemory,
      used: usedMemory,
      free: totalMemory - usedMemory,
      cached: Math.floor(totalMemory * 0.3),
      buffers: Math.floor(totalMemory * 0.1),
      swap: {
        total: 8 * 1024,
        used: Math.floor((8 * 1024) * 0.1), // 通常swap使用率较低
        free: Math.floor((8 * 1024) * 0.9)
      }
    };
  }

  private generateDiskUsage(): DiskUsage {
    // 磁盘使用率缓慢增长
    this.baseDiskUsage += Math.random() * 0.1;
    this.baseDiskUsage = Math.min(this.baseDiskUsage, 95);

    const totalSpace = 500 * 1024; // 500GB
    const usedSpace = Math.floor(totalSpace * (this.baseDiskUsage / 100));

    return {
      volumes: [
        {
          mount: '/',
          total: totalSpace * 0.3,
          used: usedSpace * 0.3,
          free: (totalSpace - usedSpace) * 0.3,
          usage: this.baseDiskUsage
        },
        {
          mount: '/data',
          total: totalSpace * 0.7,
          used: usedSpace * 0.7,
          free: (totalSpace - usedSpace) * 0.7,
          usage: this.baseDiskUsage
        }
      ],
      io: {
        read: this.generateDiskIO(true),
        write: this.generateDiskIO(false),
        iops: this.randomNumber(100, 1000)
      }
    };
  }

  private generateDiskIO(isRead: boolean): DiskIOStats {
    const isWorkHours = this.isWorkHours();
    const baseIO = isWorkHours ? 20 : 10;
    const multiplier = isRead ? 1 : 1.5; // 写入通常比读取大

    return {
      operations: this.randomNumber(baseIO * 50, baseIO * 100),
      bytes: this.randomNumber(baseIO * 1024 * 1024, baseIO * 2 * 1024 * 1024) * multiplier,
      time: this.randomNumber(100, 500) // IO时间（毫秒）
    };
  }

  private generateNetworkUsage(isWorkHours: boolean, isHighLoad: boolean): NetworkUsage {
    let baseTraffic = isWorkHours ? 5120 : 2048; // KB/s
    if (isHighLoad) baseTraffic *= 1.5;

    return {
      interfaces: [
        {
          name: 'eth0',
          incoming: {
            bytes: this.randomNumber(baseTraffic * 0.8, baseTraffic * 1.2),
            packets: this.randomNumber(1000, 5000),
            errors: Math.random() < 0.01 ? this.randomNumber(1, 5) : 0,
            dropped: Math.random() < 0.02 ? this.randomNumber(1, 10) : 0
          },
          outgoing: {
            bytes: this.randomNumber(baseTraffic * 0.4, baseTraffic * 0.8),
            packets: this.randomNumber(800, 4000),
            errors: Math.random() < 0.01 ? this.randomNumber(1, 5) : 0,
            dropped: Math.random() < 0.02 ? this.randomNumber(1, 10) : 0
          }
        }
      ],
      connections: {
        total: this.randomNumber(isWorkHours ? 1000 : 500, isWorkHours ? 2000 : 1000),
        established: this.randomNumber(isWorkHours ? 800 : 400, isWorkHours ? 1600 : 800),
        timeWait: this.randomNumber(50, 200),
        closeWait: this.randomNumber(10, 50)
      }
    };
  }

  private generateProcessStats(): ProcessStats {
    // 进程数量缓慢变化
    this.processCount += Math.random() < 0.5 ? 1 : -1;
    this.processCount = Math.min(Math.max(this.processCount, 100), 150);

    return {
      total: this.processCount,
      types: {
        user: Math.floor(this.processCount * 0.6),
        system: Math.floor(this.processCount * 0.3),
        kernel: Math.floor(this.processCount * 0.1)
      },
      topCpu: this.generateTopProcesses('cpu'),
      topMemory: this.generateTopProcesses('memory')
    };
  }

  private generateTopProcesses(type: 'cpu' | 'memory'): ProcessInfo[] {
    const processes = [
      { name: 'java', cmd: 'java -jar app.jar' },
      { name: 'nginx', cmd: 'nginx: master process' },
      { name: 'mysql', cmd: 'mysqld' },
      { name: 'redis-server', cmd: 'redis-server *:6379' },
      { name: 'node', cmd: 'node server.js' }
    ];

    return processes.map(p => ({
      pid: this.randomNumber(1000, 9999),
      name: p.name,
      cmd: p.cmd,
      user: Math.random() < 0.8 ? 'app' : 'root',
      cpu: type === 'cpu' ? this.randomNumber(0, 100) : this.randomNumber(0, 10),
      memory: type === 'memory' ? this.randomNumber(0, 30) : this.randomNumber(0, 5),
      state: Math.random() < 0.9 ? 'S' : 'R'
    })).sort((a, b) => b[type] - a[type]).slice(0, 5);
  }

  private generateSystemStats(): SystemStats {
    const uptime = (new Date().getTime() - this.systemStartTime.getTime()) / 1000;
    
    return {
      uptime: uptime,
      bootTime: this.systemStartTime.getTime(),
      hostname: 'prod-app-server-01',
      os: {
        platform: 'linux',
        distro: 'Ubuntu 20.04.3 LTS',
        release: '5.4.0-88-generic',
        arch: 'x64'
      },
      time: {
        current: new Date().getTime(),
        timezone: 'Asia/Shanghai',
        timezoneName: 'China Standard Time'
      }
    };
  }

  private updateHistoricalData(usage: ResourceUsage): void {
    const currentTime = new Date();
    
    // 保存最近6小时的数据，每5分钟一个点
    const maxDataPoints = (6 * 60) / 5;
    
    Object.entries(usage).forEach(([metric, value]) => {
      const data = this.historicalData.get(metric) || [];
      data.push({ time: currentTime, value: typeof value === 'object' ? value.total : value });
      
      // 只保留最近的数据点
      if (data.length > maxDataPoints) {
        data.shift();
      }
      
      this.historicalData.set(metric, data);
    });
  }

  private isWorkHours(): boolean {
    const hour = new Date().getHours();
    return hour >= 9 && hour < 18;
  }

  private isHighLoadTime(): boolean {
    const hour = new Date().getHours();
    // 上午10-11点，下午3-4点是高峰期
    return (hour >= 10 && hour < 11) || (hour >= 15 && hour < 16);
  }

  private randomNumber(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  // 获取历史数据
  async getHistoricalData(metric: string, duration: string): Promise<Array<{ time: Date, value: number }>> {
    return this.historicalData.get(metric) || [];
  }
}

// 源使用类型定义
interface CpuUsage {
  total: number;
  cores: number[];
  loadAvg: number[];
  processes: {
    running: number;
    sleeping: number;
    stopped: number;
    zombie: number;
  };
}

interface MemoryUsage {
  total: number;
  used: number;
  free: number;
  cached: number;
  buffers: number;
  swap: {
    total: number;
    used: number;
    free: number;
  };
}

interface DiskUsage {
  volumes: Array<{
    mount: string;
    total: number;
    used: number;
    free: number;
    usage: number;
  }>;
  io: {
    read: DiskIOStats;
    write: DiskIOStats;
    iops: number;
  };
}

interface DiskIOStats {
  operations: number;
  bytes: number;
  time: number;
}

interface NetworkUsage {
  interfaces: Array<{
    name: string;
    incoming: NetworkStats;
    outgoing: NetworkStats;
  }>;
  connections: {
    total: number;
    established: number;
    timeWait: number;
    closeWait: number;
  };
}

interface NetworkStats {
  bytes: number;
  packets: number;
  errors: number;
  dropped: number;
}

interface ProcessStats {
  total: number;
  types: {
    user: number;
    system: number;
    kernel: number;
  };
  topCpu: ProcessInfo[];
  topMemory: ProcessInfo[];
}

interface ProcessInfo {
  pid: number;
  name: string;
  cmd: string;
  user: string;
  cpu: number;
  memory: number;
  state: string;
}

interface SystemStats {
  uptime: number;
  bootTime: number;
  hostname: string;
  os: {
    platform: string;
    distro: string;
    release: string;
    arch: string;
  };
  time: {
    current: number;
    timezone: string;
    timezoneName: string;
  };
}
```

### 3. 配置切换机制
```typescript
// src/config/monitor.ts
export const MONITOR_CONFIG = {
  useMockData: true,  // 是否使用模拟数据
  mockDataInterval: 5000,  // 模拟数据更新间隔（毫秒）
  alertGenerationRate: 0.2,  // 预警生成概率
  resourceUpdateInterval: 3000,  // 资源监控数据更新间隔
};

// src/services/monitorService.ts
export const getMonitorService = () => {
  return MONITOR_CONFIG.useMockData ? new MockMonitorService() : new RealMonitorService();
};
```

### 3. 预警规则模拟
```typescript
// src/services/mockAlertRuleService.ts
export class MockAlertRuleService {
  private rules: Map<string, AlertRule[]> = new Map();
  private ruleTemplates: AlertRuleTemplate[] = [];
  private evaluationHistory: Map<string, AlertEvaluation[]> = new Map();

  constructor() {
    this.initializeRuleTemplates();
    this.initializeDefaultRules();
  }

  // 初始化预警规则模板
  private initializeRuleTemplates(): void {
    this.ruleTemplates = [
      // CPU相关规则模板
      {
        id: 'tpl_cpu_high',
        name: 'CPU使用率过高',
        description: '监控CPU使用率是否超过阈值',
        metric: 'cpu_usage',
        defaultThreshold: 80,
        defaultDuration: 300, // 5分钟
        defaultCooldown: 1800, // 30分钟
        severity: 'high',
        template: {
          condition: 'cpu_usage > {threshold} for {duration}s',
          message: 'CPU使用率持续{duration}秒超过{threshold}%，当前值：{value}%',
          suggestion: [
            '检查是否有异常进程占用CPU',
            '查看系统负载情况',
            '考虑是否需要扩容'
          ]
        }
      },
      {
        id: 'tpl_cpu_load',
        name: '系统负载过高',
        description: '监控系统负载是否超过CPU核心数',
        metric: 'system_load',
        defaultThreshold: 'cores * 0.8',
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'high',
        template: {
          condition: 'system_load > {threshold} for {duration}s',
          message: '系统负载持续{duration}秒超过{threshold}，当前值：{value}',
          suggestion: [
            '检查系统进程状态',
            '分析业务请求量',
            '评估��统容量'
          ]
        }
      },

      // 内存相关规则模板
      {
        id: 'tpl_memory_high',
        name: '内存使用率过高',
        description: '监控内存使用率是否超过阈值',
        metric: 'memory_usage',
        defaultThreshold: 85,
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'high',
        template: {
          condition: 'memory_usage > {threshold} for {duration}s',
          message: '内存使用率持续{duration}秒超过{threshold}%，当前值：{value}%',
          suggestion: [
            '检查内存占用最高的进程',
            '分析是否存在内存泄漏',
            '考虑增加内存容量'
          ]
        }
      },
      {
        id: 'tpl_memory_leak',
        name: '疑似内存泄漏',
        description: '监控内存使用持续增长情况',
        metric: 'memory_trend',
        defaultThreshold: '10%/hour',
        defaultDuration: 3600,
        defaultCooldown: 7200,
        severity: 'critical',
        template: {
          condition: 'memory_growth_rate > {threshold} for {duration}s',
          message: '内存使用量持续{duration}秒增长超过{threshold}，疑似存在内存泄漏',
          suggestion: [
            '检查应用程序内存使用情况',
            '分析内存增长趋势',
            '考虑重启相关服务'
          ]
        }
      },

      // 磁盘相关规则模板
      {
        id: 'tpl_disk_space',
        name: '磁盘空间不足',
        description: '监控磁盘使用率是否超过阈值',
        metric: 'disk_usage',
        defaultThreshold: 85,
        defaultDuration: 0,
        defaultCooldown: 3600,
        severity: 'high',
        template: {
          condition: 'disk_usage > {threshold}',
          message: '磁盘使用率超过{threshold}%，当前值：{value}%',
          suggestion: [
            '清理临时文件和日志',
            '分析磁盘占用情况',
            '考虑扩容或迁移数据'
          ]
        }
      },
      {
        id: 'tpl_disk_io',
        name: '磁盘IO负载过高',
        description: '监控磁盘IO使用率是否超过阈值',
        metric: 'disk_io',
        defaultThreshold: 85,
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'high',
        template: {
          condition: 'disk_io > {threshold} for {duration}s',
          message: '磁盘IO使用率持续{duration}秒超过{threshold}%，当前值：{value}%',
          suggestion: [
            '检查IO密集型进程',
            '优化磁盘读写操作',
            '考虑使用SSD或优���存储架构'
          ]
        }
      },

      // 网络相关规则模板
      {
        id: 'tpl_network_traffic',
        name: '网络流量异常',
        description: '监控网络流量是否超过阈值',
        metric: 'network_traffic',
        defaultThreshold: '100MB/s',
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'medium',
        template: {
          condition: 'network_traffic > {threshold} for {duration}s',
          message: '网络流量持续{duration}秒超过{threshold}，当前值：{value}',
          suggestion: [
            '分析网络流量来源',
            '检查是否存在异常访问',
            '评估带宽使用情况'
          ]
        }
      },
      {
        id: 'tpl_network_error',
        name: '网络错误率过高',
        description: '监控网络接口错误率是否超过阈值',
        metric: 'network_error_rate',
        defaultThreshold: 1,
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'high',
        template: {
          condition: 'network_error_rate > {threshold} for {duration}s',
          message: '网络错误率持续{duration}秒超过{threshold}%，当前值：{value}%',
          suggestion: [
            '检查网络连接状态',
            '分析网络错误类型',
            '排查网络设备问题'
          ]
        }
      },

      // 应用相关规则模板
      {
        id: 'tpl_service_error',
        name: '服务错误率过高',
        description: '监控服务错误率是否超过阈值',
        metric: 'error_rate',
        defaultThreshold: 5,
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'high',
        template: {
          condition: 'error_rate > {threshold} for {duration}s',
          message: '服务错误率持续{duration}秒超过{threshold}%，当前值：{value}%',
          suggestion: [
            '检查错误日志',
            '分析错误类型分布',
            '评估服务健康状态'
          ]
        }
      },
      {
        id: 'tpl_service_latency',
        name: '服务响应时间过高',
        description: '监控服务响应时间是否超过阈值',
        metric: 'response_time',
        defaultThreshold: 1000,
        defaultDuration: 300,
        defaultCooldown: 1800,
        severity: 'high',
        template: {
          condition: 'response_time > {threshold} for {duration}s',
          message: '服务响应时间持续{duration}秒超过{threshold}ms，当前值：{value}ms',
          suggestion: [
            '检查服务负载情况',
            '分析慢请��原因',
            '优化服务性能'
          ]
        }
      }
    ];
  }

  // 初始化默认规则
  private initializeDefaultRules(): void {
    // 为每个规则模板创建默认规则
    this.ruleTemplates.forEach(template => {
      const rule: AlertRule = {
        id: `rule_${template.id}`,
        name: template.name,
        description: template.description,
        metric: template.metric,
        threshold: template.defaultThreshold,
        duration: template.defaultDuration,
        cooldown: template.defaultCooldown,
        severity: template.severity,
        enabled: true,
        template: template.template,
        lastTriggered: null,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      const metricRules = this.rules.get(template.metric) || [];
      metricRules.push(rule);
      this.rules.set(template.metric, metricRules);
    });
  }

  // 评估指标是否触发预警
  async evaluateMetric(metric: string, value: number | string): Promise<AlertEvaluation[]> {
    const metricRules = this.rules.get(metric) || [];
    const evaluations: AlertEvaluation[] = [];

    for (const rule of metricRules) {
      if (!rule.enabled) continue;

      // 检查冷却时间
      if (rule.lastTriggered) {
        const cooldownEnd = new Date(rule.lastTriggered.getTime() + rule.cooldown * 1000);
        if (new Date() < cooldownEnd) continue;
      }

      // 评估规则
      const triggered = this.evaluateRule(rule, value);
      if (triggered) {
        const evaluation: AlertEvaluation = {
          ruleId: rule.id,
          metric: metric,
          value: value,
          timestamp: new Date(),
          triggered: true,
          message: this.generateAlertMessage(rule, value)
        };

        evaluations.push(evaluation);
        rule.lastTriggered = new Date();
      }
    }

    // 保存评估历史
    const history = this.evaluationHistory.get(metric) || [];
    history.push(...evaluations);
    if (history.length > 1000) { // 只保留最近1000条记录
      history.splice(0, history.length - 1000);
    }
    this.evaluationHistory.set(metric, history);

    return evaluations;
  }

  // 评估单个规则
  private evaluateRule(rule: AlertRule, value: number | string): boolean {
    const threshold = this.parseThreshold(rule.threshold);
    const currentValue = typeof value === 'string' ? parseFloat(value) : value;

    if (typeof threshold === 'number' && typeof currentValue === 'number') {
      switch (rule.template.condition) {
        case 'gt':
          return currentValue > threshold;
        case 'gte':
          return currentValue >= threshold;
        case 'lt':
          return currentValue < threshold;
        case 'lte':
          return currentValue <= threshold;
        case 'eq':
          return currentValue === threshold;
        default:
          return false;
      }
    }

    return false;
  }

  // 解析阈值
  private parseThreshold(threshold: any): number {
    if (typeof threshold === 'number') return threshold;
    if (typeof threshold === 'string') {
      // 处理特殊阈值格式，如 "cores * 0.8" 或 "10%/hour"
      // 这里需要根据具体需求实现解析逻辑
      return parseFloat(threshold);
    }
    return 0;
  }

  // 生成预警消息
  private generateAlertMessage(rule: AlertRule, value: number | string): string {
    let message = rule.template.message;
    message = message.replace('{threshold}', rule.threshold.toString());
    message = message.replace('{duration}', rule.duration.toString());
    message = message.replace('{value}', value.toString());
    return message;
  }

  // 获取规则模板
  async getRuleTemplates(): Promise<AlertRuleTemplate[]> {
    return this.ruleTemplates;
  }

  // 获取规则列表
  async getRules(metric?: string): Promise<AlertRule[]> {
    if (metric) {
      return this.rules.get(metric) || [];
    }
    return Array.from(this.rules.values()).flat();
  }

  // 获取评估历史
  async getEvaluationHistory(metric: string, limit: number = 100): Promise<AlertEvaluation[]> {
    const history = this.evaluationHistory.get(metric) || [];
    return history.slice(-limit);
  }
}

// 类型定义
interface AlertRuleTemplate {
  id: string;
  name: string;
  description: string;
  metric: string;
  defaultThreshold: number | string;
  defaultDuration: number;
  defaultCooldown: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  template: {
    condition: string;
    message: string;
    suggestion: string[];
  };
}

interface AlertRule {
  id: string;
  name: string;
  description: string;
  metric: string;
  threshold: number | string;
  duration: number;
  cooldown: number;
  severity: string;
  enabled: boolean;
  template: {
    condition: string;
    message: string;
    suggestion: string[];
  };
  lastTriggered: Date | null;
  createdAt: Date;
  updatedAt: Date;
}

interface AlertEvaluation {
  ruleId: string;
  metric: string;
  value: number | string;
  timestamp: Date;
  triggered: boolean;
  message: string;
}
```

## 三、实现步骤

1. 前端优化实现步骤：
   - 按照新的组件结构重组织代码
   - 实现通用组件
   - 配置状态管理
   - 优化数据流转

2. 模拟数据实现步骤：
   - 创建模拟数据服务类
   - 实现资源监控模拟
   - 配置切换机制
   - 调试和验证

3. 注意事项：
   - 保持模拟数据的真实性和合理性
   - 确保模拟数据服务接口与真实服务一致
   - 添加必要的日志和错误处理
   - 考虑性能和内存占用

## 四、后续优化建议

1. 数据可视化增强：
   - 添加更多类型的统计图表
   - 支持数据下钻分析
   - 添加趋势分析功能

2. 交互体验优化：
   - 添加预警声音提醒
   - 支持预警消息推送
   - 优化移动端适配

3. 性能优化：
   - 实现��据缓存机制
   - 优化大量数据的渲染
   - 添加虚拟滚动

4. 功能扩展：
   - 支持自定义预警规则
   - 添加预警知识库
   - 集成机器学习预测 

## 五、数据分析和可视化优化

### 1. 监控预警可视化

#### 1.1 预警分布分析
```typescript
// src/components/monitor/AlertDistribution.vue
interface AlertDistributionProps {
  // 预警分布数据
  distribution: {
    type: string;      // 预警类型
    count: number;     // 预警数量
    severity: string;  // 严重程度
    status: string;    // 处理状态
    source: string;    // 来源系统
    target: string;    // 影响对象
  }[];
  // 时间范围
  timeRange: 'day' | 'week' | 'month';
}
```

- 多维度预警分布热力图
  - 按时间和类型的分布
  - 按严重程度和状态的分布
  - 按来源系统和影响对象的分布

- 预警趋势分析
  - 不同类型预警的时间趋势
  - 预警数量环比/同比分析
  - 高发时段分析

#### 1.2 预警关联分析
```typescript
// src/components/monitor/AlertCorrelation.vue
interface AlertCorrelationProps {
  // 预警关联数据
  correlations: {
    sourceAlert: string;    // 源预警
    targetAlert: string;    // 目标预警
    relationship: string;   // 关联关系
    confidence: number;     // 关联置信度
    timeWindow: number;     // 时间窗口
  }[];
}
```

- 预警关联网络图
  - 展示预警间的关联关系
  - 关联强度和方向的可视化
  - 关键路径分析

- 时序关联分析
  - 预警触发的时序关系
  - 关联规则的时间窗口
  - 因果链路追踪

#### 1.3 预警处理分析
```typescript
// src/components/monitor/AlertHandling.vue
interface AlertHandlingProps {
  // 预警处理数据
  handling: {
    alertId: string;        // 预警ID
    responseTime: number;   // 响应时间
    handleTime: number;     // 处理时间
    steps: {               // 处理步骤
      step: string;        // 步骤名称
      duration: number;    // 持续时间
      status: string;      // 状态
    }[];
    result: string;        // 处理结果
  }[];
}
```

- 处理时效性分析
  - 平均响应时间统计
  - 处理时长分布
  - 超时预警分析

- 处理流程分析
  - 处理步骤时间分布
  - 步骤状态统计
  - 瓶颈环节识别

### 2. 资源监控可视化

#### 2.1 系统资源仪表盘
```typescript
// src/components/monitor/ResourceDashboard.vue
interface ResourceMetrics {
  // CPU指标
  cpu: {
    usage: number;         // 使用率
    load: number[];        // 负载
    cores: number[];       // 核心使用率
  };
  // 内存指标
  memory: {
    total: number;         // 总量
    used: number;         // 已用
    free: number;         // 空闲
    cached: number;       // 缓存
    swap: {              // 交换分区
      total: number;
      used: number;
    };
  };
  // 磁盘指标
  disk: {
    volumes: {           // 磁盘卷
      path: string;
      total: number;
      used: number;
      iops: number;
    }[];
    io: {               // IO统计
      read: number;
      write: number;
      await: number;
    };
  };
  // 网络指标
  network: {
    interfaces: {        // 网络接口
      name: string;
      in: number;
      out: number;
      errors: number;
    }[];
    connections: {      // 连接统计
      total: number;
      established: number;
      waiting: number;
    };
  };
}
```

- 实时监控仪表盘
  - CPU/内存/磁盘/网络使用率仪表盘
  - 关键指标趋势图
  - 资源告警阈值线

- 资源使用分布
  - 进程资源占用排行
  - 资源分配情况
  - 容量利用率分析

#### 2.2 性能分析图表
```typescript
// src/components/monitor/PerformanceAnalysis.vue
interface PerformanceData {
  // 性能指标
  metrics: {
    name: string;          // 指标名称
    value: number;         // 当前值
    threshold: number;     // 阈值
    trend: number[];       // 趋势数据
    baseline: number;      // 基线值
  }[];
  // 性能事件
  events: {
    time: Date;           // 发生时间
    type: string;         // 事件类型
    impact: string;       // 影响程度
    duration: number;     // 持续时间
  }[];
}
```

- 性能趋势分析
  - 多指标联合分析
  - 性能劣化检测
  - 异常模式识别

- 性能瓶颈分析
  - 资源竞争分析
  - 性能事件关联
  - 容量瓶颈预测

#### 2.3 健康状态评估
```typescript
// src/components/monitor/HealthAssessment.vue
interface HealthScore {
  // 健康评分
  overall: number;        // 总体评分
  dimensions: {          // 维度评分
    name: string;        // 维度名称
    score: number;       // 评分
    weight: number;      // 权重
    factors: {          // 影响因素
      name: string;     // 因素名称
      impact: number;   // 影响程度
    }[];
  }[];
  // 健康趋势
  trends: {
    time: Date;         // 时间点
    score: number;      // 评分
    events: string[];   // 关键事件
  }[];
}
```

- 健康评分可视化
  - 多维度健康评分
  - 评分趋势分析
  - 健康状态预警

- 影响因素分析
  - 关键影响因素识别
  - 因素权重分析
  - 优化建议生成

### 3. 预警规则分析

#### 3.1 规则效果分析
```typescript
// src/components/monitor/RuleEffectiveness.vue
interface RuleMetrics {
  // 规则统计
  stats: {
    ruleId: string;       // 规则ID
    triggers: number;     // 触发次数
    accuracy: number;     // 准确率
    recall: number;       // 召回率
    falsePositives: number; // 误报数
    falseNegatives: number; // 漏报数
  }[];
  // 规则评估
  evaluation: {
    effectiveness: number; // 有效性
    efficiency: number;    // 效率
    coverage: number;      // 覆盖率
    suggestions: string[]; // 优化建议
  };
}
```

- 规则触发分析
  - 规则触发频率统计
  - 规则准确率分析
  - 误报/漏报分析

- 规则有效性评估
  - 规则覆盖率分析
  - 规则冗余度检测
  - 规则优化建议

#### 3.2 规则优化分析
```typescript
// src/components/monitor/RuleOptimization.vue
interface OptimizationData {
  // 优化建议
  suggestions: {
    ruleId: string;       // 规则ID
    type: string;         // 建议类型
    priority: number;     // 优先级
    impact: string;       // 预期影响
    implementation: string; // 实施建议
  }[];
  // 优化效果
  effects: {
    before: RuleMetrics;  // 优化前
    after: RuleMetrics;   // 优化后
    improvement: number;  // 改进程度
  };
}
```

- 规则优化建议
  - 阈值优化建议
  - 条件优化建议
  - 规则合并建议

- 优化效果评估
  - 优化前后对比
  - 性能影响分析
  - ROI评估

### 4. 实现步骤

1. 基础组件开发
   - 开发各类图表组件
   - 实现数据转换和处理
   - 添加交互和动画效果

2. 数据分析实现
   - 实现数据统计分析
   - 开发异常检测算法
   - 构建预测模型

3. 可视化集成
   - 整合各类图表
   - 实现联动分析
   - 优化交互体验

### 5. 注意事项

1. 性能优化
   - 大数据量展示优化
   - 按需加载策略
   - 缓存机制实现

2. 交互体验
   - 响应式设计
   - 实时更新机制
   - 多维度筛选

3. 可扩展性
   - 组件化设计
   - 数据接口标准化
   - 主题定制支持