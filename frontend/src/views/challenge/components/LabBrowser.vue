<template>
  <div class="browser-window">
    <div class="browser-header">
      <div class="browser-controls">
        <span class="control close"></span>
        <span class="control minimize"></span>
        <span class="control maximize"></span>
      </div>
      <div class="browser-address-bar">
        <el-input
          v-model="currentUrl"
          :readonly="true"
          class="browser-url"
        >
          <template #prefix>
            <el-icon><Lock /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="browser-actions">
        <el-button-group>
          <el-button :icon="RefreshLeft" circle @click="refreshPage" />
          <el-button :icon="Search" circle @click="viewSource" />
        </el-button-group>
      </div>
    </div>
    <div class="browser-content">
      <div class="vulnerable-app">
        <template v-if="challengeId === 1">
          <!-- SQL注入测试页面 -->
          <div class="sql-injection-lab">
            <div class="lab-header">
              <h2>员工信息查询系统</h2>
              <p class="system-info">系统版本: v1.0.0 | 数据库: MySQL 5.7</p>
            </div>

            <!-- 查询表单 -->
            <div class="search-form">
              <el-form>
                <el-form-item>
                  <el-input
                    v-model="searchId"
                    placeholder="请输入员工ID"
                    class="search-input"
                  >
                    <template #prepend>员工ID</template>
                    <template #append>
                      <el-button @click="searchEmployee">查询</el-button>
                    </template>
                  </el-input>
                </el-form-item>
              </el-form>

              <!-- URL 显示 -->
              <div class="url-display">
                当前请求: GET /api/employee?id={{ encodeURIComponent(searchId) }}
              </div>
            </div>

            <!-- 查询结果 -->
            <div v-if="searchResult" class="search-result">
              <div v-if="searchError" class="error-message">
                <el-alert
                  :title="searchError"
                  type="error"
                  :closable="false"
                  show-icon
                />
              </div>
              <div v-else>
                <el-table :data="searchResult" border style="width: 100%">
                  <el-table-column
                    v-for="col in visibleColumns"
                    :key="col.prop"
                    :prop="col.prop"
                    :label="col.label"
                  />
                </el-table>
                
                <!-- 注入成功后显示的隐藏表 -->
                <template v-if="showHiddenTables">
                  <div class="hidden-tables">
                    <h3>发现数据库表:</h3>
                    <el-tag 
                      v-for="table in hiddenTables" 
                      :key="table"
                      class="table-tag"
                    >
                      {{ table }}
                    </el-tag>
                  </div>
                </template>
              </div>
            </div>

            <!-- 注入过程提示 -->
            <div v-if="injectionHints.length > 0" class="injection-hints">
              <el-timeline>
                <el-timeline-item
                  v-for="(hint, index) in injectionHints"
                  :key="index"
                  :type="hint.type"
                  :color="hint.color"
                  :timestamp="hint.timestamp"
                >
                  {{ hint.content }}
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </template>
        
        <template v-else-if="challengeId === 2">
          <!-- XSS测试页面 -->
          <div class="message-board">
            <h2>留言板</h2>
            <div class="message-list">
              <div v-for="msg in messages" :key="msg.id" class="message-item">
                <div class="message-header">
                  <span class="message-author">{{ msg.author }}</span>
                  <span class="message-time">{{ msg.time }}</span>
                </div>
                <div class="message-content" v-html="msg.content"></div>
              </div>
            </div>
            <div class="message-form">
              <el-input
                v-model="newMessage"
                type="textarea"
                rows="3"
                placeholder="输入留言内容"
              />
              <el-button type="primary" @click="submitMessage" style="margin-top: 10px">
                发表留言
              </el-button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Lock, User, RefreshLeft, Search } from '@element-plus/icons-vue'
import { format } from 'date-fns'

defineOptions({
  name: 'LabBrowser'
})

const props = defineProps<{
  challengeId: number
}>()

// 通用状态
const currentUrl = ref('http://localhost:8080')
const newMessage = ref('')

// SQL注入相关状态
const searchId = ref('')
const searchResult = ref<any[] | null>(null)
const searchError = ref('')
const showHiddenTables = ref(false)
const injectionHints = ref<Array<{
  content: string
  timestamp: string
  type?: 'primary' | 'success' | 'warning' | 'danger'
  color?: string
}>>([])

// 定义可见的数据列
const visibleColumns = ref([
  { prop: 'id', label: 'ID' },
  { prop: 'username', label: '用户名' },
  { prop: 'email', label: '邮箱' }
])

// 隐藏的数据库表
const hiddenTables = ref([
  'employees',
  'users',
  'admin_users',
  'system_config',
  'secret_flags'
])

// 模拟的数据库查询结果
const mockDbQuery = (sql: string) => {
  // 模拟users表
  const users = [
    { id: 1, username: 'admin', email: 'admin@example.com', password: 'c4ca4238a0b923820dcc509a6f75849b' },
    { id: 2, username: 'test', email: 'test@example.com', password: '098f6bcd4621d373cade4e832627b4f6' }
  ]
  
  // 模拟flag表
  const flags = [
    { id: 1, flag: 'flag{n0_w4y_y0u_f0und_m3}' }
  ]

  return { users, flags }
}

// SQL注入测试
const searchEmployee = () => {
  searchError.value = ''
  searchResult.value = null
  showHiddenTables.value = false
  
  try {
    // 构造模拟的SQL查询
    const sql = `SELECT id, username, email FROM users WHERE id = ${searchId.value}`
    addInjectionHint(`执行SQL: ${sql}`, 'info')

    // 判断各种注入情况
    const input = searchId.value.toLowerCase()

    // 基本的注入检测
    if (input.includes("'") && !input.includes('table_schema') && !input.includes('table_name')) {
      searchError.value = `Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '"${searchId.value}"' at line 1`
      addInjectionHint('SQL语法错误，注入点已确认', 'warning')
      return
    }

    // 判断列数
    if (input.includes('order by')) {
      const colNum = parseInt(input.match(/order by (\d+)/i)?.[1] || '0')
      if (colNum <= 3) {
        addInjectionHint(`ORDER BY ${colNum} 成功，列数 >= ${colNum}`, 'success')
        searchResult.value = [{ id: 1, username: 'test', email: 'test@example.com' }]
      } else {
        searchError.value = `Unknown column '${colNum}' in 'order clause'`
        addInjectionHint(`ORDER BY ${colNum} 失败，列数 < ${colNum}`, 'warning')
      }
      return
    }

    // 确定显示位置
    if (input.match(/union\s+select\s+1\s*,\s*2\s*,\s*3/i)) {
      searchResult.value = [
        { id: '1', username: '2', email: '3' }
      ]
      addInjectionHint('成功确定显示位置：id=1, username=2, email=3', 'success')
      return
    }

    // 获取数据库信息
    if (input.includes('database()')) {
      searchResult.value = [
        { id: '1', username: 'ctf_db', email: '3' }
      ]
      addInjectionHint('当前数据库名: ctf_db', 'success')
      return
    }

    if (input.includes('version()')) {
      searchResult.value = [
        { id: '1', username: '5.7.35-MySQL', email: '3' }
      ]
      addInjectionHint('数据库版本: 5.7.35-MySQL', 'success')
      return
    }

    // 获取表名
    if (input.includes('information_schema.tables') && input.includes('table_schema') && input.includes('ctf_db')) {
      searchResult.value = [
        { id: '1', username: 'users', email: '3' },
        { id: '1', username: 'fl4g_table', email: '3' }
      ]
      addInjectionHint('成功获取数据库表', 'success')
      addInjectionHint('发现表: users', 'info')
      addInjectionHint('发现表: fl4g_table', 'info')
      return
    }

    // 获取列名
    if (input.includes('information_schema.columns') && input.includes('table_name=\'fl4g_table\'')) {
      searchResult.value = [
        { id: '1', username: 'id', email: '3' },
        { id: '1', username: 'fl4g', email: '3' }
      ]
      addInjectionHint('成功获取表结构', 'success')
      addInjectionHint('发现列: id', 'info')
      addInjectionHint('发现列: fl4g', 'info')
      return
    }

    // 获取flag
    const flagMatch = input.match(/union\s+select\s+.*\s+from\s+fl4g_table/i)
    if (flagMatch) {
      searchResult.value = [
        { id: '1', username: 'Congratulations!', email: 'flag{sql_injection_success}' }
      ]
      addInjectionHint('成功获取flag！', 'success')
      ElMessage.success('恭喜你找到了Flag！flag{sql_injection_success}')
      return
    }

    // 正常查询
    if (/^\d+$/.test(searchId.value)) {
      const { users } = mockDbQuery(sql)
      const user = users.find(u => u.id === parseInt(searchId.value))
      if (user) {
        searchResult.value = [{
          id: user.id,
          username: user.username,
          email: user.email
        }]
        addInjectionHint('查询成功', 'primary')
      } else {
        searchResult.value = []
        addInjectionHint('未找到结果', 'info')
      }
    } else if (searchId.value === '') {
      searchError.value = '请输入ID'
    }
  } catch (error) {
    searchError.value = String(error)
    addInjectionHint('查询执行出错', 'danger')
  }
}

// 添加注入提示
const addInjectionHint = (content: string, type: 'primary' | 'success' | 'warning' | 'danger' | 'info') => {
  const colorMap = {
    primary: '#409EFF',
    success: '#67C23A',
    warning: '#E6A23C',
    danger: '#F56C6C',
    info: '#909399'
  }
  
  injectionHints.value.unshift({
    content,
    timestamp: format(new Date(), 'HH:mm:ss'),
    type,
    color: colorMap[type]
  })
}

// XSS相关状态
const messages = ref([
  {
    id: 1,
    author: 'admin',
    time: '2024-01-20 10:00',
    content: '欢迎来到留言板！'
  }
])

// XSS测试
const submitMessage = () => {
  if (newMessage.value.includes('<script>') || newMessage.value.includes('onerror=')) {
    ElMessage.success('XSS攻击成功！Flag: flag{xss_attack_success}')
  }
  messages.value.push({
    id: messages.value.length + 1,
    author: '游客',
    time: format(new Date(), 'yyyy-MM-dd HH:mm'),
    content: newMessage.value
  })
  newMessage.value = ''
}

// 浏览器功能
const refreshPage = () => {
  searchId.value = ''
  searchResult.value = null
  searchError.value = ''
  showHiddenTables.value = false
  injectionHints.value = []
  messages.value = [{
    id: 1,
    author: 'admin',
    time: '2024-01-20 10:00',
    content: '欢迎来到留言板！'
  }]
  newMessage.value = ''
}

const viewSource = () => {
  ElMessage.info('查看源代码功能即将推出')
}
</script>

<style scoped>
.browser-window {
  height: 400px;
  background: #1e1e1e;
  border-radius: 4px;
  overflow: hidden;
}

.browser-header {
  background: #323232;
  padding: 8px;
  display: flex;
  gap: 8px;
  align-items: center;
  border-bottom: 1px solid #424242;
}

.browser-controls {
  display: flex;
  gap: 8px;
}

.control {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.control.close {
  background: #ff5f56;
}

.control.minimize {
  background: #ffbd2e;
}

.control.maximize {
  background: #27c93f;
}

.browser-address-bar {
  flex: 1;
}

.browser-url :deep(.el-input__wrapper) {
  background: #1e1e1e;
}

.browser-content {
  height: calc(100% - 53px);
  overflow-y: auto;
  background: #fff;
}

.vulnerable-app {
  padding: 20px;
}

.sql-injection-lab {
  max-width: 800px;
  margin: 0 auto;
}

.lab-header {
  text-align: center;
  margin-bottom: 20px;
}

.lab-header h2 {
  margin: 0 0 8px;
  color: #333;
}

.system-info {
  color: #666;
  font-size: 12px;
  margin: 0;
}

.search-form {
  margin-bottom: 20px;
}

.url-display {
  font-family: monospace;
  background: #f5f7fa;
  padding: 8px;
  border-radius: 4px;
  color: #666;
  margin-top: 8px;
  font-size: 12px;
}

.search-result {
  margin-bottom: 20px;
}

.hidden-tables {
  margin-top: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.hidden-tables h3 {
  margin: 0 0 12px;
  color: #333;
  font-size: 14px;
}

.table-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.injection-hints {
  margin-top: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
}

:deep(.el-timeline-item__node) {
  width: 12px;
  height: 12px;
}

:deep(.el-timeline-item__timestamp) {
  font-size: 12px;
}

.message-board {
  max-width: 600px;
  margin: 0 auto;
}

.message-board h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.message-list {
  margin-bottom: 20px;
}

.message-item {
  border-bottom: 1px solid #eee;
  padding: 10px 0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  color: #666;
  font-size: 12px;
}

.message-content {
  color: #333;
}
</style> 