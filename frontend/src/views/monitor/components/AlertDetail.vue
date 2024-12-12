<template>
  <div class="alert-detail">
    <el-descriptions
      :column="2"
      border
      class="alert-info"
    >
      <el-descriptions-item label="预警类型">
        <el-tag :type="getAlertTypeTag(alertInfo.type)">
          {{ getAlertTypeLabel(alertInfo.type) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="预警状态">
        <el-tag :type="getStatusTag(alertInfo.status)">
          {{ getStatusLabel(alertInfo.status) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="发生时间">
        {{ formatDate(alertInfo.time) }}
      </el-descriptions-item>
      <el-descriptions-item label="处理时间" v-if="alertInfo.handledAt">
        {{ formatDate(alertInfo.handledAt) }}
      </el-descriptions-item>
      <el-descriptions-item label="预警内容" :span="2">
        {{ alertInfo.content }}
      </el-descriptions-item>
      <el-descriptions-item label="处理记录" :span="2" v-if="alertInfo.handleNote">
        {{ alertInfo.handleNote }}
      </el-descriptions-item>
    </el-descriptions>

    <!-- 处理表单 -->
    <div v-if="alertInfo.status === 'pending'" class="handle-form">
      <h3>处理预警</h3>
      <el-form ref="formRef" :model="handleForm" :rules="rules" label-width="100px">
        <el-form-item label="处理方式" prop="handleType">
          <el-radio-group v-model="handleForm.handleType">
            <el-radio label="resolve">解决</el-radio>
            <el-radio label="ignore">忽略</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="处理说明" prop="note">
          <el-input
            v-model="handleForm.note"
            type="textarea"
            :rows="4"
            placeholder="请输入处理说明"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submitHandle">
            提交
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 相关记录 -->
    <div class="related-records" v-if="relatedAlerts.length > 0">
      <h3>相关记录</h3>
      <el-timeline>
        <el-timeline-item
          v-for="item in relatedAlerts"
          :key="item.id"
          :timestamp="formatDate(item.time)"
          :type="getTimelineItemType(item.status)"
        >
          <div class="timeline-content">
            <div class="alert-type">
              <el-tag size="small" :type="getAlertTypeTag(item.type)">
                {{ getAlertTypeLabel(item.type) }}
              </el-tag>
            </div>
            <div class="alert-content">{{ item.content }}</div>
            <div class="alert-status">
              <el-tag size="small" :type="getStatusTag(item.status)">
                {{ getStatusLabel(item.status) }}
              </el-tag>
            </div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import dayjs from 'dayjs'

const props = defineProps<{
  alertId: number
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'refresh'): void
}>()

// 预警信息
const alertInfo = ref({
  id: 0,
  type: '',
  status: 'pending',
  time: '',
  handledAt: '',
  content: '',
  handleNote: ''
})

// 相关记录
const relatedAlerts = ref([])

// 处理表单
const formRef = ref<FormInstance>()
const submitting = ref(false)
const handleForm = ref({
  handleType: 'resolve',
  note: ''
})

// 表单验证规则
const rules: FormRules = {
  handleType: [
    { required: true, message: '请选择处理方式', trigger: 'change' }
  ],
  note: [
    { required: true, message: '请输入处理说明', trigger: 'blur' },
    { min: 10, message: '处理说明不能少于10个字符', trigger: 'blur' }
  ]
}

// 加载预警详情
const loadAlertDetail = async () => {
  try {
    // TODO: 调用API获取预警详情
    alertInfo.value = {
      id: props.alertId,
      type: 'login',
      status: 'pending',
      time: '2023-12-12 10:30:00',
      content: '检测到异常登录行为，IP地址: 192.168.1.100，尝试次数: 5次',
      handleNote: ''
    }
  } catch (error) {
    console.error('Failed to load alert detail:', error)
    ElMessage.error('加载预警详情失败')
  }
}

// 加载相关记录
const loadRelatedAlerts = async () => {
  try {
    // TODO: 调用API获取相关记录
    relatedAlerts.value = [
      {
        id: 1,
        type: 'login',
        status: 'handled',
        time: '2023-12-11 15:30:00',
        content: '检测到异常登录行为，IP地址: 192.168.1.100，尝试次数: 3次'
      },
      {
        id: 2,
        type: 'login',
        status: 'ignored',
        time: '2023-12-10 14:20:00',
        content: '检测到异常登录行为，IP地址: 192.168.1.100，尝试次数: 4次'
      }
    ]
  } catch (error) {
    console.error('Failed to load related alerts:', error)
    ElMessage.error('加载相关记录失败')
  }
}

// 提交处理
const submitHandle = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        // TODO: 调用API提交处理结果
        await new Promise(resolve => setTimeout(resolve, 1000))
        ElMessage.success('处理成功')
        emit('refresh')
        emit('close')
      } catch (error) {
        console.error('Failed to handle alert:', error)
        ElMessage.error('处理失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 工具函数
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const getAlertTypeTag = (type: string): string => {
  const types: Record<string, string> = {
    login: 'danger',
    operation: 'warning',
    security: 'error'
  }
  return types[type] || 'info'
}

const getStatusTag = (status: string): string => {
  const types: Record<string, string> = {
    pending: 'danger',
    processing: 'warning',
    handled: 'success',
    ignored: 'info'
  }
  return types[status] || 'info'
}

const getAlertTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    login: '登录预警',
    operation: '操作预警',
    security: '安全预警'
  }
  return labels[type] || type
}

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    handled: '已处理',
    ignored: '已忽略'
  }
  return labels[status] || status
}

const getTimelineItemType = (status: string): string => {
  const types: Record<string, string> = {
    pending: 'warning',
    processing: 'primary',
    handled: 'success',
    ignored: 'info'
  }
  return types[status] || 'info'
}

// 初始化
onMounted(() => {
  loadAlertDetail()
  loadRelatedAlerts()
})
</script>

<style lang="scss" scoped>
.alert-detail {
  padding: 20px;

  .alert-info {
    margin-bottom: 24px;
  }

  .handle-form {
    margin-top: 24px;
    padding: 24px;
    background: var(--el-fill-color-light);
    border-radius: 8px;

    h3 {
      margin: 0 0 16px;
      font-size: 16px;
      font-weight: 500;
    }
  }

  .related-records {
    margin-top: 24px;

    h3 {
      margin: 0 0 16px;
      font-size: 16px;
      font-weight: 500;
    }

    .timeline-content {
      display: flex;
      align-items: center;
      gap: 12px;

      .alert-type {
        width: 80px;
      }

      .alert-content {
        flex: 1;
        color: var(--el-text-color-regular);
      }

      .alert-status {
        width: 60px;
        text-align: right;
      }
    }
  }
}
</style> 