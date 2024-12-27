import request from '@/utils/request'

export interface ResourceItem {
  name: string
  description: string
  url: string
}

export interface ResourceGroup {
  type: string
  items: ResourceItem[]
}

export interface KnowledgeNode {
  id: string
  name: string
  category: string
  difficulty: string
  value: number
  description: string
  keyPoints: string[]
  resources: ResourceGroup[]
  prerequisites: string[]
  nextSteps: string[]
  tags: string[]
  createdAt?: string
  updatedAt?: string
  progress?: number
  isRecommended?: boolean
}

export interface KnowledgeLink {
  source: string
  target: string
  value: number
  type: string
}

export interface KnowledgeGraphData {
  nodes: KnowledgeNode[]
  links: KnowledgeLink[]
}

export interface LearningPathResponse {
  path: string[]
  difficulty: number
  estimatedTime: number
  prerequisites: string[]
}

export interface ProgressResponse {
  progress: number
}

export interface ProgressSyncResponse {
  [key: string]: number
}

export function getKnowledgeGraph(): Promise<KnowledgeGraphData> {
  return request({
    url: '/knowledge/graph',
    method: 'get'
  }).then(response => response.data)
}

export function updateNodeProgress(nodeId: string, progress: number): Promise<{ status: string }> {
  return request({
    url: `/knowledge/node/${nodeId}/progress`,
    method: 'post',
    data: { progress }
  }).then(response => response.data)
}

export function getNodeProgress(nodeId: string): Promise<ProgressResponse> {
  return request({
    url: `/knowledge/node/${nodeId}/progress`,
    method: 'get'
  }).then(response => response.data)
}

export function syncLearningProgress(): Promise<ProgressSyncResponse> {
  return request({
    url: '/knowledge/progress/sync',
    method: 'get'
  }).then(response => response.data)
}

export function getLearningPath(nodeId: string): Promise<LearningPathResponse> {
  return request({
    url: `/knowledge/path/${nodeId}`,
    method: 'get'
  }).then(response => response.data)
}

export function markNodeComplete(nodeId: string): Promise<{ status: string }> {
  return request({
    url: `/knowledge/node/${nodeId}/complete`,
    method: 'post'
  }).then(response => response.data)
} 