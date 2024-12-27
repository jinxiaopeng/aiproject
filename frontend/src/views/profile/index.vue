<template>
  <div class="profile-container">
    <div class="main-content">
      <!-- 个人信息卡片 -->
      <el-card class="profile-card">
        <div class="profile-header">
          <div class="avatar-section">
            <el-avatar :size="100" :src="userInfo?.avatar || defaultAvatar" />
            <div class="avatar-mask">
              <el-upload
                class="avatar-uploader"
                action="/api/profile/avatar"
                :show-file-list="false"
                :before-upload="beforeAvatarUpload"
                :http-request="handleAvatarUpload"
              >
                <el-icon><CameraIcon /></el-icon>
                <span>更换头像</span>
              </el-upload>
            </div>
          </div>
          
          <div class="user-info">
            <h2>{{ userInfo?.username }}</h2>
            <p class="user-email">{{ userInfo?.email }}</p>
            
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-value">{{ stats.studyDays }}</span>
                <span class="stat-label">学习天数</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ stats.completedCourses }}</span>
                <span class="stat-label">完成课程</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ stats.points }}</span>
                <span class="stat-label">积分</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- AI学习分析 -->
      <AILearningAnalysis />

      <!-- 学习可视化 -->
      <LearningVisualization />
    </div>

    <!-- 安全设置卡片 -->
    <el-card class="security-card">
      <template #header>
        <div class="card-header">
          <h3>安全设置</h3>
        </div>
      </template>
      
      <div class="security-content">
        <div class="security-list">
          <div class="security-item">
            <div class="security-info">
              <el-icon><LockIcon /></el-icon>
              <div class="security-text">
                <h4>修改密码</h4>
                <p>定期更换密码可以提高账号安全性</p>
              </div>
            </div>
            <el-button link type="primary" @click="passwordDialogVisible = true">修改</el-button>
          </div>
          
          <div class="security-item">
            <div class="security-info">
              <el-icon><MessageIcon /></el-icon>
              <div class="security-text">
                <h4>邮箱验证</h4>
                <p>验证邮箱可以提高账号安全性</p>
              </div>
            </div>
            <el-button 
              link
              type="primary" 
              :disabled="!!userInfo?.email"
            >
              {{ userInfo?.email ? '已验证' : '去验证' }}
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="修改密码"
      width="400px"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="原密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="submitting"
            @click="handleChangePassword"
          >
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { EChartsOption } from 'echarts'
import { graphic } from 'echarts/core'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, RadarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  MarkPointComponent,
  MarkLineComponent
} from 'echarts/components'
import {
  getProfile,
  updateProfile,
  uploadAvatar,
  changePassword,
  sendEmailCode,
  changeEmail
} from '@/api/profile'
import dayjs from 'dayjs'
import LearningVisualization from './components/LearningVisualization.vue'
import AILearningAnalysis from '@/components/analysis/AILearningAnalysis.vue'

// 注册必需的 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  RadarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  MarkPointComponent,
  MarkLineComponent
])

const authStore = useAuthStore()
const userInfo = computed(() => authStore.userInfo)
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

// 统计数据
const stats = ref({
  studyDays: 30,
  completedCourses: 5,
  points: 1200
})

// 时间范围选择
const timeRange = ref('week')

// 最近活动
const activities = ref([
  {
    id: 1,
    content: '完成了 Web安全基础 课程的学习',
    time: '2023-12-04 15:30',
    type: 'success'
  },
  {
    id: 2,
    content: '获得了 XSS攻防 技能徽章',
    time: '2023-12-03 14:20',
    type: 'warning'
  },
  {
    id: 3,
    content: '参与了 SQL注入进阶 实验',
    time: '2023-12-02 10:15',
    type: 'primary'
  }
])

// 头像上传
const beforeAvatarUpload = (file: File) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

const handleAvatarUpload = async (options: any) => {
  try {
    const result = await uploadAvatar(options.file)
    authStore.updateUserInfo({ avatar: result.url })
    ElMessage.success('头像上传成功')
  } catch (error) {
    ElMessage.error('头像上传失败')
  }
}

// 修改密码
const passwordDialogVisible = ref(false)
const passwordFormRef = ref<FormInstance>()
const submitting = ref(false)

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validatePass = (rule: any, value: string, callback: (error?: Error) => void) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (passwordForm.value.confirmPassword !== '') {
      if (passwordFormRef.value) {
        passwordFormRef.value.validateField('confirmPassword')
      }
    }
    callback()
  }
}

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.value.newPassword) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const passwordRules: FormRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const handleChangePassword = () => {
  passwordDialogVisible.value = true
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}

const submitPasswordChange = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    submitting.value = true
    await changePassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
    ElMessage.success('密码修改成功')
    passwordDialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '密码修改失败')
  } finally {
    submitting.value = false
  }
}

// 修改邮箱
const emailDialogVisible = ref(false)
const emailFormRef = ref<FormInstance>()
const countdown = ref(0)

const emailForm = ref({
  email: '',
  code: ''
})

const emailRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码长度为6位', trigger: 'blur' }
  ]
}

const handleChangeEmail = () => {
  emailDialogVisible.value = true
  emailForm.value = {
    email: '',
    code: ''
  }
}

const sendVerificationCode = async () => {
  try {
    await emailFormRef.value?.validateField('email')
    await sendEmailCode(emailForm.value.email)
    ElMessage.success('验证码已发送')
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '发送验证码失败')
  }
}

const submitEmailChange = async () => {
  if (!emailFormRef.value) return
  
  try {
    await emailFormRef.value.validate()
    submitting.value = true
    await changeEmail(emailForm.value.email, emailForm.value.code)
    authStore.updateUserInfo({ email: emailForm.value.email })
    ElMessage.success('邮箱修改成功')
    emailDialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '邮箱修改失败')
  } finally {
    submitting.value = false
  }
}

// 模拟学习数据
const studyData = {
  weeklyData: {
    dates: ['12-05', '12-06', '12-07', '12-08', '12-09', '12-10', '12-11'],
    hours: [2.5, 1.5, 3, 4, 2, 3.5, 2]
  },
  monthlyData: {
    dates: Array.from({ length: 30 }, (_, i) => `12-${String(i + 1).padStart(2, '0')}`),
    hours: Array.from({ length: 30 }, () => Math.random() * 4 + 1)
  },
  yearlyData: {
    dates: Array.from({ length: 12 }, (_, i) => `2023-${String(i + 1).padStart(2, '0')}`),
    hours: Array.from({ length: 12 }, () => Math.floor(Math.random() * 60 + 30))
  }
}

// 模拟技能数据
const skillsData = [
  { name: 'Web安全', value: 85 },
  { name: '系统安全', value: 70 },
  { name: '网络安全', value: 75 },
  { name: '密码学', value: 60 },
  { name: '安全开发', value: 80 },
  { name: '渗透测试', value: 65 }
]

// 学习进度图表配置
const progressChartOption = computed<EChartsOption>(() => {
  const currentData = studyData[`${timeRange.value}Data` as keyof typeof studyData]
  
  return {
    title: {
      text: '学习时长统计',
      textStyle: {
        color: '#8892b0',
        fontSize: 14
      },
      top: 0,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const data = params[0]
        return `${data.name}<br/>学习时长: ${data.value} 小时`
      }
    },
    grid: {
      top: 50,
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: currentData.dates,
      axisLabel: {
        color: '#8892b0',
        interval: timeRange.value === 'year' ? 0 : 'auto',
        rotate: timeRange.value === 'month' ? 45 : 0
      },
      axisLine: {
        lineStyle: {
          color: '#8892b0'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '学习时长(小时)',
      nameTextStyle: {
        color: '#8892b0',
        padding: [0, 30, 0, 0]
      },
      axisLabel: {
        color: '#8892b0',
        formatter: '{value}'
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: '#8892b0'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(136, 146, 176, 0.2)'
        }
      }
    },
    series: [
      {
        name: '学习时长',
        type: 'line',
        smooth: true,
        data: currentData.hours,
        symbolSize: 8,
        symbol: 'circle',
        showSymbol: true,
        itemStyle: {
          color: '#64ffda',
          borderWidth: 2,
          borderColor: '#64ffda'
        },
        emphasis: {
          scale: true,
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(100, 255, 218, 0.5)'
          }
        },
        lineStyle: {
          width: 3,
          color: '#64ffda'
        },
        areaStyle: {
          color: new graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(100, 255, 218, 0.3)' },
            { offset: 1, color: 'rgba(100, 255, 218, 0.05)' }
          ])
        }
      }
    ]
  }
})

// 技能雷达图配置
const radarChartOption = computed<EChartsOption>(() => {
  return {
    tooltip: {
      trigger: 'item'
    },
    radar: {
      shape: 'circle',
      center: ['50%', '50%'],
      radius: '70%',
      indicator: skillsData.map(skill => ({
        name: skill.name,
        max: 100
      })),
      splitArea: {
        areaStyle: {
          color: ['rgba(100, 255, 218, 0.05)', 'rgba(100, 255, 218, 0.1)']
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(136, 146, 176, 0.3)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(136, 146, 176, 0.3)'
        }
      },
      nameTextStyle: {
        color: '#8892b0',
        padding: [3, 5]
      }
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: skillsData.map(skill => skill.value),
            name: '技能掌握度',
            symbolSize: 6,
            itemStyle: {
              color: '#64ffda'
            },
            areaStyle: {
              color: new graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(100, 255, 218, 0.3)' },
                { offset: 1, color: 'rgba(100, 255, 218, 0.05)' }
              ])
            },
            lineStyle: {
              width: 2,
              color: '#64ffda'
            }
          }
        ]
      }
    ]
  }
})

onMounted(() => {
  // 不再需要调用 initCharts
})

const router = useRouter()

// 模拟最近学习的课程数据
const recentCourses = ref([
  {
    id: 3,
    title: 'Web安全基础入门',
    description: '学习Web安全的基础知识和实践技能',
    cover_url: '/images/courses/web-security.jpg',
    progress: 30,
    last_learn_time: '2023-12-11 15:30:00',
    current_chapter: '第1章 Web安全概述'
  },
  {
    id: 4,
    title: '网络攻防实战',
    description: '网络攻防技术战演练',
    cover_url: '/images/courses/network-security.jpg',
    progress: 60,
    last_learn_time: '2023-12-10 14:20:00',
    current_chapter: '第3章 网络渗透测试'
  }
])

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 继续学习
const continueLearning = (course: any) => {
  router.push(`/courses/${course.id}/learn/1`)
}

// 查看全部课程
const viewAllCourses = () => {
  router.push('/courses')
}
</script>

<style lang="scss" scoped>
.profile-container {
  position: relative;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.main-content {
  margin-right: 320px; // 为右侧安全设置留出空间
  display: flex;
  flex-direction: column;
  gap: 20px;

  .profile-card,
  .visualization-container {
    width: 100%;
  }
}

.security-card {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 300px;
  background: var(--el-bg-color);
}

@media (max-width: 1200px) {
  .main-content {
    margin-right: 0;
  }

  .security-card {
    position: static;
    width: 100%;
    margin-top: 20px;
  }
}

.profile-card {
  background: var(--el-bg-color);
  margin-bottom: 20px;
}

.visualization-container {
  display: grid;
  gap: 20px;
}

.profile-header {
  display: flex;
  gap: 40px;
  padding: 20px;
}

.avatar-section {
  position: relative;
  
  .avatar {
    border: 4px solid rgba(100, 255, 218, 0.2);
    transition: all 0.3s;
  }
  
  .avatar-mask {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5);
    color: #fff;
    opacity: 0;
    transition: opacity 0.3s;
    cursor: pointer;
    border-radius: 50%;
    
    .el-icon {
      font-size: 24px;
      margin-bottom: 4px;
    }
    
    span {
      font-size: 12px;
    }
  }
  
  &:hover {
    .avatar-mask {
      opacity: 1;
    }
  }
}

.user-info {
  flex: 1;
  
  h2 {
    font-size: 24px;
    color: #64ffda;
    margin: 0 0 8px;
  }
  
  .user-email {
    color: #8892b0;
    margin: 0 0 20px;
  }
}

.user-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
  
  .stat-value {
    display: block;
    font-size: 24px;
    font-weight: bold;
    color: #64ffda;
    margin-bottom: 4px;
  }
  
  .stat-label {
    color: #8892b0;
    font-size: 14px;
  }
}

.progress-card,
.skills-card {
  height: 400px;
  background-color: var(--el-bg-color);
  
  .progress-content,
  .skills-content {
    height: calc(100% - 60px);
    width: 100%;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .chart {
    width: 100%;
    height: 100%;
    min-height: 300px;
  }
}

.activity-card,
.security-card {
  height: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
  
  h3 {
    margin: 0;
    color: var(--el-text-color-primary);
    font-size: 16px;
    font-weight: 500;
  }
}

.security-card {
  margin-left: 20px;
  width: 300px;
  flex-shrink: 0;
}

.security-content {
  padding: 0;
}

.security-list {
  .security-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid var(--el-border-color-lighter);

    &:last-child {
      border-bottom: none;
    }

    .security-info {
      display: flex;
      align-items: center;
      gap: 12px;

      .el-icon {
        font-size: 18px;
        color: var(--el-text-color-secondary);
      }

      .security-text {
        h4 {
          margin: 0;
          font-size: 14px;
          color: var(--el-text-color-primary);
          margin-bottom: 4px;
        }

        p {
          margin: 0;
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}

.code-input {
  display: flex;
  gap: 16px;
  
  .el-input {
    flex: 1;
  }
}

@media (max-width: 768px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
  
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .user-stats {
    justify-content: center;
  }
}

.recent-courses-card {
  .recent-courses {
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    .course-item {
      display: flex;
      gap: 16px;
      padding: 16px;
      border: 1px solid var(--el-border-color-light);
      border-radius: 8px;
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }
      
      .course-cover {
        width: 160px;
        height: 90px;
        border-radius: 4px;
        overflow: hidden;
      }
      
      .course-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 8px;
        
        .course-title {
          margin: 0;
          font-size: 16px;
          font-weight: 500;
          color: var(--el-text-color-primary);
        }
        
        .course-progress {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .progress-text {
            font-size: 14px;
            color: var(--el-text-color-secondary);
          }
        }
        
        .course-meta {
          display: flex;
          justify-content: space-between;
          font-size: 14px;
          color: var(--el-text-color-secondary);
          
          .chapter-info {
            color: var(--el-color-primary);
          }
        }
        
        .course-actions {
          margin-top: 8px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .recent-courses-card {
    .recent-courses {
      .course-item {
        flex-direction: column;
        
        .course-cover {
          width: 100%;
          height: 200px;
        }
      }
    }
  }
}

@media (max-width: 1200px) {
  .profile-container {
    flex-direction: column;

    .security-card {
      width: 100%;
      margin-left: 0;
    }
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }

  .visualization-container {
    grid-template-columns: 1fr;
  }
}
</style> 