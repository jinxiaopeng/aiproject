import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { KnowledgeNode, KnowledgeLink, FilterState, GraphState, LayoutMode } from '../types'
import { mockNodes, mockLinks } from '../mock/data'

export const useKnowledgeStore = defineStore('knowledge', () => {
  // 状态
  const nodes = ref<KnowledgeNode[]>([])
  const links = ref<KnowledgeLink[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedNode = ref<KnowledgeNode | null>(null)
  const hoveredNode = ref<KnowledgeNode | null>(null)
  const learningProgress = ref<Map<string, number>>(new Map())
  const recommendedPath = ref<string[]>([])

  // 过滤器状态
  const filters = ref<FilterState>({
    categories: [],
    difficulties: [],
    search: ''
  })

  // 图谱状态
  const graphState = ref<GraphState>({
    zoom: 1,
    center: { x: 0, y: 0 },
    layout: 'force'
  })

  // 计算属性
  const filteredNodes = computed(() => {
    return nodes.value.filter(node => {
      const categoryMatch = filters.value.categories.length === 0 || 
        filters.value.categories.includes(node.category)
      const difficultyMatch = filters.value.difficulties.length === 0 || 
        filters.value.difficulties.includes(node.difficulty)
      const searchMatch = !filters.value.search || 
        node.name.toLowerCase().includes(filters.value.search.toLowerCase()) ||
        node.description.toLowerCase().includes(filters.value.search.toLowerCase())
      return categoryMatch && difficultyMatch && searchMatch
    })
  })

  const filteredLinks = computed(() => {
    const filteredNodeIds = new Set(filteredNodes.value.map(node => node.id))
    return links.value.filter(link => 
      filteredNodeIds.has(link.source) && filteredNodeIds.has(link.target)
    )
  })

  const relatedNodes = computed(() => {
    if (!selectedNode.value) return []
    const relatedLinks = links.value.filter(link => 
      link.source === selectedNode.value?.id || link.target === selectedNode.value?.id
    )
    const relatedNodeIds = new Set(relatedLinks.flatMap(link => [link.source, link.target]))
    return nodes.value.filter(node => relatedNodeIds.has(node.id))
  })

  // 方法
  const fetchGraphData = async () => {
    loading.value = true
    error.value = null
    try {
      // 直接使用模拟数据
      nodes.value = mockNodes
      links.value = mockLinks
      
      // 初始化学习进度（模拟数据）
      mockNodes.forEach(node => {
        learningProgress.value.set(String(node.id), Math.random())
      })
      
      // 初始化推荐路径（模拟数据）
      const randomNodes = mockNodes
        .filter(node => node.id !== 1) // 排除根节点
        .sort(() => Math.random() - 0.5)
        .slice(0, 3)
      recommendedPath.value = randomNodes.map(node => String(node.id))
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败'
      console.error('Failed to load graph data:', err)
    } finally {
      loading.value = false
    }
  }

  const updateProgress = (nodeId: string, progress: number) => {
    learningProgress.value.set(nodeId, progress)
  }

  const getProgress = (nodeId: string) => {
    return learningProgress.value.get(nodeId) || 0
  }

  const generateLearningPath = (targetNodeId: string) => {
    // 生成模拟的学习路径
    const availableNodes = mockNodes
      .filter(node => node.id !== Number(targetNodeId))
      .sort(() => Math.random() - 0.5)
      .slice(0, 3)
    recommendedPath.value = availableNodes.map(node => String(node.id))
  }

  const setSelectedNode = (node: KnowledgeNode | null) => {
    selectedNode.value = node
    if (node) {
      generateLearningPath(String(node.id))
    }
  }

  const setHoveredNode = (node: KnowledgeNode | null) => {
    hoveredNode.value = node
  }

  const setFilters = (newFilters: Partial<FilterState>) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  const resetFilters = () => {
    filters.value = {
      categories: [],
      difficulties: [],
      search: ''
    }
  }

  const setLayoutMode = (mode: LayoutMode) => {
    graphState.value.layout = mode
  }

  const setZoom = (zoom: number) => {
    graphState.value.zoom = zoom
  }

  const setCenter = (x: number, y: number) => {
    graphState.value.center = { x, y }
  }

  const resetGraphState = () => {
    graphState.value = {
      zoom: 1,
      center: { x: 0, y: 0 },
      layout: 'force'
    }
  }

  return {
    // 状态
    nodes,
    links,
    loading,
    error,
    selectedNode,
    hoveredNode,
    learningProgress,
    recommendedPath,
    filters,
    graphState,

    // 计算属性
    filteredNodes,
    filteredLinks,
    relatedNodes,

    // 方法
    fetchGraphData,
    updateProgress,
    getProgress,
    generateLearningPath,
    setSelectedNode,
    setHoveredNode,
    setFilters,
    resetFilters,
    setLayoutMode,
    setZoom,
    setCenter,
    resetGraphState
  }
}) 