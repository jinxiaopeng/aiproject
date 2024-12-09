import { defineStore } from 'pinia'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

export const useKnowledgeGraphStore = defineStore('knowledgeGraph', {
  state: () => ({
    nodes: [] as KnowledgeNode[],
    links: [] as KnowledgeLink[],
    selectedNode: null as KnowledgeNode | null,
    hoveredNode: null as KnowledgeNode | null,
    filters: {
      category: [] as string[],
      difficulty: [] as string[],
      search: '' as string
    },
    layout: {
      mode: 'force' as 'force' | 'circular',
      zoom: 1,
      center: { x: 0, y: 0 }
    }
  }),

  getters: {
    getNodeById: (state) => (id: string | number) => {
      return state.nodes.find(node => node.id === id)
    },
    
    getRelatedNodes: (state) => (nodeId: string | number) => {
      const relatedLinks = state.links.filter(link => 
        link.source === nodeId || link.target === nodeId
      )
      const relatedNodeIds = new Set(relatedLinks.flatMap(link => [link.source, link.target]))
      return state.nodes.filter(node => relatedNodeIds.has(node.id))
    },
    
    filteredNodes: (state) => {
      return state.nodes.filter(node => {
        const categoryMatch = state.filters.category.length === 0 || 
          state.filters.category.includes(node.category)
        const difficultyMatch = state.filters.difficulty.length === 0 || 
          state.filters.difficulty.includes(node.difficulty)
        const searchMatch = !state.filters.search || 
          node.name.toLowerCase().includes(state.filters.search.toLowerCase()) ||
          node.description.toLowerCase().includes(state.filters.search.toLowerCase())
        return categoryMatch && difficultyMatch && searchMatch
      })
    },
    
    filteredEdges: (state) => {
      const filteredNodeIds = new Set(state.nodes
        .filter(node => {
          const categoryMatch = state.filters.category.length === 0 || 
            state.filters.category.includes(node.category)
          const difficultyMatch = state.filters.difficulty.length === 0 || 
            state.filters.difficulty.includes(node.difficulty)
          return categoryMatch && difficultyMatch
        })
        .map(node => node.id)
      )
      
      return state.links.filter(link => 
        filteredNodeIds.has(link.source) && filteredNodeIds.has(link.target)
      )
    },
    
    categories: (state) => {
      return Array.from(new Set(state.nodes.map(node => node.category)))
    },
    
    difficulties: (state) => {
      return Array.from(new Set(state.nodes.map(node => node.difficulty)))
    }
  },

  actions: {
    setNodes(nodes: KnowledgeNode[]) {
      this.nodes = nodes
    },
    
    setLinks(links: KnowledgeLink[]) {
      this.links = links
    },
    
    setSelectedNode(node: KnowledgeNode | null) {
      this.selectedNode = node
    },
    
    setHoveredNode(node: KnowledgeNode | null) {
      this.hoveredNode = node
    },
    
    setFilters(filters: { category?: string[], difficulty?: string[], search?: string }) {
      if (filters.category !== undefined) {
        this.filters.category = filters.category
      }
      if (filters.difficulty !== undefined) {
        this.filters.difficulty = filters.difficulty
      }
      if (filters.search !== undefined) {
        this.filters.search = filters.search
      }
    },
    
    clearFilters() {
      this.filters.category = []
      this.filters.difficulty = []
      this.filters.search = ''
    },
    
    setLayoutMode(mode: 'force' | 'circular') {
      this.layout.mode = mode
    },
    
    setZoom(zoom: number) {
      this.layout.zoom = zoom
    },
    
    setCenter(x: number, y: number) {
      this.layout.center = { x, y }
    },
    
    resetLayout() {
      this.layout.mode = 'force'
      this.layout.zoom = 1
      this.layout.center = { x: 0, y: 0 }
    }
  }
}) 