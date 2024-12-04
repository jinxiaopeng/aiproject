<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <!-- 左侧个人信息卡片 -->
      <el-col :span="8">
        <el-card class="profile-card">
          <div class="avatar-container">
            <el-avatar
              :size="120"
              :src="userInfo.avatar || defaultAvatar"
              @error="handleAvatarError"
            />
            <el-upload
              class="avatar-uploader"
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
              action="/api/user/avatar"
              :headers="uploadHeaders"
            >
              <el-button size="small" type="primary" class="upload-btn">
                更换头像
              </el-button>
            </el-upload>
          </div>
          
          <h2 class="username">{{ userInfo.username }}</h2>
          <p class="email">{{ userInfo.email }}</p>
          
          <div class="info-list">
            <div class="info-item">
              <span class="label">角色：</span>
              <el-tag :type="userInfo.role === 'admin' ? 'danger' : 'success'">
                {{ userInfo.role === 'admin' ? '管理员' : '学员' }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">注册时间：</span>
              <span>{{ formatDate(userInfo.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">最后登录：</span>
              <span>{{ formatDate(userInfo.last_login) }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧学习数据 -->
      <el-col :span="16">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>学习统计</span>
              <el-button type="primary" link>查看详情</el-button>
            </div>
          </template>
          
          <el-row :gutter="20" class="stats-row">
            <el-col :span="8">
              <div class="stats-item">
                <h3>{{ stats.courseCount }}</h3>
                <p>已学课程</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stats-item">
                <h3>{{ stats.labCount }}</h3>
                <p>完成实验</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stats-item">
                <h3>{{ stats.studyHours }}h</h3>
                <p>学习时长</p>
              </div>
            </el-col>
          </el-row>
          
          <!-- 学习进度图表 -->
          <div class="progress-chart" ref="chartRef"></div>
        </el-card>
        
        <!-- 最近活动 -->
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
            </div>
          </template>
          
          <el-timeline>
            <el-timeline-item
              v-for="activity in activities"
              :key="activity.id"
              :timestamp="formatDate(activity.created_at)"
              :type="activity.type"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { formatDate } from '@/utils/format'

const authStore = useAuthStore()
const chartRef = ref<HTMLElement>()
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

// 用户信息
const userInfo = ref(authStore.userInfo)

// 统计数据
const stats = ref({
  courseCount: 0,
  labCount: 0,
  studyHours: 0
})

// 最近活动
const activities = ref([])

// 上传相关
const uploadHeaders = {
  Authorization: `Bearer ${authStore.token}`
}

// 头像上传前的验证
const beforeAvatarUpload = (file: File) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('头像只能是 JPG 或 PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
  }
  return isJPG && isLt2M
}

// 头像上传成功
const handleAvatarSuccess = (res: any) => {
  userInfo.value.avatar = res.url
  ElMessage.success('头像更新成功')
}

// 头像加载失败
const handleAvatarError = () => {
  userInfo.value.avatar = defaultAvatar
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  const chart = echarts.init(chartRef.value)
  const option = {
    title: {
      text: '学习进度',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line',
        smooth: true
      }
    ]
  }
  
  chart.setOption(option)
}

// 获取统计数据
const fetchStats = async () => {
  try {
    // TODO: 调用后端 API 获取统计数据
    stats.value = {
      courseCount: 5,
      labCount: 12,
      studyHours: 24
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取最近活动
const fetchActivities = async () => {
  try {
    // TODO: 调用后端 API 获取活动数据
    activities.value = [
      {
        id: 1,
        content: '完成了 Web 安全基础课程的学习',
        created_at: '2024-01-20 14:30:00',
        type: 'success'
      },
      {
        id: 2,
        content: '参与了 SQL 注入实验',
        created_at: '2024-01-19 16:20:00',
        type: 'primary'
      }
    ]
  } catch (error) {
    console.error('获取活动数据失败:', error)
  }
}

onMounted(async () => {
  await Promise.all([
    fetchStats(),
    fetchActivities()
  ])
  initChart()
})
</script>

<style lang="scss" scoped>
.profile-container {
  padding: 20px;
  
  .profile-card {
    text-align: center;
    
    .avatar-container {
      margin: 20px 0;
      position: relative;
      
      .upload-btn {
        margin-top: 10px;
      }
    }
    
    .username {
      font-size: 24px;
      margin: 10px 0;
    }
    
    .email {
      color: #666;
      margin-bottom: 20px;
    }
    
    .info-list {
      text-align: left;
      padding: 0 20px;
      
      .info-item {
        margin: 10px 0;
        
        .label {
          color: #666;
          margin-right: 10px;
        }
      }
    }
  }
  
  .stats-card {
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .stats-row {
      text-align: center;
      margin-bottom: 20px;
      
      .stats-item {
        h3 {
          font-size: 24px;
          color: #409EFF;
          margin-bottom: 5px;
        }
        
        p {
          color: #666;
        }
      }
    }
    
    .progress-chart {
      height: 300px;
    }
  }
  
  .activity-card {
    .el-timeline {
      padding: 20px;
    }
  }
}
</style> 