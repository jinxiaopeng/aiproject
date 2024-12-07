import request from '@/utils/request'

export interface SearchResult {
  id: number
  category: 'courses' | 'labs' | 'knowledge'
  title: string
  description: string
  path: string
}

export interface SearchParams {
  keyword: string
  page?: number
  pageSize?: number
  categories?: string[]
}

export function search(params: SearchParams) {
  return request({
    url: '/api/search',
    method: 'get',
    params
  })
}

export function getSearchSuggestions() {
  return request({
    url: '/api/search/suggestions',
    method: 'get'
  })
} 