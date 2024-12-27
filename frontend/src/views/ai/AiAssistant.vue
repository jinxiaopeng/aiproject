<template>
  <div class="ai-assistant">
    <el-card class="chat-card">
      <template #header>
        <div class="card-header">
          <h3>AI助手</h3>
          <div class="header-actions">
            <el-select v-model="currentMode" placeholder="选择模式" style="width: 150px">
              <el-option label="聊天模式" value="chat" />
              <el-option label="代码分析" value="code_analysis" />
              <el-option label="漏洞解释" value="vulnerability" />
              <el-option label="生成题目" value="challenge" />
              <el-option label="学习规划" value="learning_path" />
            </el-select>
            <el-button type="primary" @click="clearChat">清空对话</el-button>
          </div>
        </div>
      </template>

      <!-- 聊天记录区域 -->
      <div class="chat-messages" ref="messagesRef">
        <div v-for="(msg, index) in messages" :key="index" 
             :class="['message', msg.role === 'user' ? 'user-message' : 'ai-message']">
          <div class="message-content">
            <div class="message-header">
              <span class="role-tag">{{ msg.role === 'user' ? '你' : 'AI助手' }}</span>
              <span class="time">{{ formatTime(msg.timestamp) }}</span>
            </div>
            <div class="message-body" v-html="formatMessage(msg.content)"></div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <el-input
          v-if="currentMode === 'chat'"
          v-model="userInput"
          type="textarea"
          :rows="3"
          placeholder="输入你的问题..."
          @keyup.enter.ctrl="sendMessage"
        />
        <el-input
          v-else-if="currentMode === 'code_analysis'"
          v-model="userInput"
          type="textarea"
          :rows="8"
          placeholder="粘贴要分析的代码..."
        />
        <el-select
          v-else-if="currentMode === 'vulnerability'"
          v-model="userInput"
          placeholder="选择漏洞类型"
          style="width: 100%"
        >
          <el-option label="SQL注入" value="sql_injection" />
          <el-option label="XSS跨站脚本" value="xss" />
          <el-option label="CSRF跨站请求伪造" value="csrf" />
          <el-option label="文件上传漏洞" value="file_upload" />
          <el-option label="命令注入" value="command_injection" />
        </el-select>
        <div v-else-if="currentMode === 'challenge'" class="challenge-inputs">
          <el-select v-model="challengeConfig.difficulty" placeholder="选择难度" style="width: 48%">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
          <el-select v-model="challengeConfig.category" placeholder="选择类型" style="width: 48%">
            <el-option label="Web安全" value="web" />
            <el-option label="系统安全" value="system" />
            <el-option label="密码学" value="crypto" />
          </el-select>
        </div>
        <div v-else-if="currentMode === 'learning_path'" class="learning-inputs">
          <el-select v-model="learningConfig.targetSkill" placeholder="目标技能" style="width: 48%">
            <el-option label="Web渗透测试" value="web_pentest" />
            <el-option label="代码审计" value="code_audit" />
            <el-option label="安全开发" value="secure_dev" />
          </el-select>
          <el-select v-model="learningConfig.currentLevel" placeholder="当前水平" style="width: 48%">
            <el-option label="入门" value="beginner" />
            <el-option label="初级" value="elementary" />
            <el-option label="中级" value="intermediate" />
            <el-option label="高级" value="advanced" />
          </el-select>
        </div>

        <div class="input-actions">
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ submitButtonText }}
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import hljs from 'highlight.js'
import { useAiStore } from '@/stores/ai'
import { useRoute } from 'vue-router'

// 状态
const route = useRoute()
const currentMode = ref(route.path.includes('learning') ? 'chat' : 'code_analysis')
const userInput = ref('')
const messages = ref<Array<{role: string, content: string, timestamp: number}>>([])
const loading = ref(false)
const messagesRef = ref<HTMLElement>()

// 配置
const challengeConfig = ref({
  difficulty: '',
  category: ''
})
const learningConfig = ref({
  targetSkill: '',
  currentLevel: ''
})

// 计算属性
const submitButtonText = computed(() => {
  const buttonTexts: Record<string, string> = {
    chat: '发送',
    code_analysis: '分析代码',
    vulnerability: '获取解释',
    challenge: '生成题目',
    learning_path: '生成路径'
  }
  return buttonTexts[currentMode.value] || '发送'
})

// 方法
const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString()
}

const formatMessage = (content: string) => {
  marked.setOptions({
    highlight: (code: string, lang: string) => {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return code
    }
  })
  return marked(content)
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

const clearChat = () => {
  messages.value = []
  userInput.value = ''
  challengeConfig.value = { difficulty: '', category: '' }
  learningConfig.value = { targetSkill: '', currentLevel: '' }
}

const handleSubmit = async () => {
  if (loading.value) return
  
  try {
    loading.value = true
    const aiStore = useAiStore()
    let response
    
    switch (currentMode.value) {
      case 'chat':
        if (!userInput.value.trim()) return
        messages.value.push({
          role: 'user',
          content: userInput.value,
          timestamp: Date.now()
        })
        response = await aiStore.chat(userInput.value)
        messages.value.push({
          role: 'assistant',
          content: response.response,
          timestamp: Date.now()
        })
        userInput.value = ''
        break
        
      case 'code_analysis':
        if (!userInput.value.trim()) return
        response = await aiStore.analyzeCode(userInput.value, 'auto')
        messages.value.push({
          role: 'assistant',
          content: formatAnalysisResult(response),
          timestamp: Date.now()
        })
        break
        
      case 'vulnerability':
        if (!userInput.value) return
        response = await aiStore.explainVulnerability(userInput.value)
        messages.value.push({
          role: 'assistant',
          content: formatVulnerabilityExplanation(response),
          timestamp: Date.now()
        })
        break
        
      case 'challenge':
        if (!challengeConfig.value.difficulty || !challengeConfig.value.category) {
          ElMessage.warning('请选择难度和类型')
          return
        }
        response = await aiStore.generateChallenge(
          challengeConfig.value.difficulty,
          challengeConfig.value.category,
          []
        )
        messages.value.push({
          role: 'assistant',
          content: formatChallengeResult(response),
          timestamp: Date.now()
        })
        break
        
      case 'learning_path':
        if (!learningConfig.value.targetSkill || !learningConfig.value.currentLevel) {
          ElMessage.warning('请选择目标技能和当前水平')
          return
        }
        response = await aiStore.generateLearningPath(
          learningConfig.value.targetSkill,
          learningConfig.value.currentLevel,
          'medium'
        )
        messages.value.push({
          role: 'assistant',
          content: formatLearningPath(response),
          timestamp: Date.now()
        })
        break
    }
    
    await scrollToBottom()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

// 格式化函数
const formatAnalysisResult = (result: any) => {
  return `### 代码分析结果\n\n` +
    `**风险等级:** ${result.risk_level}\n\n` +
    `#### 发现的漏洞:\n${result.vulnerabilities.map((v: string) => `- ${v}`).join('\n')}\n\n` +
    `#### 改进建议:\n${result.suggestions.map((s: string) => `- ${s}`).join('\n')}`
}

const formatVulnerabilityExplanation = (result: any) => {
  return `### ${result.vulnerability_type} 漏洞说明\n\n` +
    `${result.explanation}\n\n` +
    `#### 示例:\n\`\`\`\n${result.examples.join('\n')}\n\`\`\`\n\n` +
    `#### 防护措施:\n${result.prevention.map((p: string) => `- ${p}`).join('\n')}`
}

const formatChallengeResult = (result: any) => {
  return `### ${result.title}\n\n` +
    `**难度:** ${result.difficulty}\n` +
    `**类型:** ${result.category}\n\n` +
    `${result.description}\n\n` +
    `#### 提示:\n${result.hints.map((h: string) => `- ${h}`).join('\n')}`
}

const formatLearningPath = (result: any) => {
  return `### 个性化学习路径\n\n` +
    `**目标技能:** ${result.target_skill}\n` +
    `**预计用时:** ${result.estimated_time}\n\n` +
    `#### 学习路径:\n${result.path.map((p: any, i: number) => `${i + 1}. ${p}`).join('\n')}\n\n` +
    `#### 推荐资源:\n${result.resources.map((r: any) => `- [${r.name}](${r.url})`).join('\n')}`
}

const sendMessage = () => {
  if (currentMode.value === 'chat') {
    handleSubmit()
  }
}

// 生命周期
onMounted(() => {
  // 添加欢迎消息
  messages.value.push({
    role: 'assistant',
    content: '你好！我是你的AI助手，我可以:\n\n' +
      '- 回答安全相关问题\n' +
      '- 分析代码中的安全问题\n' +
      '- 解释各种漏洞原理\n' +
      '- 生成练习题目\n' +
      '- 规划学习路径\n\n' +
      '请选择一个模式开始吧！',
    timestamp: Date.now()
  })
})
</script>

<style lang="scss" scoped>
.ai-assistant {
  height: 100%;
  padding: 20px;
  
  .chat-card {
    height: calc(100vh - 100px);
    display: flex;
    flex-direction: column;
    
    :deep(.el-card__body) {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 0;
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h3 {
      margin: 0;
    }
    
    .header-actions {
      display: flex;
      gap: 10px;
    }
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    
    .message {
      margin-bottom: 20px;
      display: flex;
      
      &.user-message {
        justify-content: flex-end;
        
        .message-content {
          background: var(--el-color-primary-light-9);
        }
      }
      
      &.ai-message .message-content {
        background: var(--el-bg-color-page);
      }
      
      .message-content {
        max-width: 80%;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        
        .message-header {
          margin-bottom: 8px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          
          .role-tag {
            font-weight: bold;
            color: var(--el-color-primary);
          }
          
          .time {
            font-size: 12px;
            color: var(--el-text-color-secondary);
          }
        }
        
        .message-body {
          line-height: 1.5;
          
          :deep(pre) {
            margin: 10px 0;
            padding: 12px;
            background: var(--el-bg-color);
            border-radius: 4px;
            overflow-x: auto;
          }
          
          :deep(code) {
            font-family: monospace;
            padding: 2px 4px;
            background: var(--el-bg-color);
            border-radius: 4px;
          }
        }
      }
    }
  }
  
  .chat-input {
    padding: 20px;
    border-top: 1px solid var(--el-border-color-lighter);
    
    .challenge-inputs,
    .learning-inputs {
      display: flex;
      justify-content: space-between;
      margin-bottom: 10px;
    }
    
    .input-actions {
      margin-top: 10px;
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style> 