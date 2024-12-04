<template>
  <div class="home">
    <!-- 动态背景 -->
    <dynamic-background />

    <!-- 英雄区域 -->
    <div class="hero-section">
      <h1 class="hero-title">CYBER SECURITY</h1>
      <h2 class="hero-subtitle">AI驱动的安全学习平台</h2>
      
      <!-- 轮播展示区 -->
      <el-carousel 
        :interval="4000" 
        height="360px" 
        class="hero-carousel"
        :autoplay="true"
        indicator-position="outside"
        arrow="hover"
        trigger="click"
      >
        <el-carousel-item v-for="(item, index) in carouselItems" :key="index">
          <div class="carousel-content" :style="{ background: item.color }">
            <div class="carousel-text">
              <el-icon class="carousel-icon" :size="40">
                <component :is="getIcon(item.icon)" />
              </el-icon>
              <h2>{{ item.title }}</h2>
              <p>{{ item.description }}</p>
              <el-button type="primary" size="large" class="carousel-btn" @click="handleCarouselAction(item)">
                立即体验
              </el-button>
            </div>
            <div class="carousel-image">
              <el-icon :size="80">
                <component :is="getIcon(item.icon)" />
              </el-icon>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>

      <!-- 功能按钮区 -->
      <div class="feature-buttons">
        <el-button type="primary" size="large" class="feature-btn" @click="startJourney">
          『开启安全之旅』
        </el-button>
        <el-button type="success" size="large" class="feature-btn" @click="openNova">
          AI助手『NOVA』
        </el-button>
      </div>
    </div>

    <!-- 精选课程 -->
    <div class="section">
      <div class="section-header">
        <h2>FEATURED COURSES</h2>
        <el-button type="text" class="explore-btn" @click="$router.push('/courses')">
          EXPLORE <el-icon><arrow-right /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8" v-for="course in featuredCourses" :key="course.id">
          <el-card class="course-card" shadow="hover">
            <div class="course-icon">
              <el-icon :size="40">
                <component :is="getIcon(course.icon)" />
              </el-icon>
            </div>
            <h3>{{ course.title }}</h3>
            <p>{{ course.description }}</p>
            <el-progress :percentage="course.progress" />
            <el-button type="primary" plain @click="startCourse(course.id)">开始学习</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 网络实验室 -->
    <div class="section">
      <div class="section-header">
        <h2>CYBER LABS</h2>
        <el-button type="text" class="explore-btn" @click="$router.push('/labs')">
          ENTER LAB <el-icon><arrow-right /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="12" v-for="lab in cyberLabs" :key="lab.id">
          <el-card class="lab-card" shadow="hover">
            <div class="lab-status" :class="lab.status">
              {{ lab.status === 'online' ? '运行中' : '维护中' }}
            </div>
            <h3>{{ lab.title }}</h3>
            <p>{{ lab.description }}</p>
            <div class="lab-info">
              <span>
                <el-icon><user /></el-icon>
                {{ lab.users }} 在线
              </span>
              <el-button type="primary" @click="enterLab(lab.id)">进入实验</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 学习路径 -->
    <div class="section">
      <div class="section-header">
        <h2>LEARNING PATH</h2>
        <el-button type="text" class="explore-btn" @click="$router.push('/knowledge')">
          VISUALIZE <el-icon><arrow-right /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="path-card" shadow="hover">
            <h3>3D知识图谱可视化</h3>
            <div class="graph-placeholder">
              <!-- 这里后续会接入3D知识图谱 -->
              知识图谱加载中...
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="path-card" shadow="hover">
            <h3>学习路径推荐</h3>
            <div class="path-content">
              <el-steps direction="vertical">
                <el-step title="Web安全基础" description="HTML, JavaScript, HTTP基础" />
                <el-step title="漏洞原理" description="XSS, SQL注入, CSRF等" />
                <el-step title="渗透测试" description="工具使用, 漏洞利用" />
              </el-steps>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 每日挑战 -->
    <div class="section">
      <div class="section-header">
        <h2>CYBER CHALLENGE</h2>
        <el-button type="text" class="explore-btn" @click="$router.push('/challenge')">
          RANKING <el-icon><arrow-right /></el-icon>
        </el-button>
      </div>
      <el-card class="challenge-card" shadow="hover">
        <div class="challenge-header">
          <h3>今日挑战 - {{ dailyChallenge.title }}</h3>
        </div>
        <div class="challenge-info">
          <div class="info-item">
            <label>难度：</label>
            <el-rate
              v-model="dailyChallenge.difficulty"
              disabled
              show-score
              text-color="#ff9900"
            />
          </div>
          <div class="info-item">
            <label>参与：</label>
            <span>{{ dailyChallenge.participants }}</span>
          </div>
          <div class="info-item">
            <label>完成率：</label>
            <span>{{ dailyChallenge.completion_rate }}%</span>
          </div>
          <div class="info-item">
            <label>积分：</label>
            <span>{{ dailyChallenge.points }}</span>
          </div>
        </div>
        <div class="challenge-actions">
          <el-button type="primary" @click="startChallenge">立即挑战</el-button>
          <el-button @click="viewHints">查看提示</el-button>
          <el-button type="success" @click="submitFlag">提交Flag</el-button>
        </div>
      </el-card>
    </div>

    <!-- 对抗专区 -->
    <div class="section">
      <div class="section-header">
        <h2>BATTLE ZONE</h2>
        <el-button type="text" class="explore-btn" @click="$router.push('/battle')">
          ENTER BATTLE <el-icon><arrow-right /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="battle-card" shadow="hover">
            <h3>实时对抗</h3>
            <p>与其他选手实时对抗，提升实战能力</p>
            <el-button type="danger" @click="startBattle">开始对抗</el-button>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="battle-card" shadow="hover">
            <h3>创建房间</h3>
            <p>创建私人对抗房间，邀请好友加入</p>
            <el-button type="primary" @click="createRoom">创建房间</el-button>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="battle-card" shadow="hover">
            <h3>快速加入</h3>
            <p>加入正在进行对抗房间</p>
            <el-button type="warning" @click="quickJoin">快速加入</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 成就系统 -->
    <div class="section">
      <div class="section-header">
        <h2>ACHIEVEMENTS</h2>
        <el-button type="text" class="explore-btn" @click="$router.push('/achievements')">
          VIEW ALL <el-icon><arrow-right /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="achievement-card" shadow="hover">
            <h3>技能徽章</h3>
            <div class="badge-list">
              <!-- 这里后续会展示获得的徽章 -->
              <el-empty description="暂无徽章" />
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="achievement-card" shadow="hover">
            <h3>排行榜</h3>
            <div class="ranking-list">
              <!-- 这里后续会展示排行榜 -->
              <el-empty description="暂无排名" />
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="achievement-card" shadow="hover">
            <h3>项目展示</h3>
            <div class="project-list">
              <!-- 这里后续会展示完成的项目 -->
              <el-empty description="暂无项目" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import DynamicBackground from '@/components/DynamicBackground.vue'
import {
  Monitor,
  Lock,
  Connection,
  CircleCheck,
  ArrowRightBold,
  Avatar
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 图标映射函数
const getIcon = (iconName: string) => {
  const iconMap: { [key: string]: any } = {
    Monitor,
    Lock,
    Connection,
    CircleCheck,
    ArrowRightBold,
    Avatar
  }
  return iconMap[iconName] || Monitor
}

// 轮播数据
const carouselItems = ref([
  {
    icon: 'Monitor',
    title: '智能学习系统',
    description: '基于AI的个性化学习路径推荐',
    color: 'linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%)',
    action: 'courses'
  },
  {
    icon: 'Lock',
    title: '实战靶场',
    description: '真实环境的漏洞利用训练',
    color: 'linear-gradient(120deg, #ff9a9e 0%, #fad0c4 100%)',
    action: 'labs'
  },
  {
    icon: 'Connection',
    title: '在线对抗',
    description: '多人实时对抗，提升实战能力',
    color: 'linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)',
    action: 'battle'
  }
])

// 精选课程
const featuredCourses = ref([
  {
    id: 1,
    icon: 'Monitor',
    title: 'Web安全基础',
    description: '从零开始学习Web安全基础知识',
    progress: 0
  },
  {
    id: 2,
    icon: 'Lock',
    title: 'SQL注入进阶',
    description: '深入学习SQL注入原理与防御',
    progress: 0
  },
  {
    id: 3,
    icon: 'CircleCheck',
    title: '内网渗透',
    description: '企业内网渗透测试技术',
    progress: 0
  }
])

// 实验室数据
const cyberLabs = ref([
  {
    id: 1,
    title: 'Web漏洞实验室',
    description: '包含常见Web漏洞的靶场环境',
    status: 'online',
    users: 128
  },
  {
    id: 2,
    title: '内网渗透实验室',
    description: '模拟真实企业内网环境',
    status: 'online',
    users: 56
  }
])

// 每日挑战
const dailyChallenge = ref({
  title: 'SQL注入挑战',
  difficulty: 3,
  participants: 256,
  completion_rate: 45,
  points: 100
})

// 方法定义
const handleCarouselAction = (item: any) => {
  if (item.action === 'courses') {
    router.push('/courses')
  } else if (item.action === 'labs') {
    router.push('/labs')
  } else if (item.action === 'battle') {
    router.push('/battle')
  }
}

const startJourney = () => {
  if (userStore.isAuthenticated) {
    router.push('/dashboard')
  } else {
    router.push('/login')
  }
}

const openNova = () => {
  // TODO: 打开AI助手对话框
  console.log('Opening NOVA AI Assistant...')
}

const startCourse = (courseId: number) => {
  if (userStore.isAuthenticated) {
    router.push(`/courses/${courseId}`)
  } else {
    router.push('/login')
  }
}

const enterLab = (labId: number) => {
  if (userStore.isAuthenticated) {
    router.push(`/labs/${labId}`)
  } else {
    router.push('/login')
  }
}

const startChallenge = () => {
  if (userStore.isAuthenticated) {
    router.push('/challenge')
  } else {
    router.push('/login')
  }
}

const viewHints = () => {
  // TODO: 显示提示对话框
  console.log('Viewing hints...')
}

const submitFlag = () => {
  // TODO: 显示提交Flag对话框
  console.log('Submitting flag...')
}

const startBattle = () => {
  if (userStore.isAuthenticated) {
    router.push('/battle')
  } else {
    router.push('/login')
  }
}

const createRoom = () => {
  if (userStore.isAuthenticated) {
    router.push('/battle/create')
  } else {
    router.push('/login')
  }
}

const quickJoin = () => {
  if (userStore.isAuthenticated) {
    router.push('/battle/join')
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  color: #ffffff;
}

.hero-section {
  padding: 60px 20px;
  text-align: center;
}

.hero-title {
  font-size: 48px;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.hero-subtitle {
  font-size: 24px;
  margin: 10px 0 40px;
  font-weight: normal;
  opacity: 0.8;
}

.hero-carousel {
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 8px;
  overflow: hidden;
}

.carousel-content {
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 60px;
}

.carousel-text {
  flex: 1;
  text-align: left;
}

.carousel-icon {
  font-size: 40px;
  margin-bottom: 20px;
}

.carousel-text h2 {
  font-size: 36px;
  margin: 0 0 10px;
}

.carousel-text p {
  font-size: 18px;
  margin: 0 0 20px;
  opacity: 0.8;
}

.carousel-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feature-buttons {
  margin-top: 40px;
}

.feature-btn {
  margin: 0 10px;
}

.section {
  max-width: 1200px;
  margin: 60px auto;
  padding: 0 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.section-header h2 {
  margin: 0;
  font-size: 32px;
}

.explore-btn {
  display: flex;
  align-items: center;
  gap: 5px;
}

.course-card,
.lab-card,
.path-card,
.challenge-card,
.battle-card,
.achievement-card {
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: none;
  color: #ffffff;
}

.course-icon {
  text-align: center;
  margin-bottom: 20px;
}

.lab-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 4px;
}

.lab-status.online {
  background: #67c23a;
}

.lab-status.maintenance {
  background: #e6a23c;
}

.lab-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.graph-placeholder {
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.challenge-header {
  margin-bottom: 20px;
}

.challenge-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.challenge-actions {
  display: flex;
  gap: 10px;
}

.badge-list,
.ranking-list,
.project-list {
  min-height: 200px;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 20px;
  }

  .carousel-content {
    flex-direction: column;
    padding: 20px;
  }

  .carousel-text {
    text-align: center;
    margin-bottom: 20px;
  }

  .feature-buttons {
    flex-direction: column;
    gap: 10px;
  }

  .feature-btn {
    width: 100%;
    margin: 5px 0;
  }
}
</style> 