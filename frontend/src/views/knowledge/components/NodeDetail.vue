<template>
  <div class="node-detail" v-if="selectedNode">
    <el-card class="detail-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">{{ selectedNode.name }}</span>
          <el-tag :type="getDifficultyType(selectedNode.difficulty)" size="small">
            {{ selectedNode.difficulty }}
          </el-tag>
        </div>
      </template>
      
      <div class="content">
        <div class="description">
          {{ selectedNode.description }}
        </div>

        <div class="section">
          <h4>关键知识点</h4>
          <el-tag
            v-for="point in selectedNode.keyPoints"
            :key="point"
            class="key-point"
            effect="dark"
          >
            {{ point }}
          </el-tag>
        </div>

        <div class="section" v-if="selectedNode.resources && selectedNode.resources.length > 0">
          <h4>学习资源</h4>
          <div v-for="group in selectedNode.resources" :key="group.type" class="resource-group">
            <h5>{{ group.type }}</h5>
            <el-collapse>
              <el-collapse-item v-for="item in group.items" :key="item.name">
                <template #title>
                  <span class="resource-title">{{ item.title }}</span>
                </template>
                <div class="resource-content">
                  <p>{{ item.description }}</p>
                  <el-button 
                    type="primary" 
                    link 
                    :href="item.url" 
                    target="_blank"
                  >
                    查看详情
                  </el-button>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </div>
    </el-card>
    
    <el-card class="path-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>学习路径</span>
        </div>
      </template>
      
      <div class="path-content">
        <div class="prerequisites" v-if="selectedNode.prerequisites.length > 0">
          <h4>前置知识</h4>
          <div class="path-tags">
            <el-tag
              v-for="id in selectedNode.prerequisites"
              :key="id"
              type="info"
              effect="dark"
              class="path-tag"
            >
              {{ getNodeName(id) }}
            </el-tag>
          </div>
        </div>

        <div class="next-steps" v-if="selectedNode.nextSteps.length > 0">
          <h4>后续学习</h4>
          <div class="path-tags">
            <el-tag
              v-for="id in selectedNode.nextSteps"
              :key="id"
              type="success"
              effect="dark"
              class="path-tag"
            >
              {{ getNodeName(id) }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-card>
  </div>
  <el-empty v-else description="选择知识点查看详情" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useKnowledgeGraphStore } from '../store'
import type { KnowledgeNode } from '@/api/knowledge'

const store = useKnowledgeGraphStore()
const selectedNode = computed(() => store.selectedNode)

const getDifficultyType = (difficulty: string) => {
  const types = {
    'basic': 'success',
    'intermediate': 'warning',
    'advanced': 'danger',
    'expert': 'info'
  }
  return types[difficulty] || 'info'
}

const getNodeName = (id: string) => {
  const node = store.nodes.find(n => n.id === id)
  return node ? node.name : id
}
</script>

<style scoped>
.node-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.detail-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title {
  font-size: 16px;
  font-weight: 500;
  color: #e5eaf3;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.description {
  color: #a3a6ad;
  line-height: 1.6;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

h4 {
  margin: 0;
  color: #e5eaf3;
  font-size: 14px;
  font-weight: 500;
}

h5 {
  margin: 0 0 8px;
  color: #a3a6ad;
  font-size: 13px;
  font-weight: 500;
}

.key-point {
  margin: 4px;
}

.resource-group {
  margin-bottom: 16px;
}

.resource-title {
  color: #e5eaf3;
  font-weight: 500;
}

.resource-content {
  padding: 12px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.resource-content p {
  margin: 0 0 12px;
  color: #a3a6ad;
}

.path-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.path-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.path-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.path-tag:hover {
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
  color: #a3a6ad;
}

:deep(.el-tag) {
  background: rgba(65, 184, 131, 0.1);
  border: 1px solid rgba(65, 184, 131, 0.2);
}

:deep(.el-tag--dark) {
  background: rgba(65, 184, 131, 0.2);
  border: none;
}

:deep(.el-button--primary) {
  background: transparent;
  border: 1px solid rgba(65, 184, 131, 0.3);
  color: #41b883;
}

:deep(.el-button--primary:hover) {
  background: rgba(65, 184, 131, 0.1);
  border-color: rgba(65, 184, 131, 0.5);
}
</style> 