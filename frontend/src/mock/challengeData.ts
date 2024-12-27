// 挑战分类数据
export const categories = [
  { id: 1, name: 'Web安全', icon: 'web', color: '#409eff' },
  { id: 2, name: '系统安全', icon: 'system', color: '#67c23a' },
  { id: 3, name: '密码学', icon: 'crypto', color: '#e6a23c' },
  { id: 4, name: '逆向工程', icon: 'reverse', color: '#f56c6c' },
  { id: 5, name: '二进制', icon: 'binary', color: '#909399' },
  { id: 6, name: '移动安全', icon: 'mobile', color: '#9c27b0' }
]

// 难度等级数据
export const difficultyLevels = [
  { id: 1, name: '入门', value: 'beginner', color: '#409eff' },
  { id: 2, name: '简单', value: 'easy', color: '#67c23a' },
  { id: 3, name: '中等', value: 'medium', color: '#e6a23c' },
  { id: 4, name: '困难', value: 'hard', color: '#f56c6c' },
  { id: 5, name: '专家', value: 'expert', color: '#800080' }
]

// 挑战状态数据
export const challengeStatuses = [
  { id: 1, name: '未开始', value: 'not_started', color: '#909399' },
  { id: 2, name: '进行中', value: 'in_progress', color: '#e6a23c' },
  { id: 3, name: '已完成', value: 'completed', color: '#67c23a' }
]

// 模拟挑战数据
export const mockChallenges = [
  {
    id: 1,
    title: 'SQL注入基础训练',
    description: '学习SQL注入的基本原理和防御方法，包括常见的注入类型和防护措施。本题目将帮助你理解SQL注入漏洞的原理，以及如何使用各种工具进行漏洞利用和防护。',
    category: 'web',
    difficulty: 'beginner',
    points: 100,
    status: 'not_started',
    completionRate: 0,
    tags: ['SQL注入', 'Web安全', '数据库'],
    estimatedTime: '2小时',
    prerequisites: ['基础HTML', 'SQL基础'],
    tools: ['BurpSuite', 'SQLMap'],
    createTime: '2023-12-01',
    updateTime: '2023-12-15',
    targetUrl: 'http://challenge-1.example.com:8080',
    targetPort: 8080,
    containerStatus: 'stopped'
  },
  {
    id: 2,
    title: 'XSS跨站脚本攻击',
    description: '掌握XSS攻击的各种类型和防御措施，包括存储型、反射型和DOM型XSS。通过本题目，你将学习如何发现和利用XSS漏洞，以及如何实施有效的防护措施。',
    category: 'web',
    difficulty: 'easy',
    points: 150,
    status: 'running',
    completionRate: 45,
    tags: ['XSS', 'Web安全', 'JavaScript'],
    estimatedTime: '3小时',
    prerequisites: ['JavaScript基础', 'Web基础'],
    tools: ['Chrome DevTools', 'BurpSuite'],
    createTime: '2023-12-02',
    updateTime: '2023-12-16',
    targetUrl: 'http://challenge-2.example.com:8081',
    targetPort: 8081,
    containerStatus: 'running',
    remainingTime: 3600
  },
  {
    id: 3,
    title: '文件上传漏洞利用',
    description: '深入理解文件上传漏洞的原理和防护方法，包括绕过技术和安全防护。你将学习各种文件上传限制的绕过技术，以及如何构建安全的文件上传功能。',
    category: 'web',
    difficulty: 'medium',
    points: 200,
    status: 'completed',
    completionRate: 100,
    tags: ['文件上传', 'Web安全', '漏洞利用'],
    estimatedTime: '4小时',
    prerequisites: ['PHP基础', 'Web服务器基础'],
    tools: ['BurpSuite', 'Shell'],
    createTime: '2023-12-03',
    updateTime: '2023-12-17',
    targetUrl: 'http://challenge-3.example.com:8082',
    targetPort: 8082,
    containerStatus: 'stopped'
  }
]

// 模拟用户进度数据
export const mockProgress = {
  totalChallenges: 50,
  completedChallenges: 15,
  inProgressChallenges: 3,
  totalPoints: 1250,
  weeklyProgress: [
    { day: '周一', completed: 2 },
    { day: '周二', completed: 1 },
    { day: '周三', completed: 3 },
    { day: '周四', completed: 0 },
    { day: '周五', completed: 2 },
    { day: '周六', completed: 4 },
    { day: '周日', completed: 1 }
  ],
  categoryProgress: [
    { name: 'Web安全', completed: 8, total: 20 },
    { name: '系统安全', completed: 3, total: 10 },
    { name: '密码学', completed: 2, total: 8 },
    { name: '逆向工程', completed: 1, total: 7 },
    { name: '二进制', completed: 1, total: 5 }
  ]
}

// 模拟成就数据
export const mockAchievements = [
  {
    id: 1,
    name: '初出茅庐',
    description: '完成第一个靶场训练',
    icon: 'Trophy',
    unlocked: true,
    unlockedAt: '2023-12-01'
  },
  {
    id: 2,
    name: '坚持不懈',
    description: '连续7天完成训练',
    icon: 'Medal',
    unlocked: true,
    unlockedAt: '2023-12-10'
  },
  {
    id: 3,
    name: '全能选手',
    description: '每个分类至少完成一个靶场',
    icon: 'Star',
    unlocked: false
  }
] 