import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

export const useKnowledgeStore = defineStore('knowledge', () => {
  // 状态
  const nodes = ref<KnowledgeNode[]>([])
  const links = ref<KnowledgeLink[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedNode = ref<KnowledgeNode | null>(null)
  const hoveredNode = ref<KnowledgeNode | null>(null)

  // 过滤器状态
  const selectedDifficulties = ref<string[]>([])
  const selectedTypes = ref<string[]>([])
  const selectedTags = ref<string[]>([])

  // 测试数据
  const testNodes: KnowledgeNode[] = [
    {
      id: '1',
      name: 'Web安全基础',
      category: 'concept',
      difficulty: 'basic',
      value: 10,
      description: 'Web安全的基本概念和原理',
      keyPoints: ['HTTP协议', '同源策略', '认证与授权'],
      resources: [],
      prerequisites: [],
      nextSteps: ['2', '3'],
      tags: ['Web安全', '基础概念']
    },
    {
      id: '2',
      name: 'SQL注入',
      category: 'vulnerability',
      difficulty: 'intermediate',
      value: 8,
      description: 'SQL注入漏洞的原理和防御',
      keyPoints: ['SQL语法', '注入类型', '防御措施'],
      resources: [],
      prerequisites: ['1'],
      nextSteps: ['4'],
      tags: ['SQL注入', '漏洞利用']
    },
    {
      id: '3',
      name: 'XSS攻击',
      category: 'vulnerability',
      difficulty: 'intermediate',
      value: 8,
      description: '跨站脚本攻击的原理和防御',
      keyPoints: ['JavaScript', 'DOM', '输入验证'],
      resources: [],
      prerequisites: ['1'],
      nextSteps: ['4'],
      tags: ['XSS', '漏洞利用']
    },
    {
      id: '4',
      name: 'Web安全工具',
      category: 'tool',
      difficulty: 'intermediate',
      value: 6,
      description: '常用的Web安全测试工具',
      keyPoints: ['漏洞扫描', '抓包分析', '漏洞利用'],
      resources: [],
      prerequisites: ['2', '3'],
      nextSteps: ['5'],
      tags: ['安全工具', '漏洞扫描']
    }
  ]

  const testLinks: KnowledgeLink[] = [
    { source: '1', target: '2', value: 1, type: 'prerequisite' },
    { source: '1', target: '3', value: 1, type: 'prerequisite' },
    { source: '2', target: '4', value: 1, type: 'prerequisite' },
    { source: '3', target: '4', value: 1, type: 'prerequisite' }
  ]

  // 方法
  const fetchGraphData = async () => {
    console.log('Fetching graph data...')
    loading.value = true
    error.value = null
    try {
      // 使用测试数据
      nodes.value = testNodes
      links.value = testLinks
      console.log('Graph data loaded:', { nodes: nodes.value, links: links.value })
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败'
      console.error('Failed to load graph data:', err)
    } finally {
      loading.value = false
    }
  }

  const setSelectedNode = (node: KnowledgeNode | null) => {
    console.log('Selected node:', node)
    selectedNode.value = node
  }

  const setHoveredNode = (node: KnowledgeNode | null) => {
    console.log('Hovered node:', node)
    hoveredNode.value = node
  }

  const setFilters = (filters: {
    difficulties?: string[]
    types?: string[]
    tags?: string[]
  }) => {
    if (filters.difficulties !== undefined) {
      selectedDifficulties.value = filters.difficulties
    }
    if (filters.types !== undefined) {
      selectedTypes.value = filters.types
    }
    if (filters.tags !== undefined) {
      selectedTags.value = filters.tags
    }
    console.log('Filters updated:', {
      difficulties: selectedDifficulties.value,
      types: selectedTypes.value,
      tags: selectedTags.value
    })
  }

  const resetFilters = () => {
    selectedDifficulties.value = []
    selectedTypes.value = []
    selectedTags.value = []
    console.log('Filters reset')
  }

  return {
    nodes,
    links,
    loading,
    error,
    selectedNode,
    hoveredNode,
    selectedDifficulties,
    selectedTypes,
    selectedTags,
    fetchGraphData,
    setSelectedNode,
    setHoveredNode,
    setFilters,
    resetFilters
  }
}) 