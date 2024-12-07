<template>
  <div class="home">
    <DynamicBackground />
    
    <!-- 英雄区域 -->
    <div class="hero-section">
      <h1 class="hero-title">安智领航</h1>
      <p class="hero-subtitle">专业的网络安全学习平台</p>
      
      <!-- 轮播展示区 -->
      <el-carousel 
        :interval="4000" 
        height="360px" 
        class="hero-carousel"
        :autoplay="true"
        indicator-position="outside"
        type="card"
      >
        <el-carousel-item v-for="(image, index) in carouselImages" :key="index">
          <div class="carousel-content" :style="{ backgroundImage: `url(${image.url})` }">
            <div class="carousel-overlay">
              <h2>{{ image.title }}</h2>
              <p>{{ image.description }}</p>
              <el-button type="primary" @click="handleLearnMore(image)">了解更多</el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
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

// 轮播图数据
const carouselImages = ref([
  {
    url: '/src/assets/carousel/slide1.jpg',
    title: 'Web安全实战演练',
    description: '通过实际案例，掌握Web安全防护技能',
    link: '/courses/web-security'
  },
  {
    url: '/src/assets/carousel/slide2.jpg',
    title: '漏洞分析专题',
    description: '深入理解常见漏洞原���与防护方法',
    link: '/courses/vulnerability'
  },
  {
    url: '/src/assets/carousel/slide3.jpg',
    title: '渗透测试训练营',
    description: '系统化的渗透测试实践课程',
    link: '/courses/pentest'
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

// 网络实验室数据
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
    title: '渗透测试环境',
    description: '模拟真实网络环境的渗透测试靶场',
    status: 'maintenance',
    users: 0
  }
])

// 每日挑战数据
const dailyChallenge = ref({
  title: 'SQL注入进阶',
  difficulty: 4,
  participants: 256,
  completion_rate: 45,
  points: 100
})

// 功能处理方法
const handleLearnMore = (image: any) => {
  router.push(image.link)
}

const startCourse = (courseId: number) => {
  router.push(`/course/${courseId}`)
}

const enterLab = (labId: number) => {
  router.push(`/lab/${labId}`)
}

const startChallenge = () => {
  router.push('/challenge/daily')
}

const viewHints = () => {
  // 实现查看提示功能
}

const submitFlag = () => {
  // 实现提交Flag功能
}

const startBattle = () => {
  router.push('/battle/quick-match')
}

const createRoom = () => {
  router.push('/battle/create-room')
}

const quickJoin = () => {
  router.push('/battle/join')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  padding: 40px;
  background: linear-gradient(135deg, #1a2a4f, #0d1b2a);
  
  @media (max-width: 768px) {
    padding: 20px;
  }
}

.hero-section {
  margin: -40px -40px 60px -40px;
  text-align: center;
  padding: 60px 0;
  
  @media (max-width: 768px) {
    margin: -20px -20px 40px -20px;
    padding: 40px 0;
  }
  
  .hero-title {
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 16px;
    letter-spacing: 2px;
    background: linear-gradient(120deg, #ff7f50, #ff6347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    @media (max-width: 768px) {
      font-size: 36px;
      margin-bottom: 12px;
    }
  }
  
  .hero-subtitle {
    font-size: 24px;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 40px;
    
    @media (max-width: 768px) {
      font-size: 18px;
      margin-bottom: 30px;
    }
  }
  
  .hero-carousel {
    .carousel-content {
      height: 100%;
      background-size: cover;
      background-position: center;
      border-radius: 8px;
      overflow: hidden;
      position: relative;
      
      .carousel-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 40px;
        background: linear-gradient(to top, rgba(26, 42, 79, 0.9), transparent);
        
        h2 {
          font-size: 32px;
          margin-bottom: 12px;
          font-weight: 600;
          color: #fff;
        }
        
        p {
          font-size: 16px;
          margin-bottom: 20px;
          opacity: 0.9;
          color: #fff;
        }
      }
    }
  }
}

.section {
  margin-bottom: 60px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  h2 {
    font-size: 24px;
    font-weight: bold;
    color: #fff;
    position: relative;
    padding-left: 16px;
    
    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 4px;
      height: 24px;
      background: linear-gradient(135deg, #ff7f50, #ff6347);
      border-radius: 2px;
    }
  }
}

:deep(.el-card) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  height: 100%;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 127, 80, 0.2);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }
}

.course-card,
.lab-card,
.path-card,
.challenge-card,
.battle-card,
.achievement-card {
  height: 100%;
  
  h3 {
    font-size: 18px;
    margin-bottom: 12px;
    color: #fff;
  }
  
  p {
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 16px;
  }
}

.course-icon {
  text-align: center;
  margin-bottom: 16px;
  color: #ff7f50;
}

.lab-status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  margin-bottom: 12px;
}

.lab-status.online {
  background: rgba(103, 194, 58, 0.1);
  color: #67c23a;
}

.lab-status.maintenance {
  background: rgba(230, 162, 60, 0.1);
  color: #e6a23c;
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
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.6);
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
  
  label {
    color: rgba(255, 255, 255, 0.7);
  }
  
  span {
    color: #fff;
  }
}

.challenge-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #ff7f50, #ff6347);
  border: none;
  
  &:hover {
    background: linear-gradient(135deg, #ff6347, #ff4500);
  }
}

.badge-list,
.ranking-list,
.project-list {
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.explore-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #ff7f50;
  
  &:hover {
    color: #ff6347;
  }
}
</style> 