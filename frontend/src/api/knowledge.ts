import request from '@/utils/request'

export interface ResourceItem {
  name: string
  description: string
  title: string
  url: string
}

export interface ResourceGroup {
  type: string
  items: ResourceItem[]
}

export interface KnowledgeNode {
  id: string | number
  name: string
  category: string
  difficulty: string
  value: number
  description: string
  keyPoints: string[]
  resources: ResourceGroup[]
  prerequisites: string[]
  nextSteps: string[]
}

export interface KnowledgeLink {
  source: string | number
  target: string | number
  type: string
  value: number
}

export interface KnowledgeGraphData {
  nodes: KnowledgeNode[]
  links: KnowledgeLink[]
}

export function getKnowledgeGraph(): Promise<KnowledgeGraphData> {
  return request({
    url: '/api/knowledge/graph',
    method: 'get',
    timeout: 5000 // 设置5秒超时
  })
}

export function markNodeComplete(nodeId: string): Promise<{ status: string }> {
  return request({
    url: `/knowledge/node/${nodeId}/complete`,
    method: 'post'
  }).then(response => response.data)
}

export function getLearningPath(nodeId: string): Promise<LearningPath> {
  return request({
    url: `/knowledge/path/${nodeId}`,
    method: 'get'
  }).then(response => response.data)
} 