// 课程难度
export type CourseDifficulty = 'beginner' | 'elementary' | 'intermediate' | 'advanced'

// 课程分类
export type CourseCategory = 'web' | 'system' | 'network' | 'crypto' | 'secure_dev' | 'mobile' | 'blockchain' | 'cloud'

// 课程讲师
export interface Instructor {
  id: number
  name: string
  avatar: string
  title: string
}

// 课程章节
export interface Chapter {
  id: number
  title: string
  lessons: Lesson[]
}

// 课程课时
export interface Lesson {
  id: number
  title: string
  duration: number
}

// 课程评论
export interface CourseComment {
  id: number
  user: {
    id: number
    name: string
    avatar: string
  }
  content: string
  rating: number
  created_at: string
}

// 课程特性
export interface CourseFeature {
  icon: string
  title: string
  description: string
}

// 课程
export interface Course {
  id: number
  title: string
  description: string
  cover_url: string
  category: CourseCategory
  difficulty: CourseDifficulty
  duration: number
  student_count: number
  rating: number
  instructor: Instructor
  chapters: Chapter[]
  created_at: string
  updated_at: string
} 