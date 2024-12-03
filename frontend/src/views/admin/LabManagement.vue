<template>
  <div class="lab-management">
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>实验室管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><plus /></el-icon>
            添加实验环境
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索实验名称/描述"
          class="search-input"
          clearable
        >
          <template #prefix>
            <el-icon><search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="typeFilter" placeholder="类型" clearable>
          <el-option label="Web安全" value="web" />
          <el-option label="系统安全" value="system" />
          <el-option label="网络安全" value="network" />
        </el-select>
        <el-select v-model="statusFilter" placeholder="状态" clearable>
          <el-option label="运行中" value="running" />
          <el-option label="已停止" value="stopped" />
          <el-option label="维护中" value="maintenance" />
        </el-select>
      </div>

      <!-- 实验室表格 -->
      <el-table :data="filteredLabs" style="width: 100%" v-loading="loading">
        <el-table-column label="实验环境" min-width="300">
          <template #default="{ row }">
            <div class="lab-info">
              <el-image
                :src="row.image || '/placeholder.png'"
                class="lab-image"
                fit="cover"
              />
              <div class="lab-details">
                <span class="title">{{ row.name }}</span>
                <span class="description">{{ row.description }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeType(row.type)">
              {{ getTypeLabel(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="320" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" size="small" @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button 
                :type="row.status === 'running' ? 'warning' : 'success'"
                size="small" 
                @click="handleToggleStatus(row)"
              >
                {{ row.status === 'running' ? '停止' : '启动' }}
              </el-button>
              <el-button type="info" size="small" @click="handleMonitor(row)">
                监控
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 实验室表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加实验环境' : '编辑实验环境'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        style="max-width: 560px"
      >
        <el-form-item label="环境名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="环境描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="环境类型" prop="type">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="Web安全" value="web" />
            <el-option label="系统安全" value="system" />
            <el-option label="网络安全" value="network" />
          </el-select>
        </el-form-item>
        <el-form-item label="Docker镜像" prop="docker_image">
          <el-input v-model="form.docker_image" />
        </el-form-item>
        <el-form-item label="端口映射" prop="ports">
          <el-input v-model="form.ports" placeholder="例如: 80:80,443:443" />
        </el-form-item>
        <el-form-item label="环境变量" prop="env_vars">
          <el-input v-model="form.env_vars" type="textarea" :rows="3" placeholder="每行一个，格式：KEY=VALUE" />
        </el-form-item>
        <el-form-item label="资源限制">
          <div class="resource-limits">
            <el-input-number
              v-model="form.cpu_limit"
              :min="0.1"
              :max="4"
              :step="0.1"
              placeholder="CPU核心数"
            />
            <el-input-number
              v-model="form.memory_limit"
              :min="128"
              :max="4096"
              :step="128"
              placeholder="内存(MB)"
            />
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 监控对话框 -->
    <el-dialog
      v-model="monitorVisible"
      title="环境监控"
      width="800px"
    >
      <div class="monitor-content">
        <el-tabs v-model="monitorTab">
          <el-tab-pane label="资源使用" name="resources">
            <div class="resource-charts">
              <div class="chart-item">
                <h4>CPU使用率</h4>
                <div class="chart-container">
                  <!-- CPU使用率图表 -->
                </div>
              </div>
              <div class="chart-item">
                <h4>内存使用率</h4>
                <div class="chart-container">
                  <!-- 内存使用率图表 -->
                </div>
              </div>
              <div class="chart-item">
                <h4>网络流量</h4>
                <div class="chart-container">
                  <!-- 网络流量图表 -->
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="容器日志" name="logs">
            <div class="log-content">
              <pre>{{ containerLogs }}</pre>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

// 状态
const loading = ref(false)
const searchQuery = ref('')
const typeFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()
const monitorVisible = ref(false)
const monitorTab = ref('resources')
const containerLogs = ref('')

// 表单数据
const form = ref({
  name: '',
  description: '',
  type: 'web',
  docker_image: '',
  ports: '',
  env_vars: '',
  cpu_limit: 0.5,
  memory_limit: 512
})

// 表单验证规则
const rules: FormRules = {
  name: [
    { required: true, message: '请输入环境名称', trigger: 'blur' },
    { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入环境描述', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择环境类型', trigger: 'change' }
  ],
  docker_image: [
    { required: true, message: '请输入Docker镜像', trigger: 'blur' }
  ]
}

// 模拟实验室数据
const labs = ref([
  {
    id: 1,
    name: 'SQL注入实验环境',
    description: '用于学习和实践SQL注入攻击的环境',
    image: '',
    type: 'web',
    status: 'running',
    docker_image: 'webgoat/webgoat-8.0',
    ports: '8080:8080',
    created_at: '2024-01-01T00:00:00Z'
  },
  {
    id: 2,
    name: 'Linux提权实验环境',
    description: '用于学习Linux系统提权技术的环境',
    image: '',
    type: 'system',
    status: 'stopped',
    docker_image: 'vulnerables/linux-privesc',
    ports: '22:22',
    created_at: '2024-01-02T00:00:00Z'
  },
  {
    id: 3,
    name: '网络嗅探实验环境',
    description: '用于学习网络数据包分析的环境',
    image: '',
    type: 'network',
    status: 'maintenance',
    docker_image: 'vulnerables/network-analysis',
    ports: '80:80,8080:8080',
    created_at: '2024-01-03T00:00:00Z'
  }
])

// 过滤后的实验室列表
const filteredLabs = computed(() => {
  return labs.value.filter(lab => {
    const matchQuery = searchQuery.value === '' ||
      lab.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      lab.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchType = typeFilter.value === '' || lab.type === typeFilter.value
    const matchStatus = statusFilter.value === '' || lab.status === statusFilter.value
    return matchQuery && matchType && matchStatus
  })
})

// 工具函数
const getTypeType = (type: string) => {
  const types: Record<string, string> = {
    web: 'primary',
    system: 'warning',
    network: 'info'
  }
  return types[type] || 'info'
}

const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    web: 'Web安全',
    system: '系统安全',
    network: '网络安全'
  }
  return labels[type] || type
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    running: 'success',
    stopped: 'info',
    maintenance: 'warning'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    running: '运行中',
    stopped: '已停止',
    maintenance: '维护中'
  }
  return labels[status] || status
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 事件处理函数
const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    name: '',
    description: '',
    type: 'web',
    docker_image: '',
    ports: '',
    env_vars: '',
    cpu_limit: 0.5,
    memory_limit: 512
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    `确定要删除实验环境 ${row.name} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用删除API
    ElMessage.success('删除成功')
  }).catch(() => {
    // 取消删除
  })
}

const handleToggleStatus = (row: any) => {
  const action = row.status === 'running' ? '停止' : '启动'
  ElMessageBox.confirm(
    `确定要${action}实验环境 ${row.name} 吗？`,
    '确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 调用启动/停止API
    ElMessage.success(`${action}成功`)
  }).catch(() => {
    // 取消操作
  })
}

const handleMonitor = (row: any) => {
  monitorVisible.value = true
  monitorTab.value = 'resources'
  // TODO: 获取容器监控数据和日志
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid, fields) => {
    if (valid) {
      // TODO: 调用添加/编辑API
      ElMessage.success(dialogType.value === 'add' ? '添加成功' : '编辑成功')
      dialogVisible.value = false
    }
  })
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  // TODO: 重新加载数据
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  // TODO: 重新加载数据
}
</script>

<style scoped>
.lab-management {
  padding: 24px;
}

.table-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 24px;
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.lab-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.lab-image {
  width: 120px;
  height: 68px;
  border-radius: 4px;
  object-fit: cover;
}

.lab-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.description {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.resource-limits {
  display: flex;
  gap: 16px;
}

.monitor-content {
  height: 500px;
}

.resource-charts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding: 16px;
}

.chart-item {
  background: var(--el-bg-color-page);
  border-radius: 8px;
  padding: 16px;
}

.chart-container {
  height: 200px;
}

.log-content {
  height: 400px;
  overflow-y: auto;
  background: var(--el-bg-color-page);
  border-radius: 8px;
  padding: 16px;
}

.log-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  font-size: 12px;
  line-height: 1.5;
}
</style> 