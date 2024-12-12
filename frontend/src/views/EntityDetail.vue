<template>
  <div class="entity-detail">
    <div class="page-header">
      <h2>{{ entity?.name }}</h2>
      <p>{{ entity?.description }}</p>
    </div>

    <el-tabs v-model="activeTab" class="detail-tabs">
      <el-tab-pane label="基本信息" name="info">
        <div class="info-section">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="类型">
              {{ getEntityTypeLabel(entity?.entity_type) }}
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(entity?.status)">
                {{ getStatusLabel(entity?.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ formatDate(entity?.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间">
              {{ formatDate(entity?.updated_at) }}
            </el-descriptions-item>
          </el-descriptions>

          <div class="properties-section" v-if="entity?.properties">
            <h3>属性</h3>
            <el-descriptions :column="2" border>
              <el-descriptions-item
                v-for="(value, key) in entity.properties"
                :key="key"
                :label="key"
              >
                {{ value }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="关系图" name="graph">
        <div class="graph-section">
          <knowledge-graph
            :center-node-id="entityId"
            :depth="2"
            style="height: 600px"
          />
        </div>
      </el-tab-pane>

      <el-tab-pane label="学习记录" name="learning">
        <div class="learning-section">
          <learning-record :entity-id="entityId" />
        </div>
      </el-tab-pane>

      <el-tab-pane label="反馈" name="feedback">
        <div class="feedback-section">
          <div class="feedback-header">
            <el-button type="primary" @click="showFeedbackForm = true">
              提交反馈
            </el-button>
          </div>
          <feedback-list
            :entity-id="entityId"
            @refresh="loadEntity"
          />
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 反馈表单对话框 -->
    <el-dialog
      v-model="showFeedbackForm"
      title="提交反馈"
      width="50%"
      destroy-on-close
    >
      <feedback-form
        v-if="showFeedbackForm"
        :entity-id="entityId"
        @submit="handleFeedbackSubmit"
        @cancel="showFeedbackForm = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import KnowledgeGraph from '@/components/KnowledgeGraph.vue'
import LearningRecord from '@/components/learning/LearningRecord.vue'
import FeedbackList from '@/components/feedback/FeedbackList.vue'
import FeedbackForm from '@/components/feedback/FeedbackForm.vue'
import { useKnowledgeStore } from '@/stores/knowledge'
import { formatDate } from '@/utils/date'

const route = useRoute()
const knowledgeStore = useKnowledgeStore()

// 状态
const entityId = ref(parseInt(route.params.id as string))
const entity = ref(null)
const activeTab = ref('info')
const showFeedbackForm = ref(false)

// 加载实体详情
const loadEntity = async () => {
  try {
    entity.value = await knowledgeStore.getEntity(entityId.value)
  } catch (error) {
    console.error('Failed to load entity:', error)
    ElMessage.error('加载知识点详情失败')
  }
}

// 处理反馈提交
const handleFeedbackSubmit = () => {
  showFeedbackForm.value = false
  ElMessage.success('反馈提交成功')
}

// 获取实体类型标签
const getEntityTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    concept: '概念',
    attack: '攻击方式',
    vulnerability: '漏洞',
    defense: '防御方法',
    tool: '工具',
    protocol: '协议',
    platform: '平台'
  }
  return labels[type] || type
}

// 获取状态标签
const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    active: '活跃',
    inactive: '不活跃',
    pending: '待审核',
    deleted: '已删除'
  }
  return labels[status] || status
}

// 获取状态类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    inactive: 'info',
    pending: 'warning',
    deleted: 'danger'
  }
  return types[status] || ''
}

// 初始化
onMounted(() => {
  loadEntity()
})
</script>

<style scoped>
.entity-detail {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.page-header p {
  margin: 8px 0 0;
  color: #666;
}

.detail-tabs {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.info-section {
  padding: 20px;
}

.properties-section {
  margin-top: 20px;
}

.properties-section h3 {
  margin-bottom: 16px;
}

.graph-section {
  padding: 20px;
}

.learning-section {
  padding: 20px;
}

.feedback-section {
  padding: 20px;
}

.feedback-header {
  margin-bottom: 20px;
}
</style> 