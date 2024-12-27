<template>
  <div class="challenge-card" :class="[`difficulty-${challenge.difficulty}`, { 'completed': challenge.status === 'completed' }]">
    <!-- 卡片头部 -->
    <div class="card-header">
      <div class="difficulty-badge">
        {{ getDifficultyLabel(challenge.difficulty) }}
      </div>
      <div class="points">
        <el-icon><Trophy /></el-icon>
        {{ challenge.points }} pts
      </div>
    </div>

    <!-- 卡片内容 -->
    <div class="card-content">
      <h3 class="title">{{ challenge.title }}</h3>
      <p class="description">{{ challenge.description }}</p>
      
      <!-- 标签组 -->
      <div class="tags">
        <el-tag 
          v-for="tag in challenge.tags" 
          :key="tag"
          size="small"
          effect="dark"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <!-- 卡片底部 -->
    <div class="card-footer">
      <div class="status-progress">
        <div class="status-text" :class="challenge.status">
          {{ getStatusLabel(challenge.status) }}
        </div>
        <el-progress 
          :percentage="challenge.completionRate"
          :status="getProgressStatus(challenge.status)"
          :stroke-width="4"
          :show-text="false"
        />
      </div>
      <el-button 
        type="primary" 
        size="small"
        :icon="challenge.status === 'completed' ? Check : VideoPlay"
        @click="handleStartChallenge"
      >
        {{ getActionLabel(challenge.status) }}
      </el-button>
    </div>
  </div>

  <!-- 靶机启动对话框 -->
  <el-dialog
    v-model="showDialog"
    :title="challenge.title"
    width="800px"
    class="challenge-dialog"
    destroy-on-close
    :modal="true"
    :close-on-click-modal="false"
    :show-close="true"
    append-to-body
  >
    <!-- 标签页 -->
    <div class="dialog-tabs">
      <div 
        v-for="tab in tabs" 
        :key="tab.key"
        class="tab"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </div>
    </div>

    <!-- 标签页内容 -->
    <div class="tab-content">
      <!-- 题目内容 -->
      <div v-if="activeTab === 'problem'" class="problem-content">
        <div class="challenge-info">
          <div class="info-header">
            <div class="difficulty-badge" :class="challenge.difficulty">
              {{ getDifficultyLabel(challenge.difficulty) }}
            </div>
            <div class="points">
              <el-icon><Trophy /></el-icon>
              {{ challenge.points }} pts
            </div>
          </div>
          <div class="tags">
            <el-tag 
              v-for="tag in challenge.tags" 
              :key="tag"
              size="small"
              effect="dark"
            >
              {{ tag }}
            </el-tag>
          </div>
          <div class="description">
            {{ challenge.description }}
          </div>
          <div class="completion-info">
            <div class="completion-rate">
              通过率：{{ Math.round(challenge.completionRate || 50) }}%
            </div>
            <div class="solved-count">
              解出人数：{{ challenge.solvedCount || 5 }}
            </div>
          </div>
        </div>

        <!-- 靶机信息 -->
        <div class="machine-info">
          <div class="info-box">
            <div class="description">
              这是一个模拟的登录系统，存在SQL注入漏洞。你的目标是：
              <br><br>
              • 绕过登录验证
              <br><br>
              • 获取管理员权限
              <br><br>
              • 获取隐藏的flag
            </div>
            <div class="info-item" v-if="machineStatus === 'running'">
              <span class="label">访问地址：</span>
              <a 
                :href="`http://localhost:${machinePort}`" 
                target="_blank" 
                rel="noopener noreferrer" 
                class="value link"
              >
                http://localhost:{{ machinePort }}
              </a>
            </div>
            <div class="info-item" v-if="machineStatus === 'running' && remainingTime">
              <span class="label">剩余时间：</span>
              <span class="value countdown" :class="{ 'warning': isTimeWarning }">
                {{ remainingTime }}
              </span>
            </div>
          </div>
        </div>

        <!-- Flag提交表单 -->
        <div class="flag-submit-box">
          <div class="flag-input-group">
            <el-input
              v-model="flagInput"
              placeholder="Flag"
              type="text"
              :disabled="isSubmitting"
              class="flag-input"
              size="large"
            />
            <el-button 
              type="primary"
              :loading="isSubmitting"
              @click="submitFlag"
              class="submit-button"
              size="large"
            >
              Submit
            </el-button>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-box">
          <el-button
            v-if="machineStatus !== 'running'"
            type="primary"
            size="large"
            :loading="isStarting"
            class="action-button"
            @click="startMachine"
          >
            启动靶场环境
          </el-button>
          <template v-else>
            <el-button
              type="danger"
              size="large"
              class="action-button"
              @click="destroyMachine"
            >
              销毁靶机
            </el-button>
            <el-button
              type="success"
              size="large"
              class="action-button"
              @click="extendTime"
            >
              靶机续期
            </el-button>
          </template>
        </div>
      </div>

      <!-- WriteUp内容 -->
      <div v-else-if="activeTab === 'writeup'" class="writeup-content">
        <div v-if="challenge.status === 'completed'" class="writeup-box">
          <h3>解题思路</h3>
          <div class="writeup-text">
            <div class="section">
              <h4>1. 漏洞分析</h4>
              <p>本题目是一个基础的SQL注入训练，通过分析登录表单的行为，发现存在以下特点：</p>
              <ul>
                <li>登录请求使用POST方法提交用户名和密码</li>
                <li>后端使用字符串拼接构造SQL查询：<code>SELECT * FROM users WHERE username='{username}' AND password='{password}'</code></li>
                <li>错误信息会直接返回到前端，有助于判断注入结果</li>
              </ul>
            </div>
            
            <div class="section">
              <h4>2. 攻击步骤</h4>
              <div class="step">
                <div class="step-title">Step 1: SQL注入点探测</div>
                <div class="step-content">
                  <p>在用户名输入框中尝试注入单引号 <code>'</code>，观察到系统返回SQL语法错误，确认存在SQL注入漏洞。</p>
                </div>
              </div>
              
              <div class="step">
                <div class="step-title">Step 2: 构造绕过语句</div>
                <div class="step-content">
                  <p>使用万能密码绕过登录验证：</p>
                  <pre><code>用户名: admin' OR '1'='1'--
密码: 任意值</code></pre>
                  <p>原理：构造永真条件，使WHERE子句始终返回true，同时使用注释符号--注释掉后面的AND条件</p>
                </div>
              </div>
              
              <div class="step">
                <div class="step-title">Step 3: 获取管理员权限</div>
                <div class="step-content">
                  <p>由于查询会返回users表中的第一条记录，而admin用户通常是第一个创建的用户，所以可以直接获得管理员权限。</p>
                </div>
              </div>
              
              <div class="step">
                <div class="step-title">Step 4: 获取Flag</div>
                <div class="step-content">
                  <p>成功登录后，系统会显示flag。根据数据库结构，flag存储在flag表中：<code>flag{sql_1nj3ct10n_m4st3r_2023}</code></p>
                </div>
              </div>
            </div>
            
            <div class="section">
              <h4>3. 漏洞防御</h4>
              <ul>
                <li>使用参数化查询替代字符串拼接，例如：<code>SELECT * FROM users WHERE username=? AND password=?</code></li>
                <li>对输入进行严格过滤和转义，特别是单引号等特殊字符</li>
                <li>使用安全的密码存储方式，如加盐哈希</li>
                <li>遵循最小权限原则，限制数据库用户权限</li>
                <li>避免在错误信息中泄露技术细节和SQL语句结构</li>
              </ul>
            </div>
            
            <div class="section">
              <h4>4. 延伸思考</h4>
              <p>除了基础的登录绕过，SQL注入还可以进行以下操作：</p>
              <ul>
                <li>使用UNION SELECT语句查询其他表的数据</li>
                <li>通过报错注入获取数据库版本等信息</li>
                <li>利用布尔盲注或时间盲注获取数据</li>
                <li>通过堆叠注入执行多条SQL语句</li>
                <li>配合文件权限，读取或写入系统文件</li>
              </ul>
            </div>
          </div>
        </div>
        <div v-else class="locked-writeup">
          <el-icon><Lock /></el-icon>
          <p>完成挑战后解锁WriteUp</p>
        </div>
      </div>

      <!-- 解题榜内容 -->
      <div v-else-if="activeTab === 'ranking'" class="ranking-content">
        <div class="ranking-list">
          <div class="ranking-header">
            <span class="rank">排名</span>
            <span class="user">用户</span>
            <span class="time">解题时间</span>
          </div>
          <div v-if="rankingList.length" class="ranking-items">
            <div v-for="(item, index) in rankingList" :key="index" class="ranking-item">
              <span class="rank">{{ index + 1 }}</span>
              <span class="user">{{ item.username }}</span>
              <span class="time">{{ item.solvedTime }}</span>
            </div>
          </div>
          <div v-else class="no-data">
            暂无解题记录
          </div>
        </div>
      </div>
    </div>

    <!-- 提示信息 -->
    <div class="tips-box">
      <div class="tip-item">
        <i class="el-icon-info"></i>
        <span>1. 靶机环境会在闲置30���钟后自动关闭</span>
      </div>
      <div class="tip-item">
        <i class="el-icon-warning"></i>
        <span>2. 请勿进行非预期操作，违规可能导致账号封禁</span>
      </div>
      <div class="tip-item">
        <i class="el-icon-question"></i>
        <span>3. 遇到问题请及时在讨论区反馈</span>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onUnmounted, computed } from 'vue'
import { Trophy, VideoPlay, Check, Lock } from '@element-plus/icons-vue/dist/index'
import { ElMessage } from 'element-plus'
import { submitFlag as submitFlagApi } from '@/api/challenge'

interface Challenge {
  id: number
  title: string
  description: string
  difficulty: 'beginner' | 'easy' | 'medium' | 'hard' | 'expert'
  points: number
  status: 'not_started' | 'in_progress' | 'completed'
  completionRate: number
  solvedCount: number
  totalAttempts: number
  tags: string[]
  writeup?: string
}

const props = defineProps<{
  challenge: Challenge
}>()

const emit = defineEmits<{
  (e: 'status-change', challengeId: number, status: Challenge['status']): void
  (e: 'challenge-complete', challengeId: number): void
  (e: 'update-stats', challengeId: number, solvedCount: number, totalAttempts: number): void
}>()

// 靶机状态
const showDialog = ref(false)
const machineStatus = ref('stopped')
const machinePort = ref<number | null>(null)
const remainingTime = ref<string | null>(null)
const isStarting = ref(false)
const timerInterval = ref<number | null>(null)

// 添加 flag 提交相关的状态
const showFlagDialog = ref(false)
const flagInput = ref('')
const isSubmitting = ref(false)

// 标签页配置
const tabs = [
  { key: 'problem', label: '题目' },
  { key: 'writeup', label: 'WriteUp' },
  { key: 'ranking', label: '解题榜' }
]
const activeTab = ref('problem')

// 模拟解题榜数据
const rankingList = ref([
  { username: 'user1', solvedTime: '2024-01-20 10:30:45' },
  { username: 'user2', solvedTime: '2024-01-20 11:15:22' },
  { username: 'user3', solvedTime: '2024-01-20 12:45:10' }
])

const getDifficultyLabel = (difficulty: string) => {
  const labels = {
    beginner: '入门',
    easy: '简单',
    medium: '中等',
    hard: '困难',
    expert: '专家'
  }
  return labels[difficulty] || difficulty
}

const getStatusLabel = (status: string) => {
  const labels = {
    not_started: '未开始',
    in_progress: '进行中',
    completed: '已完成'
  }
  return labels[status] || status
}

const getProgressStatus = (status: string) => {
  const statusMap = {
    not_started: '',
    in_progress: 'warning',
    completed: 'success'
  }
  return statusMap[status] || ''
}

const getActionLabel = (status: string) => {
  const labels = {
    not_started: '开始挑战',
    in_progress: '继续挑战',
    completed: '查看详情'
  }
  return labels[status] || '开始挑战'
}

// 获取靶机状态标签
const getMachineStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    stopped: '未启动',
    starting: '启动中',
    running: '运行中',
    error: '异常'
  }
  return labels[status] || status
}

// 处理开始挑战
const handleStartChallenge = (e: Event) => {
  e.stopPropagation()
  // 显示靶机信息对话框
  showDialog.value = true
}

// 访问靶机
const accessMachine = () => {
  if (machinePort.value) {
    window.open(`http://localhost:${machinePort.value}`, '_blank')
  }
}

// 格式化时间
const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 开始倒计时
const startTimer = (initialSeconds: number = 1800) => { // 默认30分钟
  let seconds = initialSeconds
  remainingTime.value = formatTime(seconds)
  
  // 清除之前的定时器
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  
  timerInterval.value = window.setInterval(() => {
    seconds--
    if (seconds <= 0) {
      clearInterval(timerInterval.value!)
      destroyMachine()
      ElMessage.warning('靶机环境已自动关闭')
      return
    }
    remainingTime.value = formatTime(seconds)
    
    // 在剩余5分钟时发出警告
    if (seconds === 300) {
      ElMessage.warning('靶机环境将在5分钟后自动关闭')
    }
  }, 1000)
}

// 停止倒计时
const stopTimer = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
  remainingTime.value = null
}

// 启动靶机
const startMachine = async () => {
  isStarting.value = true
  try {
    ElMessage.info('正在启动靶场环境...')
    
    // 调用后端API启动Docker环境
    const response = await fetch(`http://localhost:8000/api/challenges/${props.challenge.id}/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('启动靶场失败')
    }
    
    const data = await response.json()
    if (!data.success) {
      throw new Error(data.message || '启动靶场失败')
    }
    
    // 根据不同的挑战ID设置不同的端口
    if (props.challenge.id === 1) {
      // 基础SQL注入挑战
      machinePort.value = 8081
    } else if (props.challenge.id === 2) {
      // 进阶SQL注入挑战
      machinePort.value = 8082
    } else {
      machinePort.value = 8080 + props.challenge.id
    }

    machineStatus.value = 'running'
    startTimer() // 启动倒计时
    emit('status-change', props.challenge.id, 'in_progress')
    
    if (props.challenge.id === 1) {
      ElMessage.success('基础SQL注入靶场环境已启动，请尝试绕过登录验证')
    } else if (props.challenge.id === 2) {
      ElMessage.success('进阶SQL注入靶场环境已启动，请尝试绕过密码哈希并获取管理员权限')
    }
    
  } catch (error: any) {
    ElMessage.error('启动靶场环境失败：' + error.message)
    console.error('完整错误:', error)
  } finally {
    isStarting.value = false
  }
}

// 销毁靶机
const destroyMachine = async () => {
  try {
    ElMessage.info('正在停止靶场环境...')
    
    // 调用后端API停止Docker环境
    const response = await fetch(`http://localhost:8000/api/challenges/${props.challenge.id}/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('停止靶场失败')
    }
    
    const data = await response.json()
    if (!data.success) {
      throw new Error(data.message || '停止靶场失败')
    }
    
    machineStatus.value = 'stopped'
    machinePort.value = null
    stopTimer() // 停止倒计时
    ElMessage.success('靶场环境已停止')
  } catch (error: any) {
    ElMessage.error('停止靶场环境失败：' + error.message)
    console.error(error)
  }
}

// 靶机续期
const extendTime = async () => {
  try {
    ElMessage.info('正在续期...')
    await new Promise(resolve => setTimeout(resolve, 1000))
    startTimer(1800) // 重新开始30分钟倒计时
    ElMessage.success('续期成功')
  } catch (error) {
    ElMessage.error('续期失败')
    console.error(error)
  }
}

// 组件卸载时清理定时器
onUnmounted(() => {
  stopTimer()
})

// 添加时间警告状态
const isTimeWarning = computed(() => {
  if (!remainingTime.value) return false
  const [minutes] = remainingTime.value.split(':').map(Number)
  return minutes < 5
})

// 获取推荐题目
const getNextChallenges = (currentChallenge: Challenge): Challenge[] => {
  // 模拟题库数据
  const challengeList: Challenge[] = [
    {
      id: 1,
      title: 'SQL注入基础训练',
      description: '学习SQL注入的基本原理和防御方法',
      difficulty: 'beginner',
      points: 100,
      status: 'not_started',
      completionRate: 50,
      solvedCount: 5,
      totalAttempts: 10,
      tags: ['web安全', 'SQL注入']
    },
    {
      id: 2,
      title: 'SQL注入进阶训练',
      description: '学习高级SQL注入技术和绕过方法',
      difficulty: 'medium',
      points: 200,
      status: 'not_started',
      completionRate: 30,
      solvedCount: 3,
      totalAttempts: 10,
      tags: ['web安全', 'SQL注入', '密码绕过']
    },
    {
      id: 3,
      title: 'XSS跨站脚本攻击',
      description: '学习XSS漏洞的利用与防御',
      difficulty: 'easy',
      points: 150,
      status: 'not_started',
      completionRate: 40,
      solvedCount: 4,
      totalAttempts: 10,
      tags: ['web安全', 'XSS']
    }
  ]
  
  // 根据当前题目筛选推荐
  const recommendations = challengeList.filter(challenge => {
    // 排除当前题目和已完成的题目
    if (challenge.id === currentChallenge.id || challenge.status === 'completed') {
      return false
    }
    
    // 检查难度是否合适
    const difficultyMap = {
      beginner: 1,
      easy: 2,
      medium: 3,
      hard: 4,
      expert: 5
    }
    const currentLevel = difficultyMap[currentChallenge.difficulty]
    const challengeLevel = difficultyMap[challenge.difficulty]
    
    // 只���荐相同或稍难的题目
    return challengeLevel >= currentLevel && challengeLevel <= currentLevel + 1
  })
  
  // 按推荐优先级排序
  return recommendations.sort((a, b) => {
    // 优先推荐相同标签的题目
    const aHasCommonTag = a.tags.some(tag => currentChallenge.tags.includes(tag))
    const bHasCommonTag = b.tags.some(tag => currentChallenge.tags.includes(tag))
    if (aHasCommonTag && !bHasCommonTag) return -1
    if (!aHasCommonTag && bHasCommonTag) return 1
    
    // 其次考虑完成率
    return b.completionRate - a.completionRate
  }).slice(0, 3)
}

// 显示推荐
const showRecommendations = (recommendations: Challenge[]) => {
  const aiAnalysis = `
    <div style="
      margin: 12px 0;
      padding: 20px;
      background: linear-gradient(135deg, rgba(24, 144, 255, 0.05) 0%, rgba(24, 144, 255, 0.02) 100%);
      border: 1px solid rgba(24, 144, 255, 0.1);
      border-radius: 12px;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(10px);
    ">
      <div style="
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at center, rgba(24, 144, 255, 0.1) 0%, transparent 70%);
        opacity: 0.5;
        animation: rotate 20s linear infinite;
      "></div>
      <div style="position: relative;">
        <div style="
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 16px;
        ">
          <div style="
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1890ff 0%, #40a9ff 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 20px rgba(24, 144, 255, 0.3);
          ">
            <i class="el-icon-cpu" style="font-size: 18px; color: #fff;"></i>
          </div>
          <span style="
            font-size: 16px;
            color: #1890ff;
            font-weight: 600;
            text-shadow: 0 0 10px rgba(24, 144, 255, 0.3);
          ">AI 学习路径分析</span>
        </div>
        <div style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
          <div style="
            font-size: 14px;
            margin-bottom: 16px;
            color: rgba(255, 255, 255, 0.7);
          ">基于您的学习轨迹分析，在SQL注入挑战中表现出以下特点：</div>
          <div style="
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 20px;
          ">
            <div style="
              padding: 16px;
              background: rgba(0, 0, 0, 0.2);
              border: 1px solid rgba(24, 144, 255, 0.2);
              border-radius: 8px;
              position: relative;
              overflow: hidden;
            ">
              <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, rgba(24, 144, 255, 0.1) 0%, transparent 100%);
              "></div>
              <div style="position: relative;">
                <div style="
                  font-size: 13px;
                  color: rgba(255, 255, 255, 0.5);
                  margin-bottom: 8px;
                ">解题速度</div>
                <div style="
                  font-size: 24px;
                  color: #1890ff;
                  font-weight: 600;
                  text-shadow: 0 0 10px rgba(24, 144, 255, 0.5);
                ">较快</div>
                <div style="
                  font-size: 12px;
                  color: #67c23a;
                  margin-top: 4px;
                ">超过 75% 的用户</div>
              </div>
            </div>
            <div style="
              padding: 16px;
              background: rgba(0, 0, 0, 0.2);
              border: 1px solid rgba(103, 194, 58, 0.2);
              border-radius: 8px;
              position: relative;
              overflow: hidden;
            ">
              <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, rgba(103, 194, 58, 0.1) 0%, transparent 100%);
              "></div>
              <div style="position: relative;">
                <div style="
                  font-size: 13px;
                  color: rgba(255, 255, 255, 0.5);
                  margin-bottom: 8px;
                ">掌握程度</div>
                <div style="
                  font-size: 24px;
                  color: #67c23a;
                  font-weight: 600;
                  text-shadow: 0 0 10px rgba(103, 194, 58, 0.5);
                ">良好</div>
                <div style="
                  font-size: 12px;
                  color: #67c23a;
                  margin-top: 4px;
                ">已掌握基础知识点</div>
              </div>
            </div>
          </div>
          <div style="
            display: flex;
            flex-direction: column;
            gap: 12px;
          ">
            <div style="
              font-size: 14px;
              color: rgba(255, 255, 255, 0.9);
              margin-bottom: 4px;
            ">技能分析：</div>
            <div style="
              background: rgba(0, 0, 0, 0.2);
              border: 1px solid rgba(24, 144, 255, 0.2);
              border-radius: 8px;
              padding: 16px;
            ">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="color: rgba(255, 255, 255, 0.5); font-size: 13px;">SQL语法理解</span>
                <div style="
                  flex: 1;
                  height: 8px;
                  background: rgba(255, 255, 255, 0.1);
                  border-radius: 4px;
                  overflow: hidden;
                  position: relative;
                ">
                  <div style="
                    width: 85%;
                    height: 100%;
                    background: linear-gradient(90deg, #1890ff, #40a9ff);
                    border-radius: 4px;
                    position: relative;
                    overflow: hidden;
                  ">
                    <div style="
                      position: absolute;
                      top: 0;
                      left: 0;
                      width: 200%;
                      height: 100%;
                      background: linear-gradient(90deg,
                        transparent 0%,
                        rgba(255, 255, 255, 0.3) 50%,
                        transparent 100%
                      );
                      animation: shine 2s linear infinite;
                    "></div>
                  </div>
                </div>
                <span style="color: #1890ff; font-size: 14px; font-weight: 500;">85%</span>
              </div>
              <div style="display: flex; align-items: center; gap: 12px;">
                <span style="color: rgba(255, 255, 255, 0.5); font-size: 13px;">注入技巧</span>
                <div style="
                  flex: 1;
                  height: 8px;
                  background: rgba(255, 255, 255, 0.1);
                  border-radius: 4px;
                  overflow: hidden;
                  position: relative;
                ">
                  <div style="
                    width: 70%;
                    height: 100%;
                    background: linear-gradient(90deg, #1890ff, #40a9ff);
                    border-radius: 4px;
                    position: relative;
                    overflow: hidden;
                  ">
                    <div style="
                      position: absolute;
                      top: 0;
                      left: 0;
                      width: 200%;
                      height: 100%;
                      background: linear-gradient(90deg,
                        transparent 0%,
                        rgba(255, 255, 255, 0.3) 50%,
                        transparent 100%
                      );
                      animation: shine 2s linear infinite;
                    "></div>
                  </div>
                </div>
                <span style="color: #1890ff; font-size: 14px; font-weight: 500;">70%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `

  const recommendationList = recommendations.map(challenge => `
    <div class="recommendation-item" style="
      margin-top: 16px;
      padding: 20px;
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(24, 144, 255, 0.2);
      border-radius: 12px;
      position: relative;
      overflow: hidden;
      transition: all 0.3s;
      cursor: pointer;
    ">
      <div style="
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(24, 144, 255, 0.1) 0%, transparent 100%);
      "></div>
      <div style="
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, ${getDifficultyColor(challenge.difficulty)}, ${getDifficultyColor(challenge.difficulty)}88);
      "></div>
      <div style="
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
      ">
        <div style="flex: 1; margin-left: 12px;">
          <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
          ">
            <span style="
              font-size: 18px;
              font-weight: 600;
              color: rgba(255, 255, 255, 0.9);
              text-shadow: 0 0 10px rgba(24, 144, 255, 0.3);
            ">${challenge.title}</span>
            <span style="
              padding: 4px 12px;
              border-radius: 12px;
              font-size: 12px;
              background: ${getDifficultyColor(challenge.difficulty)};
              color: #fff;
              box-shadow: 0 0 10px ${getDifficultyColor(challenge.difficulty)}88;
            ">${getDifficultyLabel(challenge.difficulty)}</span>
          </div>
          <div style="
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 16px;
            line-height: 1.6;
          ">${challenge.description}</div>
          <div style="
            display: flex;
            align-items: center;
            gap: 24px;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.5);
          ">
            <span style="display: flex; align-items: center; gap: 6px;">
              <i class="el-icon-trophy" style="
                font-size: 16px;
                color: #ffd700;
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
              "></i>
              <span style="color: rgba(255, 255, 255, 0.9);">${challenge.points}</span> pts
            </span>
            <span style="display: flex; align-items: center; gap: 6px;">
              <i class="el-icon-data-line" style="
                font-size: 16px;
                color: #67c23a;
                text-shadow: 0 0 10px rgba(103, 194, 58, 0.5);
              "></i>
              通过率: <span style="color: rgba(255, 255, 255, 0.9);">${Math.round(challenge.completionRate)}%</span>
            </span>
            <span style="
              display: flex;
              align-items: center;
              gap: 6px;
              padding: 4px 12px;
              background: rgba(103, 194, 58, 0.1);
              border: 1px solid rgba(103, 194, 58, 0.2);
              border-radius: 12px;
              color: #67c23a;
            ">
              <i class="el-icon-connection"></i>
              学习路径匹配度: ${Math.round(Math.random() * 20 + 80)}%
            </span>
          </div>
        </div>
        <button style="
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          background: linear-gradient(135deg, #1890ff 0%, #40a9ff 100%);
          color: #fff;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s;
          display: flex;
          align-items: center;
          gap: 8px;
          box-shadow: 0 0 20px rgba(24, 144, 255, 0.3);
          text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        " onmouseover="this.style.transform='translateY(-2px)'"
          onmouseout="this.style.transform='translateY(0)'">
          开始挑战
          <i class="el-icon-right"></i>
        </button>
      </div>
    </div>
  `).join('')

  ElMessage({
    type: 'success',
    dangerouslyUseHTMLString: true,
    message: `
      <div style="
        width: 600px;
        background: #1e232d;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.4);
      ">
        <div style="
          padding: 24px;
          background: linear-gradient(135deg, rgba(103, 194, 58, 0.2) 0%, rgba(103, 194, 58, 0.1) 100%);
          display: flex;
          align-items: center;
          gap: 20px;
          position: relative;
          overflow: hidden;
        ">
          <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(103, 194, 58, 0.2) 0%, transparent 70%);
            opacity: 0.5;
            animation: rotate 20s linear infinite;
          "></div>
          <div style="
            position: relative;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(103, 194, 58, 0.4);
          ">
            <i class="el-icon-success" style="
              color: #fff;
              font-size: 32px;
              text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            "></i>
          </div>
          <div style="position: relative;">
            <div style="
              font-size: 24px;
              font-weight: 600;
              color: #67c23a;
              margin-bottom: 4px;
              text-shadow: 0 0 10px rgba(103, 194, 58, 0.3);
            ">恭喜完成挑战！</div>
            <div style="
              font-size: 16px;
              color: rgba(255, 255, 255, 0.9);
            ">获得 ${props.challenge.points} 积分</div>
          </div>
        </div>
        <div style="padding: 24px;">
          ${aiAnalysis}
          <div style="
            margin: 24px 0 16px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
          ">
            <i class="el-icon-magic-stick" style="
              color: #1890ff;
              font-size: 24px;
              text-shadow: 0 0 10px rgba(24, 144, 255, 0.5);
            "></i>
            <span style="text-shadow: 0 0 10px rgba(24, 144, 255, 0.3);">
              基于AI分析的个性化推荐
            </span>
          </div>
          ${recommendationList}
        </div>
      </div>
    `,
    duration: 0,
    showClose: true,
    offset: 100,
    customClass: 'dark-message'
  })
}

// 获取难度对应的颜色
const getDifficultyColor = (difficulty: string) => {
  const colors = {
    beginner: '#909399',
    easy: '#67c23a',
    medium: '#e6a23c',
    hard: '#f56c6c',
    expert: '#800080'
  }
  return colors[difficulty] || '#909399'
}

// 修改提交flag的函数
const submitFlag = async () => {
  if (!flagInput.value) {
    ElMessage.warning('请输入flag')
    return
  }
  
  isSubmitting.value = true
  try {
    // 前端验证flag
    const correctFlag = 'flag{sql_1nj3ct10n_m4st3r_2023}'
    const isCorrect = flagInput.value.trim() === correctFlag
    
    if (isCorrect) {
      // 获取并显示推荐
      const recommendations = getNextChallenges(props.challenge)
      showRecommendations(recommendations)
      
      // 更新状态
      emit('challenge-complete', props.challenge.id)
      emit('status-change', props.challenge.id, 'completed')
      showDialog.value = false
    } else {
      ElMessage.error('flag不正确，请重试')
    }
  } catch (error: any) {
    ElMessage.error('提交失败：' + error.message)
    console.error('提交flag失败:', error)
  } finally {
    isSubmitting.value = false
  }
}

// 添加全局样式
const style = document.createElement('style')
style.textContent = `
  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  @keyframes shine {
    from { transform: translateX(-100%); }
    to { transform: translateX(100%); }
  }
  
  .dark-message {
    --el-message-bg-color: transparent !important;
    --el-message-border-color: transparent !important;
    --el-message-padding: 0 !important;
    --el-message-min-width: auto !important;
  }
  
  .dark-message .el-message__content {
    padding: 0 !important;
  }
  
  .dark-message .el-message__closeBtn {
    position: absolute !important;
    top: 16px !important;
    right: 16px !important;
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background: rgba(255, 255, 255, 0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 16px !important;
    transition: all 0.3s !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    
    &:hover {
      background: rgba(255, 255, 255, 0.15) !important;
      color: rgba(255, 255, 255, 0.9) !important;
      transform: rotate(90deg) !important;
      border-color: rgba(255, 255, 255, 0.2) !important;
      box-shadow: 0 0 20px rgba(255, 255, 255, 0.1) !important;
    }
  }
`
document.head.appendChild(style)
</script>

<style scoped lang="scss">
.challenge-card {
  background: rgba(30, 35, 45, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px;
  height: 180px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    border-color: var(--el-color-primary);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .title {
    color: #ffffff;
  }

  .description {
    color: rgba(255, 255, 255, 0.7);
  }

  // 难��式
  &.difficulty-beginner { --difficulty-color: var(--el-color-info); }
  &.difficulty-easy { --difficulty-color: var(--el-color-success); }
  &.difficulty-medium { --difficulty-color: var(--el-color-warning); }
  &.difficulty-hard { --difficulty-color: var(--el-color-danger); }
  &.difficulty-expert { --difficulty-color: #800080; }

  // 完成状态
  &.completed {
    border-color: var(--el-color-success);
    .card-header .points {
      color: var(--el-color-success);
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;

    .difficulty-badge {
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 12px;
      color: var(--difficulty-color);
      border: 1px solid var(--difficulty-color);
    }

    .points {
      display: flex;
      align-items: center;
      gap: 4px;
      color: var(--primary-color);
      font-size: 13px;

      .el-icon {
        font-size: 14px;
      }
    }
  }

  .card-content {
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 6px;

    .title {
      margin: 0;
      font-size: 15px;
      font-weight: 600;
      color: var(--text-color);
      line-height: 1.3;
    }

    .description {
      margin: 0;
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.3;
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: auto;
      padding-top: 6px;

      .el-tag {
        --el-tag-bg-color: rgba(255, 255, 255, 0.05);
        --el-tag-border-color: var(--border-color);
        --el-tag-hover-color: var(--primary-color);
        transform: scale(0.9);
      }
    }
  }

  .card-footer {
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .status-progress {
      flex: 1;
      margin-right: 8px;

      .status-text {
        font-size: 11px;
        margin-bottom: 3px;
        
        &.not_started { color: var(--text-secondary); }
        &.in_progress { color: var(--el-color-warning); }
        &.completed { color: var(--el-color-success); }
      }

      :deep(.el-progress-bar__outer) {
        height: 3px !important;
        background-color: rgba(255, 255, 255, 0.05);
      }
    }

    .el-button {
      padding: 4px 8px;
      font-size: 12px;
      --el-button-bg-color: var(--primary-color);
      --el-button-border-color: var(--primary-color);
      --el-button-hover-bg-color: var(--primary-hover);
      --el-button-hover-border-color: var(--primary-hover);
    }
  }
}

// 列表视图样式
:deep(.list-view) .challenge-card {
  height: auto;
  flex-direction: row;
  gap: 16px;
  padding: 12px 16px;

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    margin-bottom: 0;
    width: 90px;
  }

  .card-content {
    flex: 1;
    min-width: 0;

    .description {
      -webkit-line-clamp: 1;
    }

    .tags {
      margin-top: 6px;
    }
  }

  .card-footer {
    width: 180px;
    margin-top: 0;
    flex-direction: column;
    gap: 8px;

    .status-progress {
      margin-right: 0;
      width: 100%;
    }

    .el-button {
      width: 100%;
    }
  }
}

.challenge-dialog {
  :deep(.el-dialog) {
    background: #ffffff;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-dialog__header) {
    padding: 16px 24px;
    margin: 0;
    border-bottom: 1px solid #eee;
    background: #ffffff;
  }

  :deep(.el-dialog__body) {
    padding: 0;
  }

  .dialog-tabs {
    display: flex;
    border-bottom: 1px solid #eee;
    padding: 0 24px;
    background: #f5f7fa;

    .tab {
      padding: 12px 24px;
      cursor: pointer;
      color: #666666;
      position: relative;
      transition: all 0.3s ease;

      &:hover {
        color: #1890ff;
      }

      &.active {
        color: #1890ff;
        font-weight: 500;
        background: #ffffff;

        &::after {
          content: '';
          position: absolute;
          bottom: -1px;
          left: 0;
          right: 0;
          height: 2px;
          background: #1890ff;
        }
      }
    }
  }

  .machine-info {
    padding: 24px;
    border-bottom: 1px solid #eee;

    .info-box {
      background: #ffffff;
      border: 1px solid #e4e7ed;
      border-radius: 4px;
      padding: 16px;

      .description {
        font-size: 14px;
        line-height: 1.8;
        color: #333333;
        margin-bottom: 16px;
      }

      .info-item {
        display: flex;
        align-items: center;
        font-size: 14px;

        .label {
          width: 100px;
          color: #666666;
        }

        .value {
          color: #333333;

          &.link {
            color: #1890ff;
            cursor: pointer;
            text-decoration: none;

            &:hover {
              color: #40a9ff;
            }
          }
        }
      }
    }
  }

  .action-box {
    padding: 24px;
    display: flex;
    justify-content: center;
    gap: 16px;

    .action-button {
      min-width: 120px;
    }
  }

  .tips-box {
    padding: 0 24px 24px;

    .tip-item {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #666;
      font-size: 13px;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      i {
        font-size: 14px;
        color: #1890ff;
      }
    }
  }
}

.flag-submit-box {
  padding: 24px;
  border-bottom: 1px solid #eee;

  .flag-input-group {
    display: flex;
    gap: 12px;
    align-items: center;

    .flag-input {
      flex: 1;
      
      :deep(.el-input__wrapper) {
        background-color: #fff;
        border: 1px solid #dcdfe6;
        
        &:focus {
          border-color: var(--el-color-primary);
          box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
        }
      }
      
      :deep(.el-input__inner) {
        font-size: 16px;
        color: #333;
        
        &::placeholder {
          color: #999;
        }
      }
    }

    .submit-button {
      width: 120px;
      height: 48px;
      font-size: 16px;
      border-radius: 4px;
      background: #1890ff;
      border-color: #1890ff;
      
      &:hover {
        background: #40a9ff;
        border-color: #40a9ff;
      }
      
      &:active {
        background: #096dd9;
        border-color: #096dd9;
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.tab-content {
  min-height: 300px;
}

.problem-content {
  .challenge-info {
    padding: 24px;
    border-bottom: 1px solid #eee;

    .info-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .difficulty-badge {
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 13px;
      
      &.beginner { color: var(--el-color-info); border: 1px solid var(--el-color-info); }
      &.easy { color: var(--el-color-success); border: 1px solid var(--el-color-success); }
      &.medium { color: var(--el-color-warning); border: 1px solid var(--el-color-warning); }
      &.hard { color: var(--el-color-danger); border: 1px solid var(--el-color-danger); }
      &.expert { color: #800080; border: 1px solid #800080; }
    }

    .points {
      display: flex;
      align-items: center;
      gap: 4px;
      color: #1890ff;
      font-size: 14px;
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }

    .description {
      font-size: 14px;
      line-height: 1.6;
      color: #333;
      margin-bottom: 16px;
    }

    .completion-info {
      display: flex;
      gap: 24px;
      color: #666;
      font-size: 13px;
    }
  }
}

.writeup-content {
  padding: 24px;
  color: #f0f0f0;
  background: #1e232d;

  .writeup-box {
    h3 {
      margin: 0 0 24px 0;
      font-size: 20px;
      color: #fff;
      font-weight: 600;
    }

    h4 {
      margin: 24px 0 16px;
      font-size: 16px;
      color: #40a9ff;
      font-weight: 500;
    }

    .writeup-text {
      font-size: 14px;
      line-height: 1.6;
      color: rgba(255, 255, 255, 0.9);

      .section {
        margin-bottom: 24px;

        &:last-child {
          margin-bottom: 0;
        }

        ul {
          margin: 12px 0;
          padding-left: 20px;
          
          li {
            margin-bottom: 8px;
            color: rgba(255, 255, 255, 0.8);
            
            &::marker {
              color: #40a9ff;
            }
          }
        }
      }

      .step {
        margin-bottom: 20px;
        padding: 16px;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(64, 169, 255, 0.1);
        border-radius: 8px;

        .step-title {
          font-weight: 500;
          color: #40a9ff;
          margin-bottom: 12px;
        }

        .step-content {
          color: rgba(255, 255, 255, 0.8);

          pre {
            margin: 12px 0;
            padding: 12px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 4px;
            font-family: monospace;
            overflow-x: auto;
            
            code {
              color: #67c23a;
            }
          }
        }
      }
    }
  }

  .locked-writeup {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 48px 0;
    color: rgba(255, 255, 255, 0.4);
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;

    .el-icon {
      font-size: 32px;
      margin-bottom: 16px;
    }

    p {
      font-size: 14px;
    }
  }
}

.ranking-content {
  padding: 24px;
  background: #ffffff;

  .ranking-list {
    .ranking-header {
      display: grid;
      grid-template-columns: 80px 1fr 160px;
      padding: 12px 16px;
      background: #f5f7fa;
      border-radius: 4px;
      font-weight: 500;
      color: #333333;
      font-size: 14px;
    }

    .ranking-items {
      .ranking-item {
        display: grid;
        grid-template-columns: 80px 1fr 160px;
        padding: 12px 16px;
        border-bottom: 1px solid #eee;
        font-size: 14px;
        color: #666666;

        &:last-child {
          border-bottom: none;
        }

        .rank {
          color: #333333;
          font-weight: 500;
        }

        .time {
          color: #999999;
        }
      }
    }

    .no-data {
      padding: 48px 0;
      text-align: center;
      color: #999999;
      font-size: 14px;
    }
  }
}

.machine-info {
  .info-box {
    .info-item {
      .countdown {
        font-family: monospace;
        font-size: 16px;
        font-weight: 500;
        
        &.warning {
          color: var(--el-color-danger);
          animation: blink 1s infinite;
        }
      }
    }
  }
}

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

// 修改标签样式
.el-tag {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.8);
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.15);
  }
}

// 修改进度条样式
:deep(.el-progress-bar__outer) {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

// 状态文字颜色
.status-text {
  &.not_started { color: rgba(255, 255, 255, 0.4); }
  &.in_progress { color: #e6a23c; }
  &.completed { color: #67c23a; }
}

// 对话框标签页
.dialog-tabs {
  background: #1e232d;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .tab {
    color: rgba(255, 255, 255, 0.6);

    &.active {
      color: var(--el-color-primary);
    }
  }
}
</style> 