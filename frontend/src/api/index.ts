import request from '../utils/request'

// 类型定义
export interface Course {
  id: number
  title: string
  description: string
  category: string
  difficulty_level: number
  cover_image?: string
  created_at: string
  updated_at: string
  lessons_count?: number
  duration?: number
  progress?: number
  tags?: string[]
}

export interface Lesson {
  id: number
  course_id: number
  title: string
  description: string
  content: string
  duration: number
  order: number
  type: 'video' | 'text' | 'quiz'
  resources?: {
    video_url?: string
    attachments?: string[]
  }
}

export interface Chapter {
  id: number
  course_id: number
  title: string
  description: string
  order: number
  lessons: Lesson[]
}

export interface CourseDetail extends Course {
  chapters: Chapter[]
  prerequisites?: Course[]
  next_courses?: Course[]
}

export interface ProgressData {
  overall_progress: number
  completed_courses: number
  learning_hours: number
}

export interface SkillAnalysis {
  skills: {
    web_security: number
    system_security: number
    cryptography: number
    penetration_testing: number
    secure_development: number
  }
}

export interface LearningPath {
  id: number
  title: string
  description: string
  difficulty: string
  duration: string
  courses: Course[]
  progress?: number
}

// 用户相关接口
export const userApi = {
  login: (data: any) => request.post('/api/auth/login', data),
  register: (data: any) => request.post('/api/auth/register', data),
  getUserInfo: () => request.get('/api/user/info')
}

// 课程相关接口
export const courseApi = {
  // 基础课程操作
  getCourseList: (params?: { category?: string; difficulty?: string; search?: string }) => 
    request.get<Course[]>('/api/courses', { params }),
  getCourseDetail: (id: number) => request.get<CourseDetail>(`/api/courses/${id}`),
  updateProgress: (id: number, data: { lesson_id: number; progress: number }) => 
    request.post(`/api/courses/${id}/progress`, data),
  
  // 学习进度
  getProgress: () => request.get<ProgressData>('/api/user/progress'),
  
  // 技能分析
  getSkillAnalysis: () => request.get<SkillAnalysis>('/api/user/skills'),
  
  // 推荐课程
  getRecommendedCourses: () => request.get<Course[]>('/api/courses/recommended'),
  
  // 学习路径
  getLearningPaths: () => request.get<LearningPath[]>('/api/learning-paths'),
  getLearningPathDetail: (id: number) => request.get<LearningPath>(`/api/learning-paths/${id}`),
  
  // 课程章节和课时
  getChapters: (courseId: number) => request.get<Chapter[]>(`/api/courses/${courseId}/chapters`),
  getLesson: (courseId: number, lessonId: number) => 
    request.get<Lesson>(`/api/courses/${courseId}/lessons/${lessonId}`),
  
  // 课时导航
  getLessonNavigation: (lessonId: number) => 
    request.get<LessonNavigation>(`/api/lessons/${lessonId}/navigation`),
}

// 靶场相关接口
export const labApi = {
  getLabList: () => request.get('/api/labs'),
  getLabDetail: (id: number) => request.get(`/api/labs/${id}`),
  startLab: (id: number) => request.post(`/api/labs/${id}/start`),
  stopLab: (id: number) => request.post(`/api/labs/${id}/stop`)
}

// 分析相关接口
export const analysisApi = {
  getAnalysisData: () => request.get('/api/analysis'),
  getSkillRadar: () => request.get('/api/analysis/skill-radar'),
  getProgressTrend: () => request.get('/api/analysis/progress-trend')
}

// 笔记相关接口
export interface Note {
  id: number
  lesson_id: number
  content: string
  created_at: string
  updated_at: string
}

export interface NoteHistory {
  id: number
  note_id: number
  content: string
  created_at: string
}

// 笔记相关接口
export const noteApi = {
  // 获取笔记
  getNote: (lessonId: number) => 
    request.get<Note>(`/api/notes/${lessonId}`),
  
  // 创建笔记
  createNote: (data: { lesson_id: number; content: string }) => 
    request.post<Note>('/api/notes', data),
  
  // 更新笔记
  updateNote: (noteId: number, data: { content: string }) => 
    request.put<Note>(`/api/notes/${noteId}`, data),
  
  // 删除笔记
  deleteNote: (noteId: number) => 
    request.delete(`/api/notes/${noteId}`),
  
  // 获取笔记历史
  getNoteHistory: (noteId: number) => 
    request.get<NoteHistory[]>(`/api/notes/${noteId}/history`)
}

// 测验相关接口
export interface QuizQuestion {
  id: number
  lesson_id: number
  title: string
  type: 'single_choice' | 'multiple_choice' | 'true_false'
  options: {
    value: string
    label: string
  }[]
  explanation?: string
  score: number
  order_num: number
}

export interface QuizAttempt {
  id: number
  lesson_id: number
  answers: Record<string, any>
  score: number
  passed: boolean
  completed_at: string
  details?: {
    question_id: number
    user_answer: any
    is_correct: boolean
    score: number
  }[]
}

// 测验相关接口
export const quizApi = {
  // 获取测验题目
  getQuestions: (lessonId: number) => 
    request.get<QuizQuestion[]>(`/api/quiz/questions/${lessonId}`),
  
  // 创建测验题目（教师/管理员）
  createQuestion: (data: Omit<QuizQuestion, 'id' | 'order_num'>) => 
    request.post<QuizQuestion>('/api/quiz/questions', data),
  
  // 更新测验题目（教师/管理员）
  updateQuestion: (questionId: number, data: Partial<QuizQuestion>) => 
    request.put<QuizQuestion>(`/api/quiz/questions/${questionId}`, data),
  
  // 删除测验题目（教师/管理员）
  deleteQuestion: (questionId: number) => 
    request.delete(`/api/quiz/questions/${questionId}`),
  
  // 获取答题记录
  getAttempt: (lessonId: number) => 
    request.get<QuizAttempt>(`/api/quiz/attempts/${lessonId}`),
  
  // 提交答题
  submitAttempt: (data: { lesson_id: number; answers: Record<string, any> }) => 
    request.post<QuizAttempt>('/api/quiz/attempts', data)
}

// 课时导航相关接口
export interface LessonNavigation {
  current: Lesson
  previous: Lesson | null
  next: Lesson | null
  total: number
  current_index: number
} 