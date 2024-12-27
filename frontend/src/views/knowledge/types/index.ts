// 资源项类型
export interface ResourceItem {
  title: string
  url: string
  description?: string
}

// 资源组类型
export interface ResourceGroup {
  title: string
  items: ResourceItem[]
}

// 知识节点类型
export interface KnowledgeNode {
  id: string
  name: string
  category: string
  difficulty: string
  value: number
  learningStatus?: 'learning' | 'completed' | 'recommended'
  description: string
  keyPoints?: string[]
  resources?: {
    title: string
    items: {
      title: string
      url: string
      description?: string
    }[]
  }[]
  prerequisites?: string[]
  nextSteps?: string[]
  related?: string[]
  tags?: string[]
}

// 知识连接类型
export interface KnowledgeLink {
  source: string
  target: string
  value: number
  type: 'prerequisite' | 'next' | 'related'
}

// 分类类型
export interface Category {
  key: string
  label: string
  color: string
}

// 难度等级类型
export interface Difficulty {
  key: string
  label: string
  color: string
}

// 筛选状态类型
export interface FilterState {
  search: string
  categories: string[]
  difficulties: string[]
  learningStatus: 'all' | 'learning' | 'completed' | 'recommended'
  relations?: {
    nodeId: string
    types: string[]
  }
}

// 布局模式类型
export type LayoutMode = 'force' | 'tree' | 'radial'

// 图谱状态类型
export interface GraphState {
  zoom: number
  center: { x: number; y: number }
  layout: LayoutMode
}

// 节点事件类型
export interface NodeEvent {
  node: KnowledgeNode
  event: MouseEvent
}

// 图谱属性类型
export interface GraphProps {
  layoutMode: LayoutMode
  onNodeClick?: (event: NodeEvent) => void
  onNodeHover?: (event: NodeEvent) => void
}

// 学习进度类型
export interface LearningProgress {
  nodeId: string
  progress: number
  lastUpdated: string
}

// 学习路径类型
export interface LearningPath {
  nodes: string[]
  difficulty: number
  estimatedTime: number
  prerequisites: string[]
}

// 保存的筛选类型
export interface SavedFilter {
  id: number
  name: string
  filters: FilterState
} 