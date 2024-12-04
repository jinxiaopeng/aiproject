import request from '../utils/request'
import type { AxiosResponse } from 'axios'

export interface Note {
  id: number
  user_id: number
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

export interface CreateNoteData {
  lesson_id: number
  content: string
}

export interface UpdateNoteData {
  content: string
}

const noteApi = {
  // 获取笔记
  getNote(lessonId: number): Promise<AxiosResponse<Note>> {
    return request.get(`/api/notes/${lessonId}`)
  },

  // 创建笔记
  createNote(data: CreateNoteData): Promise<AxiosResponse<Note>> {
    return request.post('/api/notes', data)
  },

  // 更新笔记
  updateNote(noteId: number, data: UpdateNoteData): Promise<AxiosResponse<Note>> {
    return request.put(`/api/notes/${noteId}`, data)
  },

  // 删除笔记
  deleteNote(noteId: number): Promise<AxiosResponse<void>> {
    return request.delete(`/api/notes/${noteId}`)
  },

  // 获取笔记历史记录
  getNoteHistory(noteId: number): Promise<AxiosResponse<NoteHistory[]>> {
    return request.get(`/api/notes/${noteId}/history`)
  }
}

export default noteApi 