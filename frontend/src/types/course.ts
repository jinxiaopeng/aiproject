export interface Course {
  id: number
  title: string
  description: string
  cover_url?: string
  category: string
  difficulty: string
  instructor_id: number
  instructor?: {
    id: number
    username: string
    avatar?: string
  }
  chapters: Chapter[]
  progress?: number
  rating: number
  student_count: number
  created_at: string
  updated_at: string
}

export interface Chapter {
  id: number
  title: string
  description?: string
  video_url?: string
  duration?: number
  order: number
  progress?: number
  completed?: boolean
  last_position?: number
}

export interface ChapterResource {
  id: number
  name: string
  type: string
  url: string
  size?: number
  description?: string
}

export interface CourseFeature {
  icon: string
  title: string
  description: string
}

export interface CourseNote {
  id: number
  user_id: number
  course_id: number
  chapter_id?: number
  content: string
  video_time?: number
  created_at: string
  updated_at: string
}

export interface CourseComment {
  id: number
  user_id: number
  course_id: number
  content: string
  rating?: number
  user: {
    id: number
    username: string
    avatar?: string
  }
  created_at: string
  updated_at: string
}

export interface CourseEnrollment {
  id: number
  user_id: number
  course_id: number
  progress: number
  completed: boolean
  last_accessed_at: string
  created_at: string
  updated_at: string
}

export interface CourseQueryParams {
  category?: string
  difficulty?: string
  sort_by?: 'newest' | 'popular' | 'rating'
  search?: string
  page?: number
  limit?: number
}

export interface VideoInfo {
  video_url: string
  duration: number
  title: string
}

export interface ChapterProgress {
  chapter_id: number
  progress: number
  last_position: number
  completed: boolean
} 