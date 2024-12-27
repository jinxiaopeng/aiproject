interface Node {
  id: number
  name: string
  category: string
  description: string
}

interface Link {
  id: number
  source: number
  target: number
  value: number
}

export const generateMockData = () => {
  const nodes: Node[] = [
    {
      id: 1,
      name: 'Web安全基础',
      category: 'security',
      description: 'Web安全的基本概念和原理'
    },
    {
      id: 2,
      name: 'HTTP协议',
      category: 'web',
      description: 'HTTP协议的工作原理和安全特性'
    },
    {
      id: 3,
      name: 'SQL注入',
      category: 'security',
      description: 'SQL注入攻击原理和防御方法'
    },
    {
      id: 4,
      name: 'XSS攻击',
      category: 'security',
      description: '跨站脚本攻击原理和防御措施'
    },
    {
      id: 5,
      name: '网络协议',
      category: 'network',
      description: '常见网络协议及其安全性'
    },
    {
      id: 6,
      name: '操作系统安全',
      category: 'system',
      description: '操作系统安全基础和防护'
    },
    {
      id: 7,
      name: '数据库安全',
      category: 'database',
      description: '数据库安全原理和实践'
    },
    {
      id: 8,
      name: 'CSRF攻击',
      category: 'security',
      description: '跨站请求伪造攻击原理和防御'
    },
    {
      id: 9,
      name: '身份认证',
      category: 'security',
      description: '身份认证机制和安全实现'
    },
    {
      id: 10,
      name: '加密算法',
      category: 'security',
      description: '常用加密算法原理和应用'
    },
    {
      id: 11,
      name: 'HTTPS协议',
      category: 'web',
      description: 'HTTPS的工作原理和安全机制'
    },
    {
      id: 12,
      name: '网络防火墙',
      category: 'network',
      description: '防火墙的原理和配置方法'
    },
    {
      id: 13,
      name: '漏洞扫描',
      category: 'security',
      description: '系统漏洞扫描技术和工具'
    },
    {
      id: 14,
      name: '代码审计',
      category: 'security',
      description: '源代码安全审计方法'
    },
    {
      id: 15,
      name: '渗透测试',
      category: 'security',
      description: '渗透测试方法和工具'
    },
    {
      id: 16,
      name: 'Docker安全',
      category: 'system',
      description: 'Docker容器安全防护'
    },
    {
      id: 17,
      name: '云安全',
      category: 'system',
      description: '云计算环境下的安全防护'
    },
    {
      id: 18,
      name: '密码学',
      category: 'security',
      description: '现代密码学基础理论'
    },
    {
      id: 19,
      name: '网络监控',
      category: 'network',
      description: '网络流量监控和分析'
    },
    {
      id: 20,
      name: '应急响应',
      category: 'security',
      description: '安全事件应急处理流程'
    },
    {
      id: 21,
      name: 'Redis安全',
      category: 'database',
      description: 'Redis数据库安全配置'
    },
    {
      id: 22,
      name: 'MongoDB安全',
      category: 'database',
      description: 'MongoDB安全最佳实践'
    },
    {
      id: 23,
      name: 'JWT认证',
      category: 'web',
      description: 'JWT的原理和安全使用'
    },
    {
      id: 24,
      name: 'OAuth2.0',
      category: 'web',
      description: 'OAuth2.0授权框架'
    },
    {
      id: 25,
      name: '安全架构',
      category: 'security',
      description: '系统安全架构设计'
    },
    {
      id: 26,
      name: '威胁建模',
      category: 'security',
      description: '系统威胁分析和建模'
    },
    {
      id: 27,
      name: '安全开���',
      category: 'security',
      description: '安全软件开发生命周期'
    },
    {
      id: 28,
      name: '安全测试',
      category: 'security',
      description: '软件安全测试方法'
    },
    {
      id: 29,
      name: '网络攻防',
      category: 'security',
      description: '网络攻击与防御技术'
    },
    {
      id: 30,
      name: '安全运维',
      category: 'system',
      description: '系统安全运维实践'
    }
  ]

  // 优化连接生成逻辑
  const links: Link[] = []
  let linkId = 1
  const connectionSet = new Set<string>() // 用于记录已经存在的连接

  // 为每个节点创建合适的连接
  nodes.forEach(node => {
    // 根据节点类别找到相关的目标节点
    const relatedNodes = nodes.filter(target => {
      // 避免自连接
      if (target.id === node.id) return false
      
      // 检查是否已存在连接
      const connectionKey1 = `${node.id}-${target.id}`
      const connectionKey2 = `${target.id}-${node.id}`
      if (connectionSet.has(connectionKey1) || connectionSet.has(connectionKey2)) return false

      // 根据类别判断是否应该连接
      return shouldConnect(node.category, target.category)
    })

    // 从相关节点中选择1-2个建立连接
    const numLinks = Math.min(relatedNodes.length, Math.floor(Math.random() * 2) + 1)
    for (let i = 0; i < numLinks; i++) {
      const targetIndex = Math.floor(Math.random() * relatedNodes.length)
      const target = relatedNodes[targetIndex]
      
      // 记录连接
      const connectionKey = `${node.id}-${target.id}`
      connectionSet.add(connectionKey)
      
      links.push({
        id: linkId++,
        source: node.id,
        target: target.id,
        value: 1
      })

      // 从候选列表中移除已连接的节点
      relatedNodes.splice(targetIndex, 1)
    }
  })

  return { nodes, links }
}

// 判断两个类别之间是否应该建立连接
const shouldConnect = (category1: string, category2: string) => {
  // 定义类别之间的关联规则
  const relationRules: { [key: string]: string[] } = {
    'security': ['web', 'network', 'system', 'database', 'security'],
    'web': ['security', 'network'],
    'network': ['security', 'web', 'system'],
    'system': ['security', 'network', 'database'],
    'database': ['security', 'system']
  }

  // 检查是否存在关联关系
  return relationRules[category1]?.includes(category2) || false
} 