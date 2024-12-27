<template>
  <div class="node-detail">
    <template v-if="selectedNode">
      <!-- 基本信息 -->
      <div class="detail-header">
        <div class="node-badges">
          <el-tag
            :style="{ backgroundColor: getCategoryColor(selectedNode.category) }"
            effect="dark"
          >
            {{ getCategoryLabel(selectedNode.category) }}
          </el-tag>
          <el-tag
            :style="{ backgroundColor: getDifficultyColor(selectedNode.difficulty) }"
            effect="dark"
          >
            {{ getDifficultyLabel(selectedNode.difficulty) }}
          </el-tag>
        </div>
        <h3 class="node-title">{{ selectedNode.name }}</h3>
        <p class="node-description">{{ selectedNode.description }}</p>
      </div>

      <!-- 关键知识点 -->
      <div class="detail-section">
        <h4>关键知识点</h4>
        <ul class="key-points">
          <li v-for="point in selectedNode.keyPoints" :key="point">
            {{ point }}
          </li>
        </ul>
      </div>

      <!-- 学习资源 -->
      <div v-if="selectedNode.resources.length" class="detail-section">
        <h4>学习资源</h4>
        <div v-for="group in selectedNode.resources" :key="group.type" class="resource-group">
          <h5>{{ group.type }}</h5>
          <el-collapse>
            <el-collapse-item
              v-for="item in group.items"
              :key="item.name"
              :title="item.name"
            >
              <p>{{ item.description }}</p>
              <el-link
                :href="item.url"
                target="_blank"
                type="primary"
                :underline="false"
              >
                查看资源
                <el-icon class="el-icon--right"><ArrowRight /></el-icon>
              </el-link>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>

      <!-- 相关知识点 -->
      <div class="detail-section">
        <template v-if="prerequisites.length">
          <h4>前置知识</h4>
          <div class="related-nodes">
            <el-tag
              v-for="node in prerequisites"
              :key="node.id"
              :style="{ backgroundColor: getCategoryColor(node.category) }"
              effect="dark"
              @click="handleNodeClick(node)"
            >
              {{ node.name }}
            </el-tag>
          </div>
        </template>

        <template v-if="nextSteps.length">
          <h4>进阶知识</h4>
          <div class="related-nodes">
            <el-tag
              v-for="node in nextSteps"
              :key="node.id"
              :style="{ backgroundColor: getCategoryColor(node.category) }"
              effect="dark"
              @click="handleNodeClick(node)"
            >
              {{ node.name }}
            </el-tag>
          </div>
        </template>
      </div>

      <!-- 标签 -->
      <div class="detail-section">
        <h4>相关标签</h4>
        <div class="tags">
          <el-tag
            v-for="tag in selectedNode.tags"
            :key="tag"
            effect="plain"
            class="tag"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </template>

    <div v-else class="empty-state">
      <el-empty description="请选择一个知识点查看详情" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useKnowledgeStore } from '../store'
import { categories, difficulties } from '../mock/data'
import { ArrowRight } from '@element-plus/icons-vue'
import type { KnowledgeNode } from '../types'

const store = useKnowledgeStore()
const { selectedNode, nodes } = storeToRefs(store)

// 计算属性
const prerequisites = computed(() => {
  if (!selectedNode.value) return []
  return selectedNode.value.prerequisites
    .map(id => nodes.value.find(node => node.id === id))
    .filter((node): node is KnowledgeNode => node !== undefined)
})

const nextSteps = computed(() => {
  if (!selectedNode.value) return []
  return selectedNode.value.nextSteps
    .map(id => nodes.value.find(node => node.id === id))
    .filter((node): node is KnowledgeNode => node !== undefined)
})

// 工具函数
const getCategoryColor = (category: string) => {
  return categories.find(c => c.key === category)?.color || '#909399'
}

const getCategoryLabel = (category: string) => {
  return categories.find(c => c.key === category)?.label || category
}

const getDifficultyColor = (difficulty: string) => {
  return difficulties.find(d => d.key === difficulty)?.color || '#909399'
}

const getDifficultyLabel = (difficulty: string) => {
  return difficulties.find(d => d.key === difficulty)?.label || difficulty
}

// 事件处理
const handleNodeClick = (node: KnowledgeNode) => {
  store.setSelectedNode(node)
}
</script>

<style scoped>
.node-detail {
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
}

.detail-header {
  margin-bottom: 24px;
}

.node-badges {
  margin-bottom: 12px;
  display: flex;
  gap: 8px;
}

.node-title {
  margin: 0 0 12px;
  font-size: 20px;
  color: #e5eaf3;
}

.node-description {
  margin: 0;
  color: #a3adc8;
  line-height: 1.6;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  margin: 0 0 12px;
  font-size: 16px;
  color: #e5eaf3;
}

.detail-section h5 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #a3adc8;
}

.key-points {
  margin: 0;
  padding-left: 20px;
  color: #a3adc8;
}

.key-points li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.resource-group {
  margin-bottom: 16px;
}

.related-nodes {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a3adc8;
}

:deep(.el-tag) {
  cursor: pointer;
  transition: transform 0.2s;
}

:deep(.el-tag:hover) {
  transform: scale(1.05);
}

:deep(.el-collapse) {
  border: none;
  background: transparent;
}

:deep(.el-collapse-item__header) {
  background: transparent;
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
  color: #e5eaf3;
}

:deep(.el-collapse-item__content) {
  background: transparent;
  color: #a3adc8;
  padding: 16px;
}

:deep(.el-link) {
  margin-top: 8px;
}

/* 滚动条样式 */
.node-detail::-webkit-scrollbar {
  width: 6px;
}

.node-detail::-webkit-scrollbar-track {
  background: transparent;
}

.node-detail::-webkit-scrollbar-thumb {
  background: rgba(65, 184, 131, 0.2);
  border-radius: 3px;
}

.node-detail::-webkit-scrollbar-thumb:hover {
  background: rgba(65, 184, 131, 0.4);
}
</style> 