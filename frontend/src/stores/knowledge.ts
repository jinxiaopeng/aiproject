import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/api/knowledge'
import type { 
  KnowledgeNode, 
  KnowledgeGraph, 
  AttackType, 
  Vulnerability,
  LearningRecord,
  Feedback,
  Relationship 
} from '@/api/knowledge'

export const useKnowledgeStore = defineStore('knowledge', () => {
  // 状态
  const nodes = ref<KnowledgeNode[]>([])
  const attackTypes = ref<AttackType[]>([])
  const vulnerabilities = ref<Vulnerability[]>([])
  const learningRecords = ref<LearningRecord[]>([])
  const relationships = ref<Relationship[]>([])
  const currentNode = ref<KnowledgeNode | null>(null)
  const graph = ref<KnowledgeGraph | null>(null)
  const loading = ref(false)
  const error = ref('')

  // 获取所有实体数据
  const fetchAllData = async () => {
    try {
      loading.value = true
      const [nodesData, attacksData, vulnsData, recordsData, relsData] = await Promise.all([
        api.getKnowledgeNodes(),
        api.getAttackTypes(),
        api.getVulnerabilities(),
        api.getLearningRecords(),
        api.getRelationships()
      ])
      
      nodes.value = nodesData
      attackTypes.value = attacksData
      vulnerabilities.value = vulnsData
      learningRecords.value = recordsData
      relationships.value = relsData
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取知识图谱数据
  const getGraph = async () => {
    try {
      loading.value = true
      graph.value = await api.getKnowledgeGraph()
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新学习记录
  const updateLearningProgress = async (id: number, progress: number) => {
    try {
      loading.value = true
      const record = await api.updateLearningRecord(id, { progress })
      const index = learningRecords.value.findIndex(r => r.id === id)
      if (index !== -1) {
        learningRecords.value[index] = record
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 提交反馈
  const submitFeedback = async (feedback: Omit<Feedback, 'id' | 'created_at'>) => {
    try {
      loading.value = true
      await api.createFeedback(feedback)
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建关系
  const createRelationship = async (relationship: Omit<Relationship, 'id'>) => {
    try {
      loading.value = true
      const newRel = await api.createRelationship(relationship)
      relationships.value.push(newRel)
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    nodes,
    attackTypes,
    vulnerabilities,
    learningRecords,
    relationships,
    currentNode,
    graph,
    loading,
    error,

    // 方法
    fetchAllData,
    getGraph,
    updateLearningProgress,
    submitFeedback,
    createRelationship
  }
}) 