import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Challenge {
  id: number
  title: string
  description: string
  category: string
  difficulty: 'beginner' | 'easy' | 'medium' | 'hard' | 'expert'
  points: number
  status: 'not_started' | 'in_progress' | 'completed'
  completionRate: number
  tags: string[]
  solvedCount?: number
  totalAttempts?: number
  environment?: {
    type: string
    url: string
    port: number
  }
}

// 初始题目数据
const initialChallenges: Challenge[] = [
  {
    id: 1,
    title: 'SQL注入基础训练',
    description: '学习SQL注入的基本原理和防御方法',
    category: 'web',
    difficulty: 'beginner',
    points: 100,
    status: 'not_started',
    completionRate: 75,
    tags: ['SQL注入', 'Web安全']
  },
  {
    id: 2,
    title: 'SQL注入进阶挑战',
    description: '一个模拟管理员登录系统的SQL注入挑战，需要绕过密码哈希并获取管理员权限',
    category: 'web',
    difficulty: 'medium',
    points: 200,
    status: 'not_started',
    completionRate: 45,
    tags: ['SQL注入', 'Web安全', '密码哈���', '权限提升']
  },
  {
    id: 3,
    title: 'XSS跨站脚本攻击',
    description: '掌握XSS攻击的各种类型和防御措施',
    category: 'web',
    difficulty: 'easy',
    points: 150,
    status: 'in_progress',
    completionRate: 30,
    tags: ['XSS', 'Web安全']
  },
  {
    id: 4,
    title: '文件上传漏洞利用',
    description: '深入理解文件上传漏洞的原理和防护方法',
    category: 'web',
    difficulty: 'medium',
    points: 200,
    status: 'completed',
    completionRate: 100,
    tags: ['文件上传', 'Web安全']
  },
  {
    id: 5,
    title: 'Linux权限提升',
    description: '学习Linux系统下的权限提升技术',
    category: 'system',
    difficulty: 'hard',
    points: 300,
    status: 'not_started',
    completionRate: 0,
    tags: ['Linux', '权限提升']
  },
  {
    id: 6,
    title: '密码学基础挑战',
    description: '掌握基本的密码学原理和实践',
    category: 'crypto',
    difficulty: 'beginner',
    points: 100,
    status: 'not_started',
    completionRate: 0,
    tags: ['密码学', '加密解密']
  },
  {
    id: 7,
    title: '逆向工程入门',
    description: '学习基础的逆向工程技术和工具使用',
    category: 'reverse',
    difficulty: 'medium',
    points: 250,
    status: 'not_started',
    completionRate: 0,
    tags: ['逆向工程', '反编译']
  },
  {
    id: 8,
    title: 'CSRF跨站请求伪造',
    description: '理解CSRF攻击原理与防御策略',
    category: 'web',
    difficulty: 'medium',
    points: 200,
    status: 'not_started',
    completionRate: 0,
    tags: ['CSRF', 'Web安全']
  },
  {
    id: 9,
    title: 'Docker容器逃逸',
    description: '探索Docker容器安全与逃逸技术',
    category: 'system',
    difficulty: 'expert',
    points: 400,
    status: 'not_started',
    completionRate: 0,
    tags: ['Docker', '容器安全']
  },
  {
    id: 10,
    title: 'JWT令牌安全',
    description: '学习JWT的安全使用与常见漏洞',
    category: 'web',
    difficulty: 'easy',
    points: 150,
    status: 'not_started',
    completionRate: 0,
    tags: ['JWT', 'Web安全']
  },
  {
    id: 11,
    title: 'Android应用逆向',
    description: '安卓应用的静态分析与动态调试',
    category: 'mobile',
    difficulty: 'hard',
    points: 350,
    status: 'not_started',
    completionRate: 0,
    tags: ['Android', '移动安全']
  },
  {
    id: 12,
    title: '内存取证分析',
    description: '系统内存镜像的取证分析技术',
    category: 'forensics',
    difficulty: 'medium',
    points: 250,
    status: 'not_started',
    completionRate: 0,
    tags: ['内存取证', '数字取证']
  },
  {
    id: 13,
    title: '网络流量分析',
    description: '网络数据包的捕获与分析技术',
    category: 'network',
    difficulty: 'easy',
    points: 150,
    status: 'not_started',
    completionRate: 0,
    tags: ['流量分析', '网络安全']
  },
  {
    id: 14,
    title: 'Windows提权实战',
    description: 'Windows系统的权限提升技术',
    category: 'system',
    difficulty: 'hard',
    points: 300,
    status: 'not_started',
    completionRate: 0,
    tags: ['Windows', '权限提升']
  },
  {
    id: 15,
    title: 'Python代码审计',
    description: 'Python应用的安全漏洞分析',
    category: 'code',
    difficulty: 'medium',
    points: 200,
    status: 'not_started',
    completionRate: 0,
    tags: ['代码审计', 'Python安全']
  },
  {
    id: 16,
    title: '区块链智能合约',
    description: '智能合约安全漏洞分析与利用',
    category: 'blockchain',
    difficulty: 'expert',
    points: 400,
    status: 'not_started',
    completionRate: 0,
    tags: ['区块链', '智能合约']
  }
]

export const useStore = defineStore('challenge', () => {
  const challenges = ref<Challenge[]>(initialChallenges)  // 使用初始数据

  // 添加新的题目
  function addChallenge(challenge: Challenge) {
    challenges.value.push(challenge)
  }

  // 获取所有题目
  function getChallenges() {
    return challenges.value
  }

  // 更新题目状态
  function updateChallengeStatus(id: number, status: Challenge['status']) {
    const challenge = challenges.value.find(c => c.id === id)
    if (challenge) {
      challenge.status = status
    }
  }

  // 更新完成率
  function updateCompletionRate(id: number, rate: number) {
    const challenge = challenges.value.find(c => c.id === id)
    if (challenge) {
      challenge.completionRate = rate
    }
  }

  return {
    challenges,
    addChallenge,
    getChallenges,
    updateChallengeStatus,
    updateCompletionRate
  }
}) 