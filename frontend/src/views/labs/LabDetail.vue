<template>
  <div class="lab-detail">
    <!-- 实验头部 -->
    <div class="lab-header">
      <div class="header-content">
        <div class="lab-info">
          <h1>{{ lab.title }}</h1>
          <p class="description">{{ lab.description }}</p>
          <div class="meta">
            <div class="meta-item">
              <el-icon><Timer /></el-icon>
              <span>预计用时：{{ lab.duration }}</span>
            </div>
            <div class="meta-item">
              <el-icon><User /></el-icon>
              <span>{{ lab.participants }}人参与</span>
            </div>
            <div class="meta-item">
              <el-tag :type="getDifficultyType(lab.difficulty)">
                {{ getDifficultyText(lab.difficulty) }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="lab-action">
          <el-button 
            type="primary" 
            size="large"
            :loading="starting"
            @click="handleStart"
          >
            {{ started ? '继续实验' : '开始实验' }}
          </el-button>
          <div class="progress" v-if="started">
            <span>实验进度</span>
            <el-progress 
              :percentage="lab.progress" 
              :status="getProgressStatus(lab.progress)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 实验内容 -->
    <div class="lab-content">
      <el-tabs v-model="activeTab">
        <!-- 实验介绍 -->
        <el-tab-pane label="实验介绍" name="introduction">
          <div class="introduction" v-html="lab.introduction"></div>
        </el-tab-pane>

        <!-- 实验步骤 -->
        <el-tab-pane label="实验步骤" name="steps">
          <el-steps 
            :active="lab.currentStep" 
            direction="vertical"
            finish-status="success"
          >
            <el-step 
              v-for="step in lab.steps" 
              :key="step.id"
              :title="step.title"
              :description="step.description"
            >
              <template #icon>
                <el-icon v-if="step.completed"><Check /></el-icon>
                <el-icon v-else-if="step.id === lab.currentStep"><Loading /></el-icon>
              </template>
            </el-step>
          </el-steps>
        </el-tab-pane>

        <!-- 实验环境 -->
        <el-tab-pane label="实验环境" name="environment">
          <div class="environment">
            <div class="environment-info">
              <h3>环境配置</h3>
              <el-descriptions :column="1" border>
                <el-descriptions-item label="操作系统">
                  {{ lab.environment.os }}
                </el-descriptions-item>
                <el-descriptions-item label="软件版本">
                  {{ lab.environment.version }}
                </el-descriptions-item>
                <el-descriptions-item label="网络配置">
                  {{ lab.environment.network }}
                </el-descriptions-item>
                <el-descriptions-item label="其他要求">
                  {{ lab.environment.requirements }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
            
            <div class="environment-status">
              <h3>环境状态</h3>
              <div class="status-list">
                <div 
                  v-for="(status, service) in lab.environment.status" 
                  :key="service"
                  class="status-item"
                >
                  <span class="service-name">{{ service }}</span>
                  <el-tag 
                    :type="status === 'running' ? 'success' : 'danger'"
                    size="small"
                  >
                    {{ status === 'running' ? '运行中' : '已停止' }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 实验报告 -->
        <el-tab-pane label="实验报告" name="report">
          <div class="report">
            <el-form 
              ref="reportForm"
              :model="reportForm"
              :rules="reportRules"
              label-width="100px"
            >
              <el-form-item label="实验过程" prop="process">
                <el-input
                  v-model="reportForm.process"
                  type="textarea"
                  :rows="6"
                  placeholder="请详细描述实验过程..."
                />
              </el-form-item>
              
              <el-form-item label="实验结果" prop="result">
                <el-input
                  v-model="reportForm.result"
                  type="textarea"
                  :rows="4"
                  placeholder="请描述实验结果..."
                />
              </el-form-item>
              
              <el-form-item label="实验总结" prop="summary">
                <el-input
                  v-model="reportForm.summary"
                  type="textarea"
                  :rows="4"
                  placeholder="请总结实验心得..."
                />
              </el-form-item>
              
              <el-form-item label="截图附件">
                <el-upload
                  action="#"
                  list-type="picture-card"
                  :auto-upload="false"
                  :on-change="handleUploadChange"
                >
                  <el-icon><Plus /></el-icon>
                </el-upload>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  :loading="submitting"
                  @click="submitReport"
                >
                  提交报告
                </el-button>
                <el-button @click="saveDraft">保存草稿</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Timer, User, Check, Loading, Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

export default defineComponent({
  name: 'LabDetail',
  components: {
    Timer,
    User,
    Check,
    Loading,
    Plus
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const activeTab = ref('introduction')
    const starting = ref(false)
    const started = ref(false)
    const submitting = ref(false)
    const reportForm = ref({
      process: '',
      result: '',
      summary: '',
      attachments: []
    })
    
    // 模拟实验数据
    const lab = ref({
      id: 1,
      title: 'SQL注入漏洞实验',
      description: '通过实验了解SQL注入原理，掌握SQL注入的检测和防护方法',
      difficulty: 'medium',
      duration: '2小时',
      participants: 1234,
      progress: 60,
      currentStep: 2,
      introduction: `
        <h3>实验目的</h3>
        <p>通过本实验，学习者将：</p>
        <ul>
          <li>理解SQL注入漏洞的原理</li>
          <li>掌握SQL注入的检测方法</li>
          <li>学习SQL注入的防护措施</li>
          <li>提高Web安全防护意识</li>
        </ul>
        
        <h3>实验准备</h3>
        <ul>
          <li>基本的SQL语法知识</li>
          <li>Web开发基础</li>
          <li>HTTP协议基础</li>
        </ul>
        
        <h3>注意事项</h3>
        <ul>
          <li>严格遵守实验规范</li>
          <li>保护实验环境安全</li>
          <li>及时记录实验过程</li>
        </ul>
      `,
      steps: [
        {
          id: 1,
          title: '环境准备',
          description: '配置实验环境，确保所需服务正常运行',
          completed: true
        },
        {
          id: 2,
          title: 'SQL注入原理',
          description: '学习SQL注入的基本原理和类型',
          completed: false
        },
        {
          id: 3,
          title: '漏洞检测',
          description: '使用工具和手动方式检测SQL注入漏洞',
          completed: false
        },
        {
          id: 4,
          title: '漏洞利用',
          description: '在测试环境中进行SQL注入攻击演练',
          completed: false
        },
        {
          id: 5,
          title: '防护措施',
          description: '学习和实施SQL注入的防护方法',
          completed: false
        }
      ],
      environment: {
        os: 'Ubuntu 20.04 LTS',
        version: 'MySQL 8.0',
        network: '独立网络环境',
        requirements: '需要2GB以上内��，10GB磁盘空间',
        status: {
          'Web服务器': 'running',
          'MySQL数据库': 'running',
          '靶机系统': 'running'
        }
      }
    })
    
    // 表单校验规则
    const reportRules: FormRules = {
      process: [
        { required: true, message: '请描述实验过程', trigger: 'blur' },
        { min: 100, message: '描述不能少于100字', trigger: 'blur' }
      ],
      result: [
        { required: true, message: '请描述实验结果', trigger: 'blur' },
        { min: 50, message: '描述不能少于50字', trigger: 'blur' }
      ],
      summary: [
        { required: true, message: '请总结实验心得', trigger: 'blur' },
        { min: 50, message: '总结不能少于50字', trigger: 'blur' }
      ]
    }
    
    // 获取难度等级文本
    const getDifficultyText = (difficulty: string) => {
      const difficultyMap = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
      }
      return difficultyMap[difficulty as keyof typeof difficultyMap]
    }
    
    // 获取难度等级标签类型
    const getDifficultyType = (difficulty: string) => {
      const typeMap = {
        easy: 'success',
        medium: 'warning',
        hard: 'danger'
      }
      return typeMap[difficulty as keyof typeof typeMap]
    }
    
    // 获取进度条状态
    const getProgressStatus = (progress: number) => {
      if (progress >= 90) return 'success'
      if (progress >= 60) return 'warning'
      return 'exception'
    }
    
    // 开始实验
    const handleStart = async () => {
      if (started.value) {
        activeTab.value = 'steps'
        return
      }
      
      try {
        starting.value = true
        // TODO: 调用开始实验API
        await new Promise(resolve => setTimeout(resolve, 1000))
        started.value = true
        activeTab.value = 'steps'
        ElMessage.success('实验环境已准备就绪')
      } catch (error) {
        ElMessage.error('启动实验环境失败，请重试')
      } finally {
        starting.value = false
      }
    }
    
    // 处理上传变化
    const handleUploadChange = (file: any) => {
      reportForm.value.attachments.push(file)
    }
    
    // 提交报告
    const submitReport = async () => {
      try {
        submitting.value = true
        // TODO: 调用提交报告API
        await new Promise(resolve => setTimeout(resolve, 1000))
        ElMessage.success('实验报告提交成功')
        router.push('/labs')
      } catch (error) {
        ElMessage.error('提交失败，请重试')
      } finally {
        submitting.value = false
      }
    }
    
    // 保存草稿
    const saveDraft = async () => {
      try {
        // TODO: 调用保存草稿API
        await new Promise(resolve => setTimeout(resolve, 500))
        ElMessage.success('草稿保存成功')
      } catch (error) {
        ElMessage.error('保存失败，请重试')
      }
    }
    
    onMounted(() => {
      // TODO: 根据路由参数加载实验数据
      const labId = route.params.id
      console.log('Loading lab:', labId)
    })
    
    return {
      activeTab,
      starting,
      started,
      submitting,
      lab,
      reportForm,
      reportRules,
      getDifficultyText,
      getDifficultyType,
      getProgressStatus,
      handleStart,
      handleUploadChange,
      submitReport,
      saveDraft
    }
  }
})
</script>

<style scoped>
.lab-detail {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.lab-header {
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  color: #fff;
  padding: 40px 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
}

.lab-info {
  flex: 1;
}

.lab-info h1 {
  font-size: 32px;
  margin: 0 0 16px;
}

.description {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 24px;
}

.meta {
  display: flex;
  gap: 24px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.lab-action {
  text-align: center;
}

.progress {
  margin-top: 16px;
  text-align: left;
}

.progress span {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
}

.lab-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
  background: #fff;
  border-radius: 8px;
  margin-top: -20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.introduction {
  line-height: 1.8;
  color: var(--text-color);
}

.introduction h3 {
  margin: 24px 0 16px;
  font-size: 18px;
}

.introduction ul {
  padding-left: 20px;
  margin: 16px 0;
}

.environment {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.environment h3 {
  margin: 0 0 16px;
  font-size: 16px;
}

.status-list {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color);
}

.status-item:last-child {
  border-bottom: none;
}

.service-name {
  font-size: 14px;
  color: var(--text-color);
}

.report {
  max-width: 800px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .lab-header {
    padding: 24px 0;
  }
  
  .header-content {
    flex-direction: column;
    gap: 24px;
  }
  
  .lab-info h1 {
    font-size: 24px;
  }
  
  .meta {
    flex-wrap: wrap;
    gap: 16px;
  }
  
  .environment {
    grid-template-columns: 1fr;
  }
}
</style> 