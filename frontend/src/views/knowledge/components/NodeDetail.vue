<template>
  <div class="node-detail">
    <template v-if="selectedNode">
      <el-scrollbar>
        <el-card class="detail-card" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>{{ selectedNode.name }}</h3>
              <div class="header-tags">
                <el-tag :type="getCategoryType(selectedNode.category)" effect="dark">
                  {{ getCategoryLabel(selectedNode.category) }}
                </el-tag>
                <el-tag :type="getDifficultyType(selectedNode.difficulty)" effect="dark">
                  {{ getDifficultyLabel(selectedNode.difficulty) }}
                </el-tag>
              </div>
            </div>
          </template>

          <!-- 描述信息 -->
          <div class="detail-section">
            <h4>描述</h4>
            <p class="description">{{ selectedNode.description }}</p>
          </div>

          <!-- 关键知识点 -->
          <div class="detail-section">
            <h4>关键知识点</h4>
            <div class="key-points">
              <el-tag
                v-for="point in selectedNode.keyPoints"
                :key="point"
                class="key-point-tag"
                effect="plain"
              >
                {{ point }}
              </el-tag>
            </div>
          </div>

          <!-- 学习资源 -->
          <div class="detail-section">
            <h4>学习资源</h4>
            <div class="resources">
              <div v-for="group in selectedNode.resources" :key="group.type" class="resource-group">
                <h5>
                  <el-icon>
                    <component :is="getResourceTypeIcon(group.type)" />
                  </el-icon>
                  {{ getResourceTypeLabel(group.type) }}
                </h5>
                <el-collapse>
                  <el-collapse-item
                    v-for="item in group.items"
                    :key="item.name"
                    :title="item.name"
                  >
                    <p class="resource-description">{{ item.description }}</p>
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
          </div>

          <!-- 相关知识点 -->
          <div class="detail-section">
            <h4>相关知识点</h4>
            <div class="related-nodes">
              <!-- 前置知识 -->
              <div v-if="prerequisites.length > 0" class="related-group">
                <h5>
                  <el-icon><Back /></el-icon>
                  前置知识
                </h5>
                <div class="related-list">
                  <el-button
                    v-for="node in prerequisites"
                    :key="node.id"
                    :type="getNodeButtonType(node)"
                    size="small"
                    @click="handleNodeClick(node)"
                  >
                    {{ node.name }}
                  </el-button>
                </div>
              </div>

              <!-- 后续学习 -->
              <div v-if="nextSteps.length > 0" class="related-group">
                <h5>
                  <el-icon><Right /></el-icon>
                  后续学习
                </h5>
                <div class="related-list">
                  <el-button
                    v-for="node in nextSteps"
                    :key="node.id"
                    :type="getNodeButtonType(node)"
                    size="small"
                    @click="handleNodeClick(node)"
                  >
                    {{ node.name }}
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 时间信息 -->
          <div class="detail-section time-info">
            <el-descriptions :column="1" size="small" border>
              <el-descriptions-item label="创建时间">
                {{ formatDate(selectedNode.createdAt) }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ formatDate(selectedNode.updatedAt) }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-scrollbar>
    </template>

    <div v-else class="empty-state">
      <el-empty description="选择一个知识点查看详情">
        <template #image>
          <el-icon :size="48"><Select /></el-icon>
        </template>
      </el-empty>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { useKnowledgeGraphStore } from '../store/index'
import { ElMessage } from 'element-plus'
import {
  ArrowRight,
  Back,
  Right,
  Document,
  VideoPlay,
  Tools,
  Operation,
  Select
} from '@element-plus/icons-vue'
import type { KnowledgeNode } from '@/api/knowledge'

const store = useKnowledgeGraphStore()

const selectedNode = computed(() => store.selectedNode)

// 获取前置知识节点
const prerequisites = computed(() => {
  if (!selectedNode.value) return []
  return selectedNode.value.prerequisites
    .map(id => store.getNodeById(id))
    .filter((node): node is KnowledgeNode => node !== undefined)
})

// 获取后续学习节点
const nextSteps = computed(() => {
  if (!selectedNode.value) return []
  return selectedNode.value.nextSteps
    .map(id => store.getNodeById(id))
    .filter((node): node is KnowledgeNode => node !== undefined)
})

// 格式化日期
const formatDate = (date: string | Date | undefined) => {
  if (!date) return '暂无'
  try {
    return format(new Date(date), 'yyyy-MM-dd HH:mm')
  } catch {
    return '日期格式错误'
  }
}

// 获取分类样式
const getCategoryType = (category: string) => {
  const types: Record<string, string> = {
    'vulnerability': 'danger',
    'concept': 'primary',
    'tool': 'warning',
    'technique': 'success',
    'default': 'info'
  }
  return types[category] || types.default
}

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    'vulnerability': '漏洞',
    'concept': '概念',
    'tool': '工具',
    'technique': '技术',
    'default': '其他'
  }
  return labels[category] || category
}

// 获取难度样式
const getDifficultyType = (difficulty: string) => {
  const types: Record<string, string> = {
    'basic': 'success',
    'intermediate': 'warning',
    'advanced': 'danger',
    'expert': 'danger'
  }
  return types[difficulty] || 'info'
}

const getDifficultyLabel = (difficulty: string) => {
  const labels: Record<string, string> = {
    'basic': '入门',
    'intermediate': '进阶',
    'advanced': '高级',
    'expert': '专家'
  }
  return labels[difficulty] || difficulty
}

// 获取资源类型标签
const getResourceTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'article': '文章',
    'video': '视频',
    'tool': '工具',
    'practice': '实践',
    'default': '其他'
  }
  return labels[type] || type
}

// 获取资源类型图标
const getResourceTypeIcon = (type: string) => {
  const icons: Record<string, any> = {
    'article': Document,
    'video': VideoPlay,
    'tool': Tools,
    'practice': Operation
  }
  return icons[type] || Document
}

// 获取节点按钮类型
const getNodeButtonType = (node: KnowledgeNode) => {
  return node.id === selectedNode.value?.id ? 'primary' : ''
}

// 处理节点点击
const handleNodeClick = (node: KnowledgeNode) => {
  store.setSelectedNode(node)
  ElMessage.success(`已切换到 ${node.name}`)
}
</script>

<style scoped>
.node-detail {
  height: 100%;
  overflow: hidden;
}

.detail-card {
  height: 100%;
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-header h3 {
  margin: 0;
  color: #e5eaf3;
  font-size: 18px;
  font-weight: 600;
}

.header-tags {
  display: flex;
  gap: 8px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  margin: 0 0 12px;
  color: #e5eaf3;
  font-size: 16px;
  font-weight: 500;
}

.detail-section h5 {
  margin: 0 0 8px;
  color: #909399;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.description {
  color: #e5eaf3;
  line-height: 1.6;
  margin: 0;
}

.key-points {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.key-point-tag {
  background: rgba(64, 158, 255, 0.1);
  border-color: rgba(64, 158, 255, 0.2);
  color: #409eff;
}

.resources {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resource-group {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 4px;
  padding: 12px;
}

.resource-description {
  color: #909399;
  margin: 0 0 8px;
}

.related-nodes {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.related-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.time-info {
  margin-bottom: 0;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
}

:deep(.el-descriptions) {
  --el-descriptions-item-bordered-label-background: rgba(255, 255, 255, 0.02);
  --el-descriptions-item-label-color: #909399;
  --el-descriptions-item-color: #e5eaf3;
}

:deep(.el-collapse) {
  border: none;
  background: transparent;
}

:deep(.el-collapse-item__header) {
  background: transparent;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #e5eaf3;
}

:deep(.el-collapse-item__content) {
  background: transparent;
  color: #e5eaf3;
  padding: 12px;
}

:deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e5eaf3;
}

:deep(.el-button--default:hover) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

:deep(.el-button--primary) {
  background: #409eff;
  border-color: #409eff;
}

:deep(.el-empty__image) {
  color: #909399;
}
</style> 