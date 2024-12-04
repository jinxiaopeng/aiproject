<template>
  <div class="dashboard">
    <!-- 欢迎卡片 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <div class="user-info">
          <el-avatar :size="64" :src="userStore.userInfo.avatar" />
          <div class="welcome-text">
            <h2>欢迎回来，{{ userStore.userInfo.username }}</h2>
            <p>今天是个学习的好日子！</p>
          </div>
        </div>
        <div class="quick-stats">
          <div class="stat-item">
            <h3>{{ stats.completedCourses }}</h3>
            <span>已完成课程</span>
          </div>
          <div class="stat-item">
            <h3>{{ stats.completedLabs }}</h3>
            <span>完成实验</span>
          </div>
          <div class="stat-item">
            <h3>{{ stats.totalPoints }}</h3>
            <span>总积分</span>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20" class="dashboard-content">
      <!-- 学习进度 -->
      <el-col :span="16">
        <el-card class="progress-card">
          <template #header>
            <div class="card-header">
              <span>学习进度</span>
              <el-button type="text" @click="$router.push('/courses/list')">
                查看全部
              </el-button>
            </div>
          </template>
          <div class="course-list">
            <div v-for="course in inProgressCourses" :key="course.id" class="course-item">
              <div class="course-info">
                <img :src="course.image || '/default-course.jpg'" :alt="course.title">
                <div class="info">
                  <h4>{{ course.title }}</h4>
                  <el-tag size="small">{{ getCategoryLabel(course.category) }}</el-tag>
                </div>
              </div>
              <div class="progress">
                <el-progress 
                  :percentage="course.progress" 
                  :status="course.progress === 100 ? 'success' : ''"
                />
                <el-button 
                  type="primary" 
                  size="small"
                  @click="$router.push(`/courses/${course.id}`)"
                >
                  {{ course.progress === 100 ? '复习' : '继续学习' }}
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧信息栏 -->
      <el-col :span="8">
        <!-- 技能雷达图 -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>技能分布</span>
            </div>
          </template>
          <div class="radar-chart" ref="radarChart"></div>
        </el-card>

        <!-- 最近活动 -->
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
            </div>
          </template>
          <div class="timeline">
            <el-timeline>
              <el-timeline-item
                v-for="activity in recentActivities"
                :key="activity.id"
                :timestamp="activity.time"
                :type="activity.type"
              >
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import * as echarts from 'echarts'
import { courseApi, analysisApi } from '@/api'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const radarChart = ref(null)

    const stats = ref({
      completedCourses: 0,
      completedLabs: 0,
      totalPoints: 0
    })

    const inProgressCourses = ref([])
    const recentActivities = ref([])

    // 获取学习统计数据
    const loadStats = async () => {
      try {
        const response = await courseApi.getLearningProgress()
        const completedCourses = response.filter(c => c.progress === 100)
        stats.value = {
          completedCourses: completedCourses.length,
          completedLabs: 0, // 待实现
          totalPoints: completedCourses.reduce((sum, c) => sum + (c.score || 0), 0)
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }
    }

    // 获取进行中的课程
    const loadInProgressCourses = async () => {
      try {
        const response = await courseApi.getLearningProgress()
        inProgressCourses.value = response
          .filter(c => c.progress > 0 && c.progress < 100)
          .slice(0, 5)
      } catch (error) {
        console.error('加载课程进度失败:', error)
      }
    }

    // 获取最近活动
    const loadRecentActivities = async () => {
      // 模拟数据，实际应该从后端获取
      recentActivities.value = [
        {
          id: 1,
          content: '完成了 SQL注入基础 课程的学习',
          time: '2024-01-20 10:30',
          type: 'success'
        },
        {
          id: 2,
          content: '开始学习 XSS攻击防御 课程',
          time: '2024-01-19 15:20',
          type: 'primary'
        },
        {
          id: 3,
          content: '在 Web安全实验室 中获得了新成就',
          time: '2024-01-18 09:45',
          type: 'warning'
        }
      ]
    }

    // 初始化雷达图
    const initRadarChart = async () => {
      try {
        const chart = echarts.init(radarChart.value)
        const { categories, values } = await analysisApi.getSkillRadar()
        
        const option = {
          radar: {
            indicator: categories.map(cat => ({
              name: cat,
              max: 100
            }))
          },
          series: [{
            type: 'radar',
            data: [{
              value: values,
              name: '技能分布',
              areaStyle: {
                color: 'rgba(64,158,255,0.2)'
              },
              lineStyle: {
                color: '#409EFF'
              }
            }]
          }]
        }
        
        chart.setOption(option)
      } catch (error) {
        console.error('初始化雷达图失败:', error)
      }
    }

    const getCategoryLabel = (value) => {
      const categories = {
        'web': 'Web安全',
        'network': '网络安全',
        'system': '系统安全',
        'crypto': '密码学'
      }
      return categories[value] || value
    }

    onMounted(() => {
      loadStats()
      loadInProgressCourses()
      loadRecentActivities()
      initRadarChart()
    })

    return {
      userStore,
      stats,
      inProgressCourses,
      recentActivities,
      radarChart,
      getCategoryLabel
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome-text h2 {
  margin: 0;
  font-size: 24px;
}

.welcome-text p {
  margin: 5px 0 0;
  color: #666;
}

.quick-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-item h3 {
  margin: 0;
  font-size: 24px;
  color: #409EFF;
}

.stat-item span {
  color: #666;
  font-size: 14px;
}

.dashboard-content {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.course-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.course-info img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.info h4 {
  margin: 0 0 5px 0;
}

.progress {
  width: 200px;
}

.chart-card {
  margin-bottom: 20px;
}

.radar-chart {
  height: 300px;
}

.timeline {
  padding: 10px;
  max-height: 400px;
  overflow-y: auto;
}
</style> 