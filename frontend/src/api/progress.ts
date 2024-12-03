import request from '@/utils/request'

export interface CourseProgress {
  id: number
  userId: number
  courseId: number
  totalLessons: number
  completedLessons: number
  totalDuration: number
  learningTime: number
  lastLessonId?: number
  progress: number
  status: 'not_started' | 'in_progress' | 'completed'
  startedAt?: string
  completedAt?: string
  createdAt: string
  updatedAt: string
}

export interface LessonProgress {
  id: number
  userId: number
  lessonId: number
  courseId: number
  progress: number
  learningTime: number
  lastPosition: number
  status: 'not_started' | 'in_progress' | 'completed'
  startedAt?: string
  completedAt?: string
  createdAt: string
  updatedAt: string
}

export interface LearningRecord {
  action: 'start' | 'pause' | 'resume' | 'complete'
  position?: number
  duration: number
}

export interface CourseStatistics {
  totalLearningTime: number
  completedLessons: number
  inProgressLessons: number
  totalLessons: number
  overallProgress: number
  status: string
}

export default {
  // 获取课程进度
  getCourseProgress(courseId: number) {
    return request.get<CourseProgress>(`/api/progress/courses/${courseId}`)
  },

  // 获取课时进度
  getLessonProgress(lessonId: number) {
    return request.get<LessonProgress>(`/api/progress/lessons/${lessonId}`)
  },

  // 记录学习行为
  recordLearningProgress(lessonId: number, record: LearningRecord) {
    return request.post<LessonProgress>(`/api/progress/lessons/${lessonId}/record`, record)
  },

  // 获取课程统计信息
  getCourseStatistics(courseId: number) {
    return request.get<CourseStatistics>(`/api/progress/courses/${courseId}/statistics`)
  }
} 