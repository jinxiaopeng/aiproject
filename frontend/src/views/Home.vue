<template>
  <div class="home">
    <!-- 轮播图部分 -->
    <div class="carousel-container">
      <el-carousel :interval="5000" height="400px">
        <el-carousel-item v-for="item in carouselItems" :key="item.id">
          <div class="carousel-content" :style="{ background: item.color }">
            <div class="carousel-text">
              <el-icon class="carousel-icon" :size="64">
                <component :is="item.icon" />
              </el-icon>
              <h2>{{ item.title }}</h2>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="content">
      <h2 class="section-title">课程方向</h2>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Web安全</span>
                <el-button class="button" text>
                  了解更多 <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </template>
            <div class="card-content">
              <p>学习Web应用安全漏洞与防护</p>
              <ul>
                <li>SQL注入防护</li>
                <li>XSS攻击防御</li>
                <li>CSRF安全机制</li>
              </ul>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>系统安全</span>
                <el-button class="button" text>
                  了解更多 <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </template>
            <div class="card-content">
              <p>掌握系统安全加固技术</p>
              <ul>
                <li>系统漏洞分析</li>
                <li>安全配置管理</li>
                <li>权限控制策略</li>
              </ul>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>密码学</span>
                <el-button class="button" text>
                  了解更多 <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </template>
            <div class="card-content">
              <p>探索现代密码学原理与应用</p>
              <ul>
                <li>加密算法实现</li>
                <li>数字签名技术</li>
                <li>密钥管理方案</li>
              </ul>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { ArrowRight, User, Timer, Monitor, Lock, Key } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Home',
  components: {
    ArrowRight,
    User,
    Timer,
    Monitor,
    Lock,
    Key
  },
  setup() {
    const carouselItems = ref([
      {
        id: 1,
        title: '网络安全实验平台',
        description: '提供全面的网络安全实践环境',
        icon: 'Monitor',
        color: 'linear-gradient(120deg, #1890ff, #36cfc9)'
      },
      {
        id: 2,
        title: '实战演练',
        description: '真实场景下的安全漏洞利用与防护',
        icon: 'Lock',
        color: 'linear-gradient(120deg, #722ed1, #1890ff)'
      },
      {
        id: 3,
        title: '在线学习',
        description: '随时随地，开启安全技能提升之旅',
        icon: 'Key',
        color: 'linear-gradient(120deg, #52c41a, #1890ff)'
      }
    ])

    return {
      carouselItems
    }
  }
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.carousel-container {
  margin-bottom: 40px;
}

.carousel-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.carousel-text {
  text-align: center;
  color: white;
  padding: 0 50px;
  max-width: 800px;
  z-index: 1;
}

.carousel-icon {
  margin-bottom: 24px;
  font-size: 64px;
}

.carousel-text h2 {
  font-size: 2.5em;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.carousel-text p {
  font-size: 1.2em;
  line-height: 1.6;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.section-title {
  text-align: center;
  color: #1890ff;
  font-size: 2em;
  margin: 20px 0 40px;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  color: #666;
  line-height: 1.5;
}

.card-content p {
  margin-bottom: 15px;
  font-weight: 500;
}

.card-content ul {
  list-style: none;
  padding: 0;
}

.card-content li {
  margin: 10px 0;
  padding-left: 20px;
  position: relative;
}

.card-content li::before {
  content: "•";
  color: #1890ff;
  position: absolute;
  left: 0;
}

.el-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.el-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.button {
  display: flex;
  align-items: center;
  gap: 5px;
}

:deep(.el-carousel__item) {
  overflow: hidden;
}
</style> 