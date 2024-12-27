import type { KnowledgeNode, KnowledgeLink, Category, Difficulty } from '../types'

// 分类数据
export const categories: Category[] = [
  { key: 'vulnerability', label: '漏洞原理', color: '#41b883' },
  { key: 'tools', label: '安全工具', color: '#f1c40f' },
  { key: 'authentication', label: '身份认证', color: '#3498db' },
  { key: 'penetration', label: '渗透测试', color: '#e74c3c' },
  { key: 'protection', label: '防护措施', color: '#9b59b6' }
]

// 难度等级
export const difficulties: Difficulty[] = [
  { key: 'basic', label: '基础', color: '#2ecc71' },
  { key: 'intermediate', label: '中级', color: '#f1c40f' },
  { key: 'advanced', label: '高级', color: '#e74c3c' }
]

// 模拟节点数据
export const mockNodes: KnowledgeNode[] = [
  // 根节点
  {
    id: '1',
    name: 'Web安全',
    category: 'vulnerability',
    difficulty: 'basic',
    value: 100,
    description: 'Web安全基础知识',
    keyPoints: ['Web安全概述', '常见威胁', '基本防护'],
    resources: [
      {
        title: '入门资料',
        items: [
          {
            title: 'Web安全入门指南',
            url: '#',
            description: '基础概念和原理'
          }
        ]
      }
    ],
    prerequisites: [],
    nextSteps: ['2', '3', '4', '5', '6'],
    tags: ['基础', '概述']
  },

  // 一级节点
  {
    id: '2',
    name: '漏洞原理',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 80,
    description: '常见Web漏洞原理',
    keyPoints: ['漏洞分类', '攻击原理', '漏洞利用'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['7', '8', '9', '10'],
    tags: ['漏洞', '原理']
  },
  {
    id: '3',
    name: '安全工具',
    category: 'tools',
    difficulty: 'basic',
    value: 70,
    description: '常用安全测试工具',
    keyPoints: ['工具分类', '使用方法', '实践案例'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['11', '12', '13'],
    tags: ['工具', '测试']
  },
  {
    id: '4',
    name: '身份认证',
    category: 'authentication',
    difficulty: 'intermediate',
    value: 90,
    description: '身份认证和授权',
    keyPoints: ['认证方式', '授权机制', '安全协议'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['14', '15', '16'],
    tags: ['认证', '授权']
  },
  {
    id: '5',
    name: '渗透测试',
    category: 'penetration',
    difficulty: 'advanced',
    value: 85,
    description: '渗透测试方法论',
    keyPoints: ['测试流程', '方法技巧', '报告编写'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['17', '18', '19'],
    tags: ['渗透', '测试']
  },
  {
    id: '6',
    name: '防护措施',
    category: 'protection',
    difficulty: 'intermediate',
    value: 75,
    description: '安全防护措施',
    keyPoints: ['防护策略', '技术手段', '最佳实践'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['20', '21', '22'],
    tags: ['防护', '安全']
  },

  // 漏洞原理的子节点
  {
    id: '7',
    name: 'SQL注入',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 60,
    description: 'SQL注入攻击原理',
    keyPoints: ['注入类型', '攻击手法', '防护方法'],
    resources: [],
    prerequisites: ['2'],
    nextSteps: ['23', '24'],
    tags: ['SQL', '注入']
  },
  {
    id: '8',
    name: 'XSS攻击',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 65,
    description: '跨站脚本攻击',
    keyPoints: ['XSS类型', '攻击向量', '防御措施'],
    resources: [],
    prerequisites: ['2'],
    nextSteps: ['25', '26'],
    tags: ['XSS', '跨站']
  },
  {
    id: '9',
    name: 'CSRF攻击',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 70,
    description: '跨站请求伪造',
    keyPoints: ['攻击原理', '防护方法', '实践案例'],
    resources: [],
    prerequisites: ['2'],
    nextSteps: [],
    tags: ['CSRF', '跨站']
  },
  {
    id: '10',
    name: '文件上传',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 75,
    description: '文件上传漏洞',
    keyPoints: ['漏洞原理', '绕过技术', '安全限制'],
    resources: [],
    prerequisites: ['2'],
    nextSteps: [],
    tags: ['上传', '漏洞']
  },

  // 安全工具的子节点
  {
    id: '11',
    name: 'Burp Suite',
    category: 'tools',
    difficulty: 'intermediate',
    value: 80,
    description: '专业的渗透测试工具',
    keyPoints: ['基本功能', '插件使用', '实战技巧'],
    resources: [],
    prerequisites: ['3'],
    nextSteps: [],
    tags: ['工具', 'Burp']
  },
  {
    id: '12',
    name: 'Nmap',
    category: 'tools',
    difficulty: 'basic',
    value: 60,
    description: '网络扫描工具',
    keyPoints: ['扫描技术', '脚本使用', '结果分析'],
    resources: [],
    prerequisites: ['3'],
    nextSteps: [],
    tags: ['工具', '扫描']
  },
  {
    id: '13',
    name: 'Wireshark',
    category: 'tools',
    difficulty: 'intermediate',
    value: 70,
    description: '网络抓包分析工具',
    keyPoints: ['抓包原理', '过滤规则', '协议分析', '会话重组', '流量分析'],
    resources: [
      {
        title: '官方文档',
        items: [
          {
            title: 'Wireshark用户指南',
            url: 'https://www.wireshark.org/docs/',
            description: '官方详细使用文档'
          }
        ]
      }
    ],
    prerequisites: ['3'],
    nextSteps: ['41', '42'],
    tags: ['工具', '抓包', '协议分析']
  },

  // 身份认证的子节点
  {
    id: '14',
    name: 'OAuth2.0',
    category: 'authentication',
    difficulty: 'advanced',
    value: 85,
    description: '开放授权协议',
    keyPoints: ['授权流程', '安全考虑', '最佳实践'],
    resources: [],
    prerequisites: ['4'],
    nextSteps: [],
    tags: ['认证', 'OAuth']
  },
  {
    id: '15',
    name: 'JWT',
    category: 'authentication',
    difficulty: 'intermediate',
    value: 75,
    description: 'JSON Web Token',
    keyPoints: ['令牌结构', '使用场景', '安全措施'],
    resources: [],
    prerequisites: ['4'],
    nextSteps: [],
    tags: ['认证', 'Token']
  },
  {
    id: '16',
    name: '2FA',
    category: 'authentication',
    difficulty: 'intermediate',
    value: 70,
    description: '双因素认证',
    keyPoints: ['认证方式', '实现方法', '安全性分析'],
    resources: [],
    prerequisites: ['4'],
    nextSteps: [],
    tags: ['认证', '双因素']
  },

  // 渗透测试的子节点
  {
    id: '17',
    name: '信息收集',
    category: 'penetration',
    difficulty: 'intermediate',
    value: 75,
    description: '渗透测试信息收集',
    keyPoints: [
      '被动信息收集',
      '主动信息收集',
      '社会工程学',
      '资产梳理',
      '指纹识别'
    ],
    resources: [
      {
        title: '推荐工具',
        items: [
          {
            title: 'subfinder',
            url: 'https://github.com/projectdiscovery/subfinder',
            description: '子域名收集工具'
          },
          {
            title: 'whatweb',
            url: 'https://github.com/urbanadventurer/WhatWeb',
            description: 'Web应用指纹识别'
          }
        ]
      }
    ],
    prerequisites: ['5'],
    nextSteps: ['31', '32'],
    tags: ['渗透', '信息收集', '侦察']
  },
  {
    id: '18',
    name: '漏洞扫描',
    category: 'penetration',
    difficulty: 'advanced',
    value: 80,
    description: '自动化漏洞扫描',
    keyPoints: ['扫描技术', '工具选择', '结果分析'],
    resources: [],
    prerequisites: ['5'],
    nextSteps: [],
    tags: ['渗透', '扫描']
  },
  {
    id: '19',
    name: '后渗透',
    category: 'penetration',
    difficulty: 'advanced',
    value: 90,
    description: '后渗透测试技术',
    keyPoints: ['权限提升', '横向移动', '痕迹清理'],
    resources: [],
    prerequisites: ['5'],
    nextSteps: [],
    tags: ['渗透', '后渗透']
  },

  // 防护措施的子节点
  {
    id: '20',
    name: 'WAF',
    category: 'protection',
    difficulty: 'advanced',
    value: 85,
    description: 'Web应用防火墙',
    keyPoints: ['防护原理', '规则配置', '绕过技术'],
    resources: [],
    prerequisites: ['6'],
    nextSteps: [],
    tags: ['防护', 'WAF']
  },
  {
    id: '21',
    name: '安全编码',
    category: 'protection',
    difficulty: 'intermediate',
    value: 75,
    description: '安全编码实践',
    keyPoints: ['编码规范', '常见问题', '最佳实践'],
    resources: [],
    prerequisites: ['6'],
    nextSteps: [],
    tags: ['防护', '编码']
  },
  {
    id: '22',
    name: '安全配置',
    category: 'protection',
    difficulty: 'intermediate',
    value: 70,
    description: '服务器安全配置',
    keyPoints: ['配置检查', '加固方案', '维护管理'],
    resources: [],
    prerequisites: ['6'],
    nextSteps: [],
    tags: ['防护', '配置']
  },

  // SQL注入的子节点
  {
    id: '23',
    name: '盲注技术',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 65,
    description: 'SQL盲注技术详解',
    keyPoints: ['布尔盲注', '时间盲注', '带外通道'],
    resources: [],
    prerequisites: ['7'],
    nextSteps: [],
    tags: ['SQL注入', '盲注']
  },
  {
    id: '24',
    name: 'ORM注入',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 70,
    description: 'ORM框架SQL注入',
    keyPoints: ['ORM原理', '注入方式', '防护方法'],
    resources: [],
    prerequisites: ['7'],
    nextSteps: [],
    tags: ['SQL注入', 'ORM']
  },

  // XSS攻击的子节点
  {
    id: '25',
    name: 'DOM XSS',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 75,
    description: '基于DOM的XSS攻击',
    keyPoints: ['DOM操作', '攻击向量', '防御方式'],
    resources: [],
    prerequisites: ['8'],
    nextSteps: [],
    tags: ['XSS', 'DOM']
  },
  {
    id: '26',
    name: 'CSP绕过',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 80,
    description: '内容安全策略绕过技术',
    keyPoints: ['CSP规则', '绕过方法', '配置加固'],
    resources: [],
    prerequisites: ['8'],
    nextSteps: [],
    tags: ['XSS', 'CSP']
  },

  // Burp Suite的子节点
  {
    id: '27',
    name: 'Intruder模块',
    category: 'tools',
    difficulty: 'intermediate',
    value: 65,
    description: 'Burp Suite爆破模块',
    keyPoints: ['攻击类型', '载荷设置', '结果分析'],
    resources: [],
    prerequisites: ['11'],
    nextSteps: [],
    tags: ['Burp', '爆破']
  },
  {
    id: '28',
    name: 'Scanner模块',
    category: 'tools',
    difficulty: 'intermediate',
    value: 70,
    description: 'Burp Suite扫描模块',
    keyPoints: ['扫描配置', '漏洞检测', '报告生成'],
    resources: [],
    prerequisites: ['11'],
    nextSteps: [],
    tags: ['Burp', '扫描']
  },

  // OAuth2.0的子节点
  {
    id: '29',
    name: '授权码模式',
    category: 'authentication',
    difficulty: 'advanced',
    value: 75,
    description: 'OAuth2.0授权码模式',
    keyPoints: [
      '授权流程步骤',
      'PKCE扩展',
      '安全考虑因素',
      '实现最佳实践',
      '常见漏洞防范'
    ],
    resources: [
      {
        title: '技术规范',
        items: [
          {
            title: 'OAuth 2.0 RFC',
            url: 'https://tools.ietf.org/html/rfc6749',
            description: 'OAuth 2.0授权框架规范'
          },
          {
            title: 'PKCE RFC',
            url: 'https://tools.ietf.org/html/rfc7636',
            description: 'PKCE扩展规范'
          }
        ]
      }
    ],
    prerequisites: ['14'],
    nextSteps: [],
    tags: ['OAuth', '授权码', 'PKCE']
  },
  {
    id: '30',
    name: '隐式授权',
    category: 'authentication',
    difficulty: 'advanced',
    value: 70,
    description: 'OAuth2.0隐式授权模式',
    keyPoints: ['流程特点', '使用场景', '安全风险'],
    resources: [],
    prerequisites: ['14'],
    nextSteps: [],
    tags: ['OAuth', '隐式授权']
  },

  // 信息收集的子节点
  {
    id: '31',
    name: '子域名收集',
    category: 'penetration',
    difficulty: 'intermediate',
    value: 65,
    description: '子域名枚举与收集',
    keyPoints: ['收集方法', '工具使用', '结果验证'],
    resources: [],
    prerequisites: ['17'],
    nextSteps: [],
    tags: ['信息收集', '子域名']
  },
  {
    id: '32',
    name: '指纹识别',
    category: 'penetration',
    difficulty: 'intermediate',
    value: 60,
    description: 'Web应用指纹识别',
    keyPoints: ['识别技术', '工具选择', '结果分析'],
    resources: [],
    prerequisites: ['17'],
    nextSteps: [],
    tags: ['信息收集', '指纹']
  },

  // WAF的子节点
  {
    id: '33',
    name: '规则配置',
    category: 'protection',
    difficulty: 'advanced',
    value: 80,
    description: 'WAF规则配置与优化',
    keyPoints: [
      '规则语法详解',
      '配置最佳实践',
      '性能调优方法',
      '误报处理',
      '规则测试'
    ],
    resources: [
      {
        title: '参考资料',
        items: [
          {
            title: 'ModSecurity手册',
            url: 'https://github.com/SpiderLabs/ModSecurity',
            description: '开源WAF解决方案'
          }
        ]
      }
    ],
    prerequisites: ['20'],
    nextSteps: [],
    tags: ['WAF', '规则', '配置优化']
  },
  {
    id: '34',
    name: '绕过检测',
    category: 'protection',
    difficulty: 'advanced',
    value: 85,
    description: 'WAF绕过检测与防护',
    keyPoints: ['绕过技术', '检测方法', '防护加固'],
    resources: [],
    prerequisites: ['20'],
    nextSteps: [],
    tags: ['WAF', '绕过']
  },

  // CSRF攻击的子节点
  {
    id: '35',
    name: '防御令牌',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 65,
    description: 'CSRF Token防御机制',
    keyPoints: ['令牌生成', '验证流程', '安全存储'],
    resources: [],
    prerequisites: ['9'],
    nextSteps: [],
    tags: ['CSRF', '令牌']
  },
  {
    id: '36',
    name: 'SameSite',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 70,
    description: 'Cookie SameSite属性',
    keyPoints: ['属性值', '兼容性', '最佳实践'],
    resources: [],
    prerequisites: ['9'],
    nextSteps: [],
    tags: ['CSRF', 'Cookie']
  },

  // 文件上传的子节点
  {
    id: '37',
    name: '文件验证',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 70,
    description: '文件上传验证技术',
    keyPoints: ['类型检查', '内容验证', '安全存储'],
    resources: [],
    prerequisites: ['10'],
    nextSteps: [],
    tags: ['上传', '验证']
  },
  {
    id: '38',
    name: '绕过技术',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 75,
    description: '文件上传绕过方法',
    keyPoints: ['类型伪造', '解析漏洞', '防护方案'],
    resources: [],
    prerequisites: ['10'],
    nextSteps: [],
    tags: ['上传', '绕过']
  },

  // Nmap的子节点
  {
    id: '39',
    name: '端口���描',
    category: 'tools',
    difficulty: 'intermediate',
    value: 65,
    description: 'Nmap端口扫描技术',
    keyPoints: ['扫描类型', '参数设置', '结果分析'],
    resources: [],
    prerequisites: ['12'],
    nextSteps: [],
    tags: ['Nmap', '端口']
  },
  {
    id: '40',
    name: '脚本引擎',
    category: 'tools',
    difficulty: 'advanced',
    value: 70,
    description: 'Nmap脚本引擎(NSE)',
    keyPoints: ['脚本类型', '编写方法', '调试技巧'],
    resources: [],
    prerequisites: ['12'],
    nextSteps: [],
    tags: ['Nmap', 'NSE']
  },

  // Wireshark的子节点
  {
    id: '41',
    name: '过滤器',
    category: 'tools',
    difficulty: 'intermediate',
    value: 65,
    description: 'Wireshark过滤器使用',
    keyPoints: ['显示过滤', '捕获过滤', '过滤语法'],
    resources: [],
    prerequisites: ['13'],
    nextSteps: [],
    tags: ['Wireshark', '过滤器']
  },
  {
    id: '42',
    name: '协议分析',
    category: 'tools',
    difficulty: 'advanced',
    value: 75,
    description: '网络协议分析技术',
    keyPoints: ['协议解析', '会话追踪', '异常检测'],
    resources: [],
    prerequisites: ['13'],
    nextSteps: [],
    tags: ['Wireshark', '协议']
  },

  // 2FA的子节点
  {
    id: '43',
    name: 'TOTP',
    category: 'authentication',
    difficulty: 'intermediate',
    value: 65,
    description: '基于时间的一次性密码',
    keyPoints: ['算法原理', '实现方法', '安全考虑'],
    resources: [],
    prerequisites: ['16'],
    nextSteps: [],
    tags: ['2FA', 'TOTP']
  },
  {
    id: '44',
    name: '硬件认证',
    category: 'authentication',
    difficulty: 'advanced',
    value: 75,
    description: '硬件安全密钥认证',
    keyPoints: ['密钥类型', '认证流程', '集成方案'],
    resources: [],
    prerequisites: ['16'],
    nextSteps: [],
    tags: ['2FA', '硬件']
  },

  // 后渗透的子节点
  {
    id: '45',
    name: '权限维持',
    category: 'penetration',
    difficulty: 'advanced',
    value: 85,
    description: '后渗透权限维持技术',
    keyPoints: ['持久化', '隐蔽性', '清理方法'],
    resources: [],
    prerequisites: ['19'],
    nextSteps: [],
    tags: ['后渗透', '权限']
  },
  {
    id: '46',
    name: '内网穿透',
    category: 'penetration',
    difficulty: 'advanced',
    value: 80,
    description: '内网穿透技术',
    keyPoints: ['通道建立', '流量隐藏', '代理转发'],
    resources: [],
    prerequisites: ['19'],
    nextSteps: [],
    tags: ['后渗透', '内网']
  },

  // 新增移动安全相关节点
  {
    id: '47',
    name: '移动应用安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 85,
    description: '移动应用安全测试与防护',
    keyPoints: ['应用架构', '漏洞类型', '测试方法', '安全加固'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['48', '49', '50'],
    tags: ['移动安全', 'APP安全']
  },
  {
    id: '48',
    name: 'Android安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 80,
    description: 'Android应用安全测试',
    keyPoints: ['应用结构', '逆向分析', '漏洞挖掘', '加固技术'],
    resources: [],
    prerequisites: ['47'],
    nextSteps: ['51', '52'],
    tags: ['Android', '移动安全']
  },
  {
    id: '49',
    name: 'iOS安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 80,
    description: 'iOS应用安全测试',
    keyPoints: ['应用沙箱', '越狱检测', '安全机制', '漏洞分析'],
    resources: [],
    prerequisites: ['47'],
    nextSteps: ['53', '54'],
    tags: ['iOS', '移动安全']
  },
  {
    id: '50',
    name: '移动应用加固',
    category: 'protection',
    difficulty: 'advanced',
    value: 75,
    description: '移动应用安全加固技术',
    keyPoints: ['代码混淆', '反调试', '完整性校验', '数据加密'],
    resources: [],
    prerequisites: ['47'],
    nextSteps: [],
    tags: ['加固', '移动安全']
  },

  // 新增云安全相关节点
  {
    id: '51',
    name: '云安全',
    category: 'protection',
    difficulty: 'advanced',
    value: 90,
    description: '云计算环境安全',
    keyPoints: ['云安全架构', '威胁模型', '安全控制', '合规要求'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['52', '53', '54'],
    tags: ['云安全', '基础设施']
  },
  {
    id: '52',
    name: '容器安全',
    category: 'protection',
    difficulty: 'advanced',
    value: 85,
    description: '容器环境安全防护',
    keyPoints: ['容器技术', '安全基线', '漏洞管理', '运行时防护'],
    resources: [],
    prerequisites: ['51'],
    nextSteps: ['55'],
    tags: ['容器', 'Docker']
  },
  {
    id: '53',
    name: '服务配置',
    category: 'protection',
    difficulty: 'intermediate',
    value: 75,
    description: '云服务安全配置',
    keyPoints: ['访问控制', '网络隔离', '日志审计', '加密管理'],
    resources: [],
    prerequisites: ['51'],
    nextSteps: [],
    tags: ['云服务', '配置管理']
  },
  {
    id: '54',
    name: '身份管理',
    category: 'authentication',
    difficulty: 'advanced',
    value: 80,
    description: '云环境身份管理',
    keyPoints: ['身份认证', '权限管理', '密钥管理', '联合身份'],
    resources: [],
    prerequisites: ['51'],
    nextSteps: [],
    tags: ['IAM', '身份认证']
  },

  // 新增物联网安全相关节点
  {
    id: '55',
    name: '物联网安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 85,
    description: '物联网设备与协议安全',
    keyPoints: ['通信协议', '硬件安全', '固件分析', '漏洞挖掘'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['56', '57', '58'],
    tags: ['IoT', '物联网']
  },
  {
    id: '56',
    name: '固件安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 80,
    description: '固件安全分析与测试',
    keyPoints: ['固件提取', '逆向分析', '漏洞挖掘', '安全加固'],
    resources: [],
    prerequisites: ['55'],
    nextSteps: [],
    tags: ['固件', '逆向分析']
  },
  {
    id: '57',
    name: '协议分析',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 75,
    description: '物联网协议安全分析',
    keyPoints: ['协议逆向', '漏洞分析', '攻击利用', '防护方案'],
    resources: [],
    prerequisites: ['55'],
    nextSteps: [],
    tags: ['协议', '安全分析']
  },
  {
    id: '58',
    name: '设备安全',
    category: 'protection',
    difficulty: 'advanced',
    value: 80,
    description: '物联网设备安全防护',
    keyPoints: ['安全启动', '认证机制', '通信加密', '访问控制'],
    resources: [],
    prerequisites: ['55'],
    nextSteps: [],
    tags: ['IoT', '设备安全']
  },

  // 新增应急响应与取证相关节点
  {
    id: '59',
    name: '应急响应',
    category: 'protection',
    difficulty: 'advanced',
    value: 85,
    description: '安全事件应急响应',
    keyPoints: ['响应流程', '取证分析', '溯源技术', '事件处理'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['60', '61', '62'],
    tags: ['应急响应', '安全运维']
  },
  {
    id: '60',
    name: '数字取证',
    category: 'protection',
    difficulty: 'advanced',
    value: 80,
    description: '数字证据获取与分析',
    keyPoints: ['证据获取', '证据分析', '证据链完整性', '报告编写'],
    resources: [],
    prerequisites: ['59'],
    nextSteps: [],
    tags: ['取证', '分析']
  },
  {
    id: '61',
    name: '日志分析',
    category: 'protection',
    difficulty: 'intermediate',
    value: 75,
    description: '安全日志分析技术',
    keyPoints: ['日志收集', '异常检测', '关联分析', '威胁发现'],
    resources: [],
    prerequisites: ['59'],
    nextSteps: [],
    tags: ['日志', '分析']
  },
  {
    id: '62',
    name: '威胁狩猎',
    category: 'protection',
    difficulty: 'advanced',
    value: 85,
    description: '主动威胁发现与处置',
    keyPoints: ['威胁情报', '行为分析', '攻击链跟踪', '处置方案'],
    resources: [],
    prerequisites: ['59'],
    nextSteps: [],
    tags: ['威胁', '狩猎']
  },

  // 新增代码审计相关节点
  {
    id: '63',
    name: '代码审计',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 90,
    description: '应用代码安全审计',
    keyPoints: ['审计方法', '漏洞模式', '工具使用', '修复建议'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['64', '65', '66'],
    tags: ['代码', '审计']
  },
  {
    id: '64',
    name: '静态分析',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 85,
    description: '代码静态安全分析',
    keyPoints: ['分析工具', '规则编写', '误报处理', '自动化分析'],
    resources: [],
    prerequisites: ['63'],
    nextSteps: [],
    tags: ['SAST', '静态分析']
  },
  {
    id: '65',
    name: '动态分析',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 85,
    description: '代码动态安全分析',
    keyPoints: ['运行时分析', '漏洞验证', '污点追踪', '自动化测试'],
    resources: [],
    prerequisites: ['63'],
    nextSteps: [],
    tags: ['DAST', '动态分析']
  },
  {
    id: '66',
    name: '代码规范',
    category: 'protection',
    difficulty: 'intermediate',
    value: 75,
    description: '安全编码规范',
    keyPoints: ['编码标准', '最佳实践', '常见问题', '规范执行'],
    resources: [],
    prerequisites: ['63'],
    nextSteps: [],
    tags: ['规范', '编码']
  },

  // 新增区块链安全相关节点
  {
    id: '67',
    name: '区块链安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 90,
    description: '区块链系统安全',
    keyPoints: ['共识机制', '智能合约', '钱包安全', '隐私保护'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['68', '69', '70'],
    tags: ['区块链', '安全']
  },
  {
    id: '68',
    name: '智能合约审计',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 85,
    description: '智能合约安全审计',
    keyPoints: ['合约分析', '漏洞类型', '审计工具', '最佳实践'],
    resources: [],
    prerequisites: ['67'],
    nextSteps: [],
    tags: ['智能合约', '审计']
  },
  {
    id: '69',
    name: '共识安全',
    category: 'vulnerability',
    difficulty: 'advanced',
    value: 85,
    description: '区块链共识机制安全',
    keyPoints: ['共识算法', '攻击向量', '防护措施', '性能优化'],
    resources: [],
    prerequisites: ['67'],
    nextSteps: [],
    tags: ['共识', '区块链']
  },
  {
    id: '70',
    name: '钱包安全',
    category: 'protection',
    difficulty: 'advanced',
    value: 80,
    description: '加密货币钱包安全',
    keyPoints: ['密钥管理', '交易安全', '备份恢复', '冷热钱包'],
    resources: [],
    prerequisites: ['67'],
    nextSteps: [],
    tags: ['钱包', '加密货币']
  },

  // 新增社会工程学相关节点
  {
    id: '71',
    name: '社会工程学',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 75,
    description: '社会工程学攻击与防御',
    keyPoints: ['攻击方法', '心理学原理', '防护措施', '意识培训'],
    resources: [],
    prerequisites: ['1'],
    nextSteps: ['72', '73', '74'],
    tags: ['社工', '心理学']
  },
  {
    id: '72',
    name: '钓鱼攻击',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 70,
    description: '钓鱼攻击技术与防护',
    keyPoints: ['钓鱼类型', '攻击手段', '检测方法', '防护策略'],
    resources: [],
    prerequisites: ['71'],
    nextSteps: [],
    tags: ['钓鱼', '社工']
  },
  {
    id: '73',
    name: '身份欺骗',
    category: 'vulnerability',
    difficulty: 'intermediate',
    value: 70,
    description: '身份欺骗攻击与防护',
    keyPoints: ['欺骗手段', '身份验证', '防护措施', '案例分析'],
    resources: [],
    prerequisites: ['71'],
    nextSteps: [],
    tags: ['欺骗', '社工']
  },
  {
    id: '74',
    name: '意识培训',
    category: 'protection',
    difficulty: 'basic',
    value: 65,
    description: '安全意识培训',
    keyPoints: ['培训方法', '案例分享', '考核评估', '持续改进'],
    resources: [],
    prerequisites: ['71'],
    nextSteps: [],
    tags: ['培训', '意识']
  }
]

// 更新连接数据
export const mockLinks: KnowledgeLink[] = [
  // 根节点到一级节点的连接
  { source: '1', target: '2', value: 1, type: 'prerequisite' },
  { source: '1', target: '3', value: 1, type: 'prerequisite' },
  { source: '1', target: '4', value: 1, type: 'prerequisite' },
  { source: '1', target: '5', value: 1, type: 'prerequisite' },
  { source: '1', target: '6', value: 1, type: 'prerequisite' },

  // 漏洞原理到其子节点的连接
  { source: '2', target: '7', value: 1, type: 'prerequisite' },
  { source: '2', target: '8', value: 1, type: 'prerequisite' },
  { source: '2', target: '9', value: 1, type: 'prerequisite' },
  { source: '2', target: '10', value: 1, type: 'prerequisite' },

  // 安全工具到其子节点的连接
  { source: '3', target: '11', value: 1, type: 'prerequisite' },
  { source: '3', target: '12', value: 1, type: 'prerequisite' },
  { source: '3', target: '13', value: 1, type: 'prerequisite' },

  // 身份认证到其子节点的连接
  { source: '4', target: '14', value: 1, type: 'prerequisite' },
  { source: '4', target: '15', value: 1, type: 'prerequisite' },
  { source: '4', target: '16', value: 1, type: 'prerequisite' },

  // 渗透测试到其子节点的连接
  { source: '5', target: '17', value: 1, type: 'prerequisite' },
  { source: '5', target: '18', value: 1, type: 'prerequisite' },
  { source: '5', target: '19', value: 1, type: 'prerequisite' },

  // 防护措施到其子节点的连接
  { source: '6', target: '20', value: 1, type: 'prerequisite' },
  { source: '6', target: '21', value: 1, type: 'prerequisite' },
  { source: '6', target: '22', value: 1, type: 'prerequisite' },

  // 相关节点之间的连接
  { source: '7', target: '8', value: 0.5, type: 'related' },
  { source: '8', target: '9', value: 0.5, type: 'related' },
  { source: '9', target: '10', value: 0.5, type: 'related' },
  { source: '11', target: '12', value: 0.5, type: 'related' },
  { source: '12', target: '13', value: 0.5, type: 'related' },
  { source: '14', target: '15', value: 0.5, type: 'related' },
  { source: '15', target: '16', value: 0.5, type: 'related' },
  { source: '17', target: '18', value: 0.5, type: 'related' },
  { source: '18', target: '19', value: 0.5, type: 'related' },
  { source: '20', target: '21', value: 0.5, type: 'related' },
  { source: '21', target: '22', value: 0.5, type: 'related' },

  // 跨类别的相关连接
  { source: '7', target: '11', value: 0.5, type: 'related' }, // SQL注入与Burp Suite
  { source: '8', target: '11', value: 0.5, type: 'related' }, // XSS与Burp Suite
  { source: '17', target: '12', value: 0.5, type: 'related' }, // 信息收集与Nmap
  { source: '18', target: '11', value: 0.5, type: 'related' }, // 漏洞扫描与Burp Suite
  { source: '15', target: '21', value: 0.5, type: 'related' }, // JWT与安全编码
  { source: '20', target: '22', value: 0.5, type: 'related' },  // WAF与安全配置

  // SQL注入子节点的连接
  { source: '7', target: '23', value: 1, type: 'prerequisite' },
  { source: '7', target: '24', value: 1, type: 'prerequisite' },
  { source: '23', target: '24', value: 0.5, type: 'related' },

  // XSS攻击子节点的连接
  { source: '8', target: '25', value: 1, type: 'prerequisite' },
  { source: '8', target: '26', value: 1, type: 'prerequisite' },
  { source: '25', target: '26', value: 0.5, type: 'related' },

  // Burp Suite子节点的连接
  { source: '11', target: '27', value: 1, type: 'prerequisite' },
  { source: '11', target: '28', value: 1, type: 'prerequisite' },
  { source: '27', target: '28', value: 0.5, type: 'related' },

  // OAuth2.0子节点的连接
  { source: '14', target: '29', value: 1, type: 'prerequisite' },
  { source: '14', target: '30', value: 1, type: 'prerequisite' },
  { source: '29', target: '30', value: 0.5, type: 'related' },

  // 信息收集子节点的连接
  { source: '17', target: '31', value: 1, type: 'prerequisite' },
  { source: '17', target: '32', value: 1, type: 'prerequisite' },
  { source: '31', target: '32', value: 0.5, type: 'related' },

  // WAF子节点的连接
  { source: '20', target: '33', value: 1, type: 'prerequisite' },
  { source: '20', target: '34', value: 1, type: 'prerequisite' },
  { source: '33', target: '34', value: 0.5, type: 'related' },

  // 跨类别的相关连接
  { source: '23', target: '27', value: 0.5, type: 'related' }, // 盲注技术与Intruder
  { source: '25', target: '28', value: 0.5, type: 'related' }, // DOM XSS与Scanner
  { source: '31', target: '12', value: 0.5, type: 'related' }, // 子域名收集与Nmap
  { source: '32', target: '13', value: 0.5, type: 'related' }, // 指纹识别与Wireshark
  { source: '26', target: '33', value: 0.5, type: 'related' }, // CSP绕过与WAF规则
  { source: '29', target: '21', value: 0.5, type: 'related' },  // 授权码模式与安全编码

  // 移动安全相关连接
  { source: '1', target: '47', value: 1, type: 'prerequisite' },
  { source: '47', target: '48', value: 1, type: 'prerequisite' },
  { source: '47', target: '49', value: 1, type: 'prerequisite' },
  { source: '47', target: '50', value: 1, type: 'prerequisite' },
  { source: '48', target: '49', value: 0.5, type: 'related' },
  { source: '48', target: '50', value: 0.5, type: 'related' },
  { source: '49', target: '50', value: 0.5, type: 'related' },

  // 云安全相关连接
  { source: '1', target: '51', value: 1, type: 'prerequisite' },
  { source: '51', target: '52', value: 1, type: 'prerequisite' },
  { source: '51', target: '53', value: 1, type: 'prerequisite' },
  { source: '51', target: '54', value: 1, type: 'prerequisite' },
  { source: '52', target: '53', value: 0.5, type: 'related' },
  { source: '53', target: '54', value: 0.5, type: 'related' },
  { source: '52', target: '54', value: 0.5, type: 'related' },

  // 物联网安全相关连接
  { source: '1', target: '55', value: 1, type: 'prerequisite' },
  { source: '55', target: '56', value: 1, type: 'prerequisite' },
  { source: '55', target: '57', value: 1, type: 'prerequisite' },
  { source: '55', target: '58', value: 1, type: 'prerequisite' },
  { source: '56', target: '57', value: 0.5, type: 'related' },
  { source: '57', target: '58', value: 0.5, type: 'related' },
  { source: '56', target: '58', value: 0.5, type: 'related' },

  // 跨领域连接
  { source: '48', target: '56', value: 0.5, type: 'related' }, // Android安全与固件安全
  { source: '49', target: '56', value: 0.5, type: 'related' }, // iOS安全与固件安全
  { source: '52', target: '58', value: 0.5, type: 'related' }, // 容器安全与设备安全
  { source: '54', target: '4', value: 0.5, type: 'related' },  // 云身份管理与身份认证

  // 应急响应相关连接
  { source: '1', target: '59', value: 1, type: 'prerequisite' },
  { source: '59', target: '60', value: 1, type: 'prerequisite' },
  { source: '59', target: '61', value: 1, type: 'prerequisite' },
  { source: '59', target: '62', value: 1, type: 'prerequisite' },
  { source: '60', target: '61', value: 0.5, type: 'related' },
  { source: '61', target: '62', value: 0.5, type: 'related' },
  { source: '60', target: '62', value: 0.5, type: 'related' },

  // 代码审计相关连接
  { source: '1', target: '63', value: 1, type: 'prerequisite' },
  { source: '63', target: '64', value: 1, type: 'prerequisite' },
  { source: '63', target: '65', value: 1, type: 'prerequisite' },
  { source: '63', target: '66', value: 1, type: 'prerequisite' },
  { source: '64', target: '65', value: 0.5, type: 'related' },
  { source: '65', target: '66', value: 0.5, type: 'related' },
  { source: '64', target: '66', value: 0.5, type: 'related' },

  // 区块链安全相关连接
  { source: '1', target: '67', value: 1, type: 'prerequisite' },
  { source: '67', target: '68', value: 1, type: 'prerequisite' },
  { source: '67', target: '69', value: 1, type: 'prerequisite' },
  { source: '67', target: '70', value: 1, type: 'prerequisite' },
  { source: '68', target: '69', value: 0.5, type: 'related' },
  { source: '69', target: '70', value: 0.5, type: 'related' },
  { source: '68', target: '70', value: 0.5, type: 'related' },

  // 社会工程学相关连接
  { source: '1', target: '71', value: 1, type: 'prerequisite' },
  { source: '71', target: '72', value: 1, type: 'prerequisite' },
  { source: '71', target: '73', value: 1, type: 'prerequisite' },
  { source: '71', target: '74', value: 1, type: 'prerequisite' },
  { source: '72', target: '73', value: 0.5, type: 'related' },
  { source: '73', target: '74', value: 0.5, type: 'related' },
  { source: '72', target: '74', value: 0.5, type: 'related' },

  // 跨领域连接
  { source: '61', target: '17', value: 0.5, type: 'related' }, // 日志分析与信息收集
  { source: '64', target: '21', value: 0.5, type: 'related' }, // 静态分析与安全编码
  { source: '68', target: '63', value: 0.5, type: 'related' }, // 智能合约审计与代码审计
  { source: '72', target: '17', value: 0.5, type: 'related' }, // 钓鱼攻击与信息收集
  { source: '70', target: '15', value: 0.5, type: 'related' }, // 钱包安全与JWT
  { source: '62', target: '18', value: 0.5, type: 'related' }  // 威胁狩猎与漏洞扫描
] 