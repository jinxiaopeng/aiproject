import request from '../utils/request'
import type { AxiosResponse } from 'axios'

export interface Course {
  id: number
  title: string
  description: string
  cover_image?: string
  level: 'beginner' | 'intermediate' | 'advanced'
  category: string
  duration: number
  status: 'draft' | 'published' | 'archived'
  created_by: number
  created_at: string
  updated_at: string
  lessons_count?: number
  student_count?: number
}

export interface Chapter {
  id: number
  course_id: number
  title: string
  description?: string
  order_num: number
  created_at: string
  updated_at: string
}

export interface Lesson {
  id: number
  course_id: number
  chapter_id?: number
  title: string
  content: string
  duration: number
  order_num: number
  type: 'text' | 'video' | 'quiz'
  resources?: {
    video_url?: string
    attachments?: string[]
  }
  created_at: string
  updated_at: string
}

export interface CourseDetail extends Course {
  chapters: Chapter[]
  lessons: Lesson[]
}

export interface CourseQuery {
  category?: string
  difficulty?: string
  search?: string
}

export interface CreateCourseData {
  title: string
  description: string
  cover_image?: string
  level: string
  category: string
  duration: number
  status: string
}

export interface UpdateCourseData {
  title?: string
  description?: string
  cover_image?: string
  level?: string
  category?: string
  duration?: number
  status?: string
}

export interface LearningProgress {
  id: number
  user_id: number
  course_id: number
  progress: number
  last_lesson_id?: number
  created_at: string
  updated_at: string
}

const courseApi = {
  // 课程基础操作
  getCourses(params?: CourseQuery): Promise<AxiosResponse<Course[]>> {
    return request.get('/api/courses', { params })
  },

  getCourseDetail(id: number): Promise<AxiosResponse<CourseDetail>> {
    return request.get(`/api/courses/${id}`)
  },

  createCourse(data: CreateCourseData): Promise<AxiosResponse<Course>> {
    return request.post('/api/courses', data)
  },

  updateCourse(id: number, data: UpdateCourseData): Promise<AxiosResponse<Course>> {
    return request.put(`/api/courses/${id}`, data)
  },

  deleteCourse(id: number): Promise<AxiosResponse<void>> {
    return request.delete(`/api/courses/${id}`)
  },

  // 章节和课时
  getCourseChapters(courseId: number): Promise<AxiosResponse<Chapter[]>> {
    return request.get(`/api/courses/${courseId}/chapters`)
  },

  getLessonDetail(courseId: number, lessonId: number): Promise<AxiosResponse<Lesson>> {
    return request.get(`/api/courses/${courseId}/lessons/${lessonId}`)
  },

  // 学习进度
  updateProgress(courseId: number, data: { lesson_id: number; progress: number }): Promise<AxiosResponse<LearningProgress>> {
    return request.post(`/api/courses/${courseId}/progress`, data)
  },

  // 推荐课程
  getRecommendedCourses(): Promise<AxiosResponse<Course[]>> {
    return request.get('/api/courses/recommended')
  }
}

export default courseApi 