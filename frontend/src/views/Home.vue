<template>
  <div class="home">
    <!-- 顶部导航 -->
    <!-- Removed duplicate navigation bar -->

    <!-- 动态背景区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <el-carousel :interval="5000" height="500px" class="hero-carousel">
          <el-carousel-item v-for="item in carouselItems" :key="item.id" v-if="item.title && item.description">
            <div class="carousel-content" :style="{ background: item.color }">
              <div class="carousel-text">
                <el-icon class="carousel-icon">
                  <component :is="item.icon" />
                </el-icon>
                <h2>{{ item.title }}</h2>
                <p>{{ item.description }}</p>
                <el-button type="primary" size="large" class="carousel-btn">
                  立即体验
                </el-button>
              </div>
              <div class="carousel-image">
                <!-- 这里可以添加对应的图片 -->
                <el-icon :size="120" :class="item.icon.toLowerCase()">
                  <component :is="item.icon" />
                </el-icon>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>
    </div>

    <!-- 功能按钮区 -->
    <div class="feature-buttons">
      <el-button type="primary" size="large" class="feature-btn">
        开启安全之旅
      </el-button>
      <el-button type="success" size="large" class="feature-btn">
        AI助手『NOVA』
      </el-button>
    </div>

    <!-- 特色课程 -->
    <div class="section">
      <div class="section-header">
        <h2>精选课程</h2>
        <el-button type="text" class="explore-btn">
          探索更多 <el-icon><ArrowRight /></el-icon>
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
            <el-button type="primary" plain>开始学习</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 实验室 -->
    <div class="section">
      <div class="section-header">
        <h2>网络实验室</h2>
        <el-button type="text" class="explore-btn">
          进入实验室 <el-icon><ArrowRight /></el-icon>
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
              <el-button type="primary">进入实验</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 学习路径 -->
    <div class="section">
      <div class="section-header">
        <h2>学习路径</h2>
        <el-button type="text" class="explore-btn">
          可视化 <el-icon><ArrowRight /></el-icon>
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
        <h2>每日挑战</h2>
        <el-button type="text" class="explore-btn">
          排行榜 <el-icon><ArrowRight /></el-icon>
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
          <el-button type="primary">立即挑战</el-button>
          <el-button>查看提示</el-button>
          <el-button type="success">提交Flag</el-button>
        </div>
      </el-card>
    </div>

    <!-- 对抗专区 -->
    <div class="section">
      <div class="section-header">
        <h2>对抗专区</h2>
        <el-button type="text" class="explore-btn">
          进入对抗 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="battle-card" shadow="hover">
            <h3>实时对抗</h3>
            <p>与其他选手实时对抗，提升实战能力</p>
            <el-button type="danger">开始对抗</el-button>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="battle-card" shadow="hover">
            <h3>创建房间</h3>
            <p>创建私人对抗房间，邀请好友加入</p>
            <el-button type="primary">创建房间</el-button>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="battle-card" shadow="hover">
            <h3>快速加入</h3>
            <p>加入正在进行的对抗房间</p>
            <el-button type="warning">快速加入</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 成就系统 -->
    <div class="section">
      <div class="section-header">
        <h2>个人成就</h2>
        <el-button type="text" class="explore-btn">
          查看全部 <el-icon><ArrowRight /></el-icon>
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

<script lang="ts">
import { defineComponent, ref } from 'vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Home',
  components: {
    ...ElementPlusIconsVue
  },
  setup() {
    const router = useRouter()

    const carouselItems = ref([
      {
        id: 1,
        title: '网络安全实验平台',
        description: '提供全面的网络安全实践环境，从基础到高级的漏洞利用与防护',
        icon: 'Monitor',
        color: 'linear-gradient(135deg, #1890ff 0%, #36cfc9 100%)'
      },
      {
        id: 2,
        title: '实战演练',
        description: '真实场景下的安全漏洞利用与防护，提升实战能力',
        icon: 'Lock',
        color: 'linear-gradient(135deg, #722ed1 0%, #1890ff 100%)'
      },
      {
        id: 3,
        title: '在线学习',
        description: '随时随地，开启安全技能提升之旅，打造专业能力',
        icon: 'Key',
        color: 'linear-gradient(135deg, #52c41a 0%, #1890ff 100%)'
      }
    ])

    const featuredCourses = ref([
      {
        id: 1,
        title: 'Web渗透测试',
        description: '从基础到高级的Web安全课程',
        icon: 'Monitor',
        progress: 0
      },
      {
        id: 2,
        title: '系统安全',
        description: '系统安全与防护技术',
        icon: 'Lock',
        progress: 0
      },
      {
        id: 3,
        title: '现代密码学',
        description: '密码学原理与应用',
        icon: 'Key',
        progress: 0
      }
    ])

    const cyberLabs = ref([
      {
        id: 1,
        title: '渗透测试实验室',
        description: '真实环境下的渗透测试训练',
        status: 'online',
        users: 128
      },
      {
        id: 2,
        title: '漏洞复现环境',
        description: '常见漏洞的复现与利用',
        status: 'online',
        users: 85
      }
    ])

    const dailyChallenge = ref({
      title: 'Web安全实战',
      difficulty: 3,
      participants: 1200,
      completion_rate: 45,
      points: 500
    })

    return {
      carouselItems,
      featuredCourses,
      cyberLabs,
      dailyChallenge
    }
  }
})
</script>

<style scoped>
.home {
  padding-top: 64px;
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* 导航栏样式优化 */
.nav-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 64px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
  text-decoration: none;
  transition: color 0.3s;
}

.logo:hover {
  color: #40a9ff;
}

/* 英雄区域样式 */
.hero-section {
  padding-top: 64px;
  background: #f0f2f5;
  min-height: 100vh;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 48px;
  color: #1890ff;
  margin-bottom: 16px;
  font-weight: 600;
}

.hero-subtitle {
  font-size: 20px;
  color: #666;
  margin-bottom: 40px;
}

/* 轮播图样式优化 */
.hero-carousel {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.carousel-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 80px;
}

.carousel-text {
  flex: 1;
  text-align: left;
  color: white;
  max-width: 500px;
}

.carousel-text h2 {
  font-size: 36px;
  margin-bottom: 20px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.carousel-text p {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 30px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.carousel-icon {
  font-size: 48px;
  margin-bottom: 24px;
}

.carousel-btn {
  padding: 12px 30px;
  font-size: 16px;
}

.carousel-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image .el-icon {
  color: rgba(255, 255, 255, 0.9);
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.2));
  transition: transform 0.3s;
}

.carousel-image .el-icon:hover {
  transform: scale(1.1);
}

/* 图标特效 */
.monitor {
  animation: float 3s ease-in-out infinite;
}

.lock {
  animation: rotate 3s ease-in-out infinite;
}

.key {
  animation: swing 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes rotate {
  0%, 100% { transform: rotate(0); }
  50% { transform: rotate(10deg); }
}

@keyframes swing {
  0%, 100% { transform: rotate(0); }
  50% { transform: rotate(-10deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 20px;
  }

  .hero-content h1 {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .carousel-content {
    flex-direction: column;
    padding: 40px;
    text-align: center;
  }

  .carousel-text {
    text-align: center;
    margin-bottom: 40px;
  }

  .carousel-image {
    display: none;
  }
}

/* 功能按钮区 */
.feature-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 40px 0;
}

.feature-btn {
  padding: 20px 40px;
  font-size: 18px;
}

/* 通用section样式 */
.section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
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
  margin: 0;
}

.explore-btn {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 卡片通用样式 */
.el-card {
  transition: all 0.3s;
}

.el-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

/* 课程卡片样式 */
.course-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.course-icon {
  text-align: center;
  margin-bottom: 16px;
  color: #1890ff;
}

/* 实验室卡片样式 */
.lab-card {
  height: 100%;
  position: relative;
}

.lab-status {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.lab-status.online {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

/* 知识图谱样式 */
.graph-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 4px;
  color: #999;
}

/* 挑战卡片样式 */
.challenge-card {
  background: #fff;
  border-radius: 8px;
}

.challenge-info {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 24px 0;
}

.challenge-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

/* 对抗卡片样式 */
.battle-card {
  text-align: center;
  padding: 24px;
}

.battle-card h3 {
  margin-bottom: 16px;
}

/* 成就卡片样式 */
.achievement-card {
  height: 300px;
}

.achievement-card h3 {
  margin-bottom: 20px;
  text-align: center;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 20px;
  }

  .feature-buttons {
    flex-direction: column;
    padding: 0 20px;
  }

  .challenge-info {
    grid-template-columns: repeat(2, 1fr);
  }

  .challenge-actions {
    flex-direction: column;
  }
}
</style> 