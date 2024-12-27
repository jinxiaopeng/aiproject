import type { CareerPathResponse, CareerPathRequest } from '../types/career'
import request from '@/utils/request'

// 模拟数据
const MOCK_CAREER_PATHS: Record<string, CareerPathResponse> = {
  '渗透测试工程师': {
    path: [
      {
        id: '1',
        name: '网络基础知识',
        description: '学习计算机网络的基本概念和协议',
        difficulty: '入门',
        tags: ['网络', 'TCP/IP', 'HTTP'],
        keyPoints: [
          'OSI七层模型',
          'TCP/IP协议栈',
          'HTTP/HTTPS协议',
          '常见网络服务'
        ]
      },
      {
        id: '2',
        name: '操作系统基础',
        description: '掌握Linux和Windows操作系统的基本使用',
        difficulty: '基础',
        tags: ['Linux', 'Windows', '命令行'],
        keyPoints: [
          'Linux基本命令',
          'Shell脚本编写',
          'Windows系统管理',
          '权限管理'
        ]
      },
      {
        id: '3',
        name: '编程基础',
        description: '学习基本的编程语言和脚本编写',
        difficulty: '基础',
        tags: ['Python', 'Shell', '脚本'],
        keyPoints: [
          'Python基础语法',
          '自动化脚本编写',
          '正则表达式',
          '数据处理'
        ]
      },
      {
        id: '4',
        name: '渗透测试基础',
        description: '了解基本的渗透测试方法和工具',
        difficulty: '进阶',
        tags: ['渗透测试', '工具使用', '漏洞扫描'],
        keyPoints: [
          '信息收集技术',
          '漏洞扫描工具',
          '基本漏洞原理',
          '渗透测试方法论'
        ]
      },
      {
        id: '5',
        name: 'Web安全',
        description: '深入学习Web应用安全测试',
        difficulty: '进阶',
        tags: ['Web安全', 'OWASP', 'XSS', 'SQL注入'],
        keyPoints: [
          'OWASP Top 10',
          'Web漏洞原理',
          '漏洞利用技术',
          '安全防护方案'
        ]
      },
      {
        id: '6',
        name: '高级渗透技术',
        description: '学习高级渗透测试技术和方法',
        difficulty: '高级',
        tags: ['高级渗透', '后渗透', '社会工程'],
        keyPoints: [
          '后渗透技术',
          '权限提升',
          '横向移动',
          '痕迹清理'
        ]
      }
    ],
    estimatedTime: '6-8个月',
    difficulty: '中等',
    prerequisites: ['计算机基础知识', '英语阅读能力']
  },
  '安全开发工程师': {
    path: [
      {
        id: '1',
        name: '编程基础',
        description: '掌握基本的编程语言和开发技能',
        difficulty: '入门',
        tags: ['Java', 'Python', '编程基础'],
        keyPoints: [
          '编程语言基础',
          '数据结构与算法',
          '面向对象编程',
          '代码版本控制'
        ]
      },
      {
        id: '2',
        name: '网络与系统基础',
        description: '了解网络协议和操作系统原理',
        difficulty: '基础',
        tags: ['网络', '操作系统', 'Linux'],
        keyPoints: [
          '网络协议栈',
          '系统架构',
          'Linux系统编程',
          '网络编程'
        ]
      },
      {
        id: '3',
        name: '安全开发基础',
        description: '学习基本的安全开发概念和实践',
        difficulty: '基础',
        tags: ['安全编程', '代码审计', '漏洞修复'],
        keyPoints: [
          '安全编码规范',
          '常见漏洞原理',
          '安全测试方法',
          '漏洞修复技术'
        ]
      },
      {
        id: '4',
        name: '应用安全开发',
        description: '掌握安全功能的设计与实现',
        difficulty: '进阶',
        tags: ['认证授权', '加密解密', '安全架构'],
        keyPoints: [
          '身份认证',
          '访问控制',
          '密码学应用',
          '安全架构设计'
        ]
      },
      {
        id: '5',
        name: '安全工具开发',
        description: '开发安全评估和防护工具',
        difficulty: '进阶',
        tags: ['工具开发', '自动化', '漏洞扫描'],
        keyPoints: [
          '扫描器开发',
          'WAF规则开发',
          '自动化测试',
          '威胁检测'
        ]
      },
      {
        id: '6',
        name: '高级安全研发',
        description: '研究和开发高级安全防护方案',
        difficulty: '高级',
        tags: ['研发', '创新', '架构设计'],
        keyPoints: [
          '安全框架开发',
          '零信任架构',
          '云安全开发',
          '新技术研究'
        ]
      }
    ],
    estimatedTime: '8-12个月',
    difficulty: '高级',
    prerequisites: ['编程基础', '计算机网络基础']
  },
  '安全运维工程师': {
    path: [
      {
        id: '1',
        name: '系统运维基础',
        description: '掌握基本的系统运维技能',
        difficulty: '入门',
        tags: ['Linux', 'Windows', '运维基础'],
        keyPoints: [
          '系统管理',
          '服务配置',
          '监控部署',
          '日志管理'
        ]
      },
      {
        id: '2',
        name: '网络安全基础',
        description: '了解网络安全基本概念和防护方法',
        difficulty: '基础',
        tags: ['网络安全', '防火墙', 'IDS/IPS'],
        keyPoints: [
          '网络架构',
          '安全设备',
          '访问控制',
          '流量分析'
        ]
      },
      {
        id: '3',
        name: '安全运维实践',
        description: '学习安全运维的具体实践方法',
        difficulty: '进阶',
        tags: ['安全加固', '应急响应', '漏洞修复'],
        keyPoints: [
          '系统加固',
          '漏洞管理',
          '补丁更新',
          '安全审计'
        ]
      },
      {
        id: '4',
        name: '安全运营',
        description: '掌握安全运营的核心技能',
        difficulty: '进阶',
        tags: ['运营', 'SOC', '应急响应'],
        keyPoints: [
          'SOC建设',
          '威胁处置',
          '事件响应',
          '安全运营'
        ]
      }
    ],
    estimatedTime: '4-6个月',
    difficulty: '中等',
    prerequisites: ['Linux系统基础', '网络基础']
  }
}

export async function generateCareerPath(
  career: string,
  preferences?: CareerPathRequest['preferences']
): Promise<CareerPathResponse> {
  try {
    // 在实际环境中调用API
    const response = await request({
      url: '/api/knowledge/career-path',
      method: 'post',
      data: {
        career,
        preferences
      }
    })
    return response.data
  } catch (error) {
    console.error('Failed to generate career path:', error)
    // 返回模拟数据
    const mockPath = MOCK_CAREER_PATHS[career]
    if (!mockPath) {
      throw new Error('未找到该职业的学习路径，请尝试其他职业方向')
    }
    return mockPath
  }
} 