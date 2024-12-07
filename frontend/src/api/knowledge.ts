import request from '@/utils/request'

export interface ResourceItem {
  name: string
  description: string
  title: string
  url: string
}

export interface ResourceGroup {
  type: string
  items: ResourceItem[]
}

export interface KnowledgeNode {
  id: string | number
  name: string
  category: string
  difficulty: string
  value: number
  description: string
  keyPoints: string[]
  resources: ResourceGroup[]
  prerequisites: string[]
  nextSteps: string[]
  createdAt?: string
  updatedAt?: string
}

export interface KnowledgeLink {
  source: string | number
  target: string | number
  relation: string
  value: number
}

export interface KnowledgeGraphData {
  nodes: KnowledgeNode[]
  links: KnowledgeLink[]
}

// Mock data for development
export const mockKnowledgeGraph: KnowledgeGraphData = {
  nodes: [
    {
      id: '1',
      name: 'Web安全基础',
      category: 'concept',
      difficulty: 'basic',
      value: 1,
      description: 'Web安全的基本概念和原理，包括HTTP协议、网络架构、安全模型等基础知识。',
      keyPoints: ['HTTP协议', '网络架构', '安全模型', '攻击面分析'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'Web安全入门指南',
              description: 'Web安全基础知识的全面介绍',
              title: 'Web安全基础教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: [],
      nextSteps: ['2', '3', '4'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '2',
      name: 'SQL注入攻击',
      category: 'vulnerability',
      difficulty: 'intermediate',
      value: 1,
      description: 'SQL注入是一种常见的Web应用程序漏洞，攻击者通过在应用程序输入中注入恶意SQL代码来操纵数据库。',
      keyPoints: ['参数化查询', '输入验证', '最小权限原则', 'SQL注入类型'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'SQL注入攻击详解',
              description: 'SQL注入漏洞原理和防御方法',
              title: 'SQL注入教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['1'],
      nextSteps: ['5', '6'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '3',
      name: 'XSS跨站脚本',
      category: 'vulnerability',
      difficulty: 'intermediate',
      value: 1,
      description: '跨站脚本攻击是一种将恶意脚本注入到网页中的攻击方式，可能导致用户信息泄露或会话劫持。',
      keyPoints: ['输入过滤', 'CSP策略', '输出编码', 'XSS类型'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'XSS攻击防御指南',
              description: 'XSS漏洞原理和防御策略',
              title: 'XSS教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['1'],
      nextSteps: ['7', '8'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '4',
      name: 'CSRF跨站请求伪造',
      category: 'vulnerability',
      difficulty: 'intermediate',
      value: 1,
      description: '跨站请求伪造是一种强制用户在已登录的Web应用程序上执行非预期操作的攻击。',
      keyPoints: ['CSRF Token', 'SameSite Cookie', '请求验证', '防御策略'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'CSRF攻击与防御',
              description: 'CSRF漏洞原理和防御方法',
              title: 'CSRF教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['1'],
      nextSteps: ['9', '10'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '5',
      name: 'SQLMap工具使用',
      category: 'tool',
      difficulty: 'intermediate',
      value: 1,
      description: 'SQLMap是一个开源的SQL注入检测与利用工具，可以自动化检测和利用SQL注入漏洞。',
      keyPoints: ['基本用法', '注入技术', '绕过技巧', '后渗透'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'SQLMap使用指南',
              description: 'SQLMap工具的详细使用教程',
              title: 'SQLMap教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['2'],
      nextSteps: ['11'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '6',
      name: '数据库安全加固',
      category: 'technique',
      difficulty: 'advanced',
      value: 1,
      description: '数据库安全加固包括权限管理、漏洞修复、安全配置等多个方面。',
      keyPoints: ['权限管理', '安全配置', '漏洞修复', '审计日志'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: '数据库安全加固指南',
              description: '数据库安全加固的最佳实践',
              title: '数据库安全教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['2'],
      nextSteps: ['12'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '7',
      name: 'XSS平台搭建',
      category: 'tool',
      difficulty: 'advanced',
      value: 1,
      description: 'XSS平台是一个用于测试和验证XSS漏洞的工具平台。',
      keyPoints: ['平台架构', '功能模块', '部署配置', '使用场景'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'XSS平台搭建教程',
              description: 'XSS平台的搭建和使用指南',
              title: 'XSS平台教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['3'],
      nextSteps: ['13'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '8',
      name: 'CSP内容安全策略',
      category: 'technique',
      difficulty: 'advanced',
      value: 1,
      description: 'CSP是一种安全策略机制，用于防止XSS等注入攻击。',
      keyPoints: ['策略配置', '指令使用', '部署方式', '兼容性'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'CSP配置指南',
              description: 'CSP策略的配置和最佳实践',
              title: 'CSP教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['3'],
      nextSteps: ['14'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '9',
      name: '会话安全',
      category: 'concept',
      difficulty: 'advanced',
      value: 1,
      description: '会话安全涉及用户认证、授权、会话管理等多个安全方面。',
      keyPoints: ['会话管理', '认证机制', '授权控制', 'Cookie安全'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: '会话安全指南',
              description: 'Web应用会话安全的最佳实践',
              title: '会话安全教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['4'],
      nextSteps: ['15'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '10',
      name: 'OAuth2.0认证',
      category: 'technique',
      difficulty: 'advanced',
      value: 1,
      description: 'OAuth2.0是一个授权框架，用于实现第三方应用的授权访问。',
      keyPoints: ['授权流程', '令牌管理', '安全配置', '最佳实践'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'OAuth2.0实现指南',
              description: 'OAuth2.0认证的实现和安全配置',
              title: 'OAuth2.0教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['4'],
      nextSteps: ['16'],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '11',
      name: '渗透测试',
      category: 'technique',
      difficulty: 'expert',
      value: 1,
      description: '渗透测试是一种通过模拟攻击来评估系统安全性的方法。',
      keyPoints: ['测试方法', '工具使用', '漏洞利用', '报告编写'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: '渗透测试指南',
              description: 'Web应用渗透测试方法论',
              title: '渗透测试教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['5', '7'],
      nextSteps: [],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    },
    {
      id: '12',
      name: '安全开发生命周期',
      category: 'concept',
      difficulty: 'expert',
      value: 1,
      description: 'SDL是一种将安全实践集成到软件开发过程中的方法论。',
      keyPoints: ['需求分析', '安全设计', '代码审查', '安全测试'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'SDL实施指南',
              description: '安全开发生命周期的最佳实践',
              title: 'SDL教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: ['6', '8'],
      nextSteps: [],
      createdAt: '2023-12-01T00:00:00Z',
      updatedAt: '2023-12-01T00:00:00Z'
    }
  ],
  links: [
    { source: '1', target: '2', relation: '基础知识', value: 1 },
    { source: '1', target: '3', relation: '基础知识', value: 1 },
    { source: '1', target: '4', relation: '基础知识', value: 1 },
    { source: '2', target: '5', relation: '工具应用', value: 1 },
    { source: '2', target: '6', relation: '安全加固', value: 1 },
    { source: '3', target: '7', relation: '工具应用', value: 1 },
    { source: '3', target: '8', relation: '防御技术', value: 1 },
    { source: '4', target: '9', relation: '深入理解', value: 1 },
    { source: '4', target: '10', relation: '认证方案', value: 1 },
    { source: '5', target: '11', relation: '实践应用', value: 1 },
    { source: '7', target: '11', relation: '实践应用', value: 1 },
    { source: '6', target: '12', relation: '方法论', value: 1 },
    { source: '8', target: '12', relation: '方法论', value: 1 }
  ]
}

export function getKnowledgeGraph(): Promise<KnowledgeGraphData> {
  // 在开发环境中使用模拟数据
  if (process.env.NODE_ENV === 'development') {
    return Promise.resolve(mockKnowledgeGraph)
  }

  return request({
    url: '/api/knowledge/graph',
    method: 'get',
    timeout: 5000
  })
}

export function markNodeComplete(nodeId: string): Promise<{ status: string }> {
  return request({
    url: `/api/knowledge/node/${nodeId}/complete`,
    method: 'post'
  })
}

export function getLearningPath(nodeId: string): Promise<any> {
  return request({
    url: `/api/knowledge/path/${nodeId}`,
    method: 'get'
  })
} 