<template>
  <div class="home">
    <DynamicBackground />
    
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
              <el-icon class="carousel-icon">
                <component :is="item.icon" />
              </el-icon>
              <h2>{{ item.title }}</h2>
              <p>{{ item.description }}</p>
              <el-button type="primary" size="large" class="carousel-btn" @click="handleCarouselAction(item)">
                立即体验
              </el-button>
            </div>
            <div class="carousel-image">
              <el-icon :size="80" :class="item.icon.toLowerCase()">
                <component :is="item.icon" />
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
          EXPLORE <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8" v-for="course in featuredCourses" :key="course.id">
          <el-card class="course-card" shadow="hover">
            <div class="course-icon">
              <el-icon :size="40">
                <component :is="course.icon" />
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
          ENTER LAB <el-icon><ArrowRight /></el-icon>
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
                <el-icon><User /></el-icon>
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
          VISUALIZE <el-icon><ArrowRight /></el-icon>
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
          RANKING <el-icon><ArrowRight /></el-icon>
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
          ENTER BATTLE <el-icon><ArrowRight /></el-icon>
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
          VIEW ALL <el-icon><ArrowRight /></el-icon>
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
import DynamicBackground from '@/components/DynamicBackground.vue'
import { Monitor, Lock, Key, Document, DataAnalysis, Connection, User, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

// 轮播数据
const carouselItems = ref([
  {
    title: 'Web安全实战',
    description: '从零开始学习Web安全，掌握渗透测试技能',
    icon: 'Monitor',
    color: 'linear-gradient(135deg, #1890ff1a 0%, #1890ff4d 100%)'
  },
  {
    title: '系统安全',
    description: '深入理解系统安全，掌握防护技能',
    icon: 'Lock',
    color: 'linear-gradient(135deg, #52c41a1a 0%, #52c41a4d 100%)'
  },
  {
    title: '密码学基础',
    description: '探索现代密码学原理与应用',
    icon: 'Key',
    color: 'linear-gradient(135deg, #722ed11a 0%, #722ed14d 100%)'
  }
])

// 精选课程数据
const featuredCourses = ref([
  {
    id: 1,
    title: 'Web渗透测试',
    description: '系统学习Web应用安全漏洞与防护',
    icon: 'Monitor',
    progress: 0
  },
  {
    id: 2,
    title: '系统安全',
    description: '掌握系统安全加固技术',
    icon: 'Lock',
    progress: 0
  },
  {
    id: 3,
    title: '现代密码学',
    description: '探索密码学原理与实践',
    icon: 'Key',
    progress: 0
  }
])

// 实验室数据
const cyberLabs = ref([
  {
    id: 1,
    title: '渗透测试实验室',
    description: '真实漏洞环境，在线渗透测试',
    status: 'online',
    users: 128
  },
  {
    id: 2,
    title: '漏洞复现环境',
    description: '经典漏洞复现与分析',
    status: 'online',
    users: 86
  }
])

// 每日挑战数据
const dailyChallenge = ref({
  title: 'Web安全实战',
  difficulty: 3,
  participants: '1.2k',
  completion_rate: 45,
  points: 500
})

// 功能按钮事件处理
const startJourney = () => {
  router.push('/courses')
}

const openNova = () => {
  // TODO: 实现AI助手功能
  console.log('Opening NOVA AI Assistant...')
}

// 轮播事件处理
const handleCarouselAction = (item: any) => {
  router.push('/courses')
}

// 课程相关事件
const startCourse = (courseId: number) => {
  router.push(`/courses/${courseId}`)
}

// 实验室相关事件
const enterLab = (labId: number) => {
  router.push(`/labs/${labId}`)
}

// 挑战相关事件
const startChallenge = () => {
  router.push('/challenge')
}

const viewHints = () => {
  // TODO: 实现查看提示功能
}

const submitFlag = () => {
  // TODO: 实现提交Flag功能
}

// 对抗相关事件
const startBattle = () => {
  router.push('/battle')
}

const createRoom = () => {
  router.push('/battle/create')
}

const quickJoin = () => {
  router.push('/battle/join')
}
</script>

<style scoped>
.home {
  min-height: calc(100vh - 64px);
  padding: 40px;
}

.hero-section {
  text-align: center;
  padding: 60px 0;
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 16px;
  letter-spacing: 2px;
}

.hero-subtitle {
  font-size: 24px;
  color: #666;
  margin-bottom: 40px;
}

.hero-carousel {
  margin-bottom: 40px;
}

.carousel-content {
  height: 100%;
  padding: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 8px;
}

.carousel-text {
  flex: 1;
  text-align: left;
  padding-right: 40px;
}

.carousel-icon {
  font-size: 48px;
  color: #1890ff;
  margin-bottom: 20px;
}

.carousel-text h2 {
  font-size: 32px;
  color: #1890ff;
  margin-bottom: 16px;
}

.carousel-text p {
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
}

.carousel-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feature-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.feature-btn {
  min-width: 200px;
}

.section {
  margin-bottom: 60px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 24px;
  color: #1890ff;
  font-weight: bold;
}

.explore-btn {
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-card,
.lab-card,
.path-card,
.challenge-card,
.battle-card,
.achievement-card {
  height: 100%;
  transition: all 0.3s;
}

.course-card:hover,
.lab-card:hover,
.path-card:hover,
.battle-card:hover,
.achievement-card:hover {
  transform: translateY(-5px);
}

.course-icon {
  text-align: center;
  margin-bottom: 16px;
}

.lab-status {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.lab-status.online {
  background: #f6ffed;
  color: #52c41a;
}

.lab-status.maintenance {
  background: #fff7e6;
  color: #fa8c16;
}

.lab-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.graph-placeholder {
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
  border-radius: 4px;
  color: #999;
}

.path-content {
  padding: 20px;
}

.challenge-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin: 20px 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.challenge-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.badge-list,
.ranking-list,
.project-list {
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .home {
    padding: 20px;
  }
  
  .hero-title {
    font-size: 32px;
  }
  
  .hero-subtitle {
    font-size: 18px;
  }

  .feature-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .carousel-content {
    flex-direction: column;
    text-align: center;
  }
  
  .carousel-text {
    padding-right: 0;
    margin-bottom: 20px;
  }
}
</style> 