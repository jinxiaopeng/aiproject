import type { Course } from '@/types/course'

// 课程分类
export const courseCategories = [
  { key: 'web', label: 'Web安全', icon: 'Monitor' },
  { key: 'system', label: '系统安全', icon: 'Setting' },
  { key: 'network', label: '网络安全', icon: 'Connection' },
  { key: 'crypto', label: '密码学', icon: 'Lock' },
  { key: 'secure_dev', label: '安全开发', icon: 'Code' },
  { key: 'mobile', label: '移动安全', icon: 'Cellphone' },
  { key: 'blockchain', label: '区块链安全', icon: 'Link' },
  { key: 'cloud', label: '云安全', icon: 'CloudServer' }
]

// 课程难度
export const courseDifficulties = [
  { key: 'beginner', label: '入门', color: '#10B981' },
  { key: 'elementary', label: '初级', color: '#3B82F6' },
  { key: 'intermediate', label: '中级', color: '#F59E0B' },
  { key: 'advanced', label: '高级', color: '#EF4444' }
]

// 推荐课程
export const featuredCourses: Course[] = [
  {
    id: 1,
    title: 'Web安全基础入门',
    description: '学习Web安全的基本概念和常见漏洞原理',
    cover_url: '/images/courses/web-security-basic.jpg',
    category: 'web',
    difficulty: 'beginner',
    duration: 120,
    student_count: 1234,
    rating: 4.5,
    instructor: {
      id: 1,
      name: '张教授',
      avatar: '/images/avatars/teacher1.jpg',
      title: '资深Web安全专家'
    },
    created_at: '2023-12-01',
    updated_at: '2023-12-01',
    chapters: [
      {
        id: 1,
        title: 'Web安全概述',
        lessons: [
          { id: 1, title: '什么是Web安全', duration: 15 },
          { id: 2, title: '常见Web漏洞类型', duration: 20 }
        ]
      }
    ]
  },
  {
    id: 2,
    title: 'XSS跨站脚本攻击与防御',
    description: '深入理解XSS漏洞的原理和防护方法',
    cover_url: '/images/courses/xss-defense.jpg',
    category: 'web',
    difficulty: 'intermediate',
    duration: 180,
    student_count: 856,
    rating: 4.8,
    instructor: {
      id: 2,
      name: '李老师',
      avatar: '/images/avatars/teacher2.jpg',
      title: 'Web安全研究员'
    },
    created_at: '2023-12-10',
    updated_at: '2023-12-10',
    chapters: [
      {
        id: 1,
        title: 'XSS漏洞基础',
        lessons: [
          { id: 1, title: 'XSS漏洞原理', duration: 25 },
          { id: 2, title: 'XSS漏洞类型', duration: 30 }
        ]
      }
    ]
  }
]

// 所有课程
export const allCourses: Course[] = [
  ...featuredCourses,
  {
    id: 3,
    title: 'SQL注入高级利用技巧',
    description: '掌握SQL注入的高级利用方法和防御策略',
    cover_url: '/images/courses/sql-injection.jpg',
    category: 'web',
    difficulty: 'advanced',
    duration: 240,
    student_count: 567,
    rating: 4.9,
    instructor: {
      id: 3,
      name: '王教授',
      avatar: '/images/avatars/teacher3.jpg',
      title: '数据库安全专家'
    },
    created_at: '2023-12-15',
    updated_at: '2023-12-15',
    chapters: [
      {
        id: 1,
        title: 'SQL注入基础回顾',
        lessons: [
          { id: 1, title: 'SQL注入原理', duration: 30 },
          { id: 2, title: 'SQL注入类型', duration: 35 }
        ]
      }
    ]
  },
  {
    id: 4,
    title: '系统安全与权限提升',
    description: '学习系统安全基础知识和权限提升技术',
    cover_url: '/images/courses/system-security.jpg',
    category: 'system',
    difficulty: 'intermediate',
    duration: 200,
    student_count: 789,
    rating: 4.7,
    instructor: {
      id: 4,
      name: '刘教授',
      avatar: '/images/avatars/teacher4.jpg',
      title: '系统安全专家'
    },
    created_at: '2023-12-12',
    updated_at: '2023-12-12',
    chapters: [
      {
        id: 1,
        title: '系统安全基础',
        lessons: [
          { id: 1, title: '操作系统安全概述', duration: 25 },
          { id: 2, title: '权限控制基础', duration: 30 }
        ]
      }
    ]
  },
  {
    id: 5,
    title: '网络协议安全分析',
    description: '深入分析网络协议安全问题和防护方案',
    cover_url: '/images/courses/network-protocol.jpg',
    category: 'network',
    difficulty: 'advanced',
    duration: 180,
    student_count: 623,
    rating: 4.8,
    instructor: {
      id: 5,
      name: '张工程师',
      avatar: '/images/avatars/teacher5.jpg',
      title: '网络安全研究员'
    },
    created_at: '2023-12-20',
    updated_at: '2023-12-20',
    chapters: [
      {
        id: 1,
        title: '网络协议基础',
        lessons: [
          { id: 1, title: 'TCP/IP协议栈安全', duration: 40 },
          { id: 2, title: '常见网络攻击分析', duration: 35 }
        ]
      }
    ]
  },
  {
    id: 6,
    title: '密码学原理与应用',
    description: '学习现代密码学基础理论和实践应用',
    cover_url: '/images/courses/cryptography.jpg',
    category: 'crypto',
    difficulty: 'intermediate',
    duration: 160,
    student_count: 445,
    rating: 4.6,
    instructor: {
      id: 6,
      name: '李研究员',
      avatar: '/images/avatars/teacher6.jpg',
      title: '密码学专家'
    },
    created_at: '2023-12-18',
    updated_at: '2023-12-18',
    chapters: [
      {
        id: 1,
        title: '密码学基础',
        lessons: [
          { id: 1, title: '现代密码学概述', duration: 30 },
          { id: 2, title: '对称加密算法', duration: 35 }
        ]
      }
    ]
  },
  {
    id: 7,
    title: '安全开发实践指南',
    description: '掌握安全开发的最佳实践和编码规范',
    cover_url: '/images/courses/secure-dev.jpg',
    category: 'secure_dev',
    difficulty: 'intermediate',
    duration: 210,
    student_count: 567,
    rating: 4.7,
    instructor: {
      id: 7,
      name: '王工程师',
      avatar: '/images/avatars/teacher7.jpg',
      title: '安全开发专家'
    },
    created_at: '2023-12-16',
    updated_at: '2023-12-16',
    chapters: [
      {
        id: 1,
        title: '安全开发基础',
        lessons: [
          { id: 1, title: '代码安全原则', duration: 35 },
          { id: 2, title: '常见漏洞防护', duration: 40 }
        ]
      }
    ]
  },
  {
    id: 8,
    title: '移动应用安全测试',
    description: '学习移动应用的安全测试方法和工具使用',
    cover_url: '/images/courses/mobile-security.jpg',
    category: 'mobile',
    difficulty: 'intermediate',
    duration: 190,
    student_count: 389,
    rating: 4.5,
    instructor: {
      id: 8,
      name: '陈工程师',
      avatar: '/images/avatars/teacher8.jpg',
      title: '移动安全专家'
    },
    created_at: '2023-12-14',
    updated_at: '2023-12-14',
    chapters: [
      {
        id: 1,
        title: '移动安全基础',
        lessons: [
          { id: 1, title: 'Android安全基础', duration: 30 },
          { id: 2, title: 'iOS安全基础', duration: 35 }
        ]
      }
    ]
  },
  {
    id: 9,
    title: '区块链安全入门',
    description: '了解区块链技术的安全特性和漏洞防护',
    cover_url: '/images/courses/blockchain.jpg',
    category: 'blockchain',
    difficulty: 'elementary',
    duration: 150,
    student_count: 234,
    rating: 4.4,
    instructor: {
      id: 9,
      name: '赵研究员',
      avatar: '/images/avatars/teacher9.jpg',
      title: '区块链安全专家'
    },
    created_at: '2023-12-13',
    updated_at: '2023-12-13',
    chapters: [
      {
        id: 1,
        title: '区块链安全基础',
        lessons: [
          { id: 1, title: '区块链原理', duration: 25 },
          { id: 2, title: '智能合约安全', duration: 30 }
        ]
      }
    ]
  },
  {
    id: 10,
    title: '云安全架构设计',
    description: '学习云环境下的安全架构设计和最佳实践',
    cover_url: '/images/courses/cloud-security.jpg',
    category: 'cloud',
    difficulty: 'advanced',
    duration: 220,
    student_count: 456,
    rating: 4.8,
    instructor: {
      id: 10,
      name: '孙架构师',
      avatar: '/images/avatars/teacher10.jpg',
      title: '云安全架构师'
    },
    created_at: '2023-12-11',
    updated_at: '2023-12-11',
    chapters: [
      {
        id: 1,
        title: '云安全基础',
        lessons: [
          { id: 1, title: '云计算安全概述', duration: 35 },
          { id: 2, title: '云安全架构原则', duration: 40 }
        ]
      }
    ]
  }
]

// 课程统计数据
export const courseStats = {
  totalCourses: allCourses.length,
  totalStudents: allCourses.reduce((total, course) => total + course.student_count, 0),
  averageRating: Number((allCourses.reduce((total, course) => total + course.rating, 0) / allCourses.length).toFixed(1))
}

// 课程学习数据
export const learningCourseData = {
  id: 1,
  title: "Web安全渗透测试实战",
  description: "系统学习Web安全渗透测试技术",
  cover_url: "/images/courses/course1.jpg",
  chapters: [
    {
      id: 1,
      title: "Web安全概述",
      description: "了解Web安全的基本概念和重要性",
      duration: 45,
      progress: 0,
      video_url: "/videos/chapter1.mp4"  // 使用现有视频
    },
    {
      id: 2,
      title: "常见Web漏洞分析",
      description: "学习SQL注入、XSS等常见漏洞的原理",
      duration: 60,
      progress: 0,
      video_url: "/videos/chapter1.mp4"  // 暂时使用同一个视频
    }
  ]
} 