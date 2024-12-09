import request from '@/utils/request'
import type { Course, Chapter, CourseNote, CourseComment, VideoInfo, ChapterProgress } from '@/types/course'

export interface CourseQueryParams {
  category?: string
  difficulty?: string
  sort_by?: 'newest' | 'popular' | 'rating'
  search?: string
  page?: number
  limit?: number
}

// 获取课程列表
export const getCourses = async (params?: CourseQueryParams) => {
  const response = await request.get<Course[]>('/courses', { params })
  return response.data
}

// 获取课程详情
export const getCourse = async (id: number) => {
  const response = await request.get<Course>(`/courses/${id}`)
  return response.data
}

// 报名课程
export const enrollCourse = async (courseId: number) => {
  const response = await request.post(`/courses/${courseId}/enroll`)
  return response.data
}

// 获取章节视频信息
export const getChapterVideo = async (chapterId: number) => {
  const response = await request.get<VideoInfo>(`/courses/chapters/${chapterId}/video`)
  return response.data
}

// 更新章节进度
export const updateChapterProgress = async (courseId: number, chapterId: number, progress: ChapterProgress) => {
  const response = await request.post(`/courses/${courseId}/chapters/${chapterId}/progress`, progress)
  return response.data
}

// 获取课程笔记
export const getCourseNotes = async (courseId: number) => {
  const response = await request.get<CourseNote[]>(`/courses/${courseId}/notes`)
  return response.data
}

// 获取章节笔记
export const getChapterNotes = async (courseId: number, chapterId: number) => {
  const response = await request.get<CourseNote[]>(`/courses/${courseId}/chapters/${chapterId}/notes`)
  return response.data
}

// 创建笔记
export const createNote = async (courseId: number, data: { chapter_id?: number; content: string }) => {
  const response = await request.post<CourseNote>(`/courses/${courseId}/notes`, data)
  return response.data
}

// 更新笔记
export const updateNote = async (courseId: number, noteId: number, data: { content: string }) => {
  const response = await request.put<CourseNote>(`/courses/${courseId}/notes/${noteId}`, data)
  return response.data
}

// 删除笔记
export const deleteNote = async (courseId: number, noteId: number) => {
  const response = await request.delete(`/courses/${courseId}/notes/${noteId}`)
  return response.data
}

// 获取课程评论
export const getCourseComments = async (courseId: number) => {
  const response = await request.get<CourseComment[]>(`/courses/${courseId}/comments`)
  return response.data
}

// 创建评论
export const createComment = async (courseId: number, data: { content: string; rating?: number }) => {
  const response = await request.post<CourseComment>(`/courses/${courseId}/comments`, data)
  return response.data
}

// 上传章节视频
export const uploadChapterVideo = (chapterId: number, file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post(`/courses/chapters/${chapterId}/upload-video`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 