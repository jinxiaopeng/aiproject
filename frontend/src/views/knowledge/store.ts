// 知识图谱状态管理
import { defineStore } from 'pinia'
import type { KnowledgeNode } from '@/api/knowledge'

export const useKnowledgeGraphStore = defineStore('knowledgeGraph', {
  state: () => ({
    selectedNode: null as KnowledgeNode | null,
    nodes: [] as KnowledgeNode[],
    categories: [] as string[],
    difficulties: [] as string[],
    filters: {
      categories: [] as string[],
      difficulties: [] as string[]
    }
  }),
  
  actions: {
    setSelectedNode(node: KnowledgeNode | null) {
      this.selectedNode = node
    },

    setNodes(nodes: KnowledgeNode[]) {
      this.nodes = nodes
    },

    setFilters(filters: { categories: string[], difficulties: string[] }) {
      this.filters = filters
    },

    resetFilters() {
      this.filters = {
        categories: [],
        difficulties: []
      }
    }
  }
}) 