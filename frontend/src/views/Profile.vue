<template>
  <div class="profile-page">
    <div class="profile-header">
      <div class="header-content">
        <div class="user-info">
          <div class="avatar-wrapper">
            <el-avatar 
              :size="100" 
              :src="userStore.userInfo?.avatar"
              @click="handleAvatarClick"
            >
              {{ userStore.userInfo?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            <div class="avatar-edit">
              <i class="el-icon-camera"></i>
            </div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleFileChange"
            >
          </div>
          <div class="user-details">
            <h1>{{ userStore.userInfo?.username }}</h1>
            <p class="email">{{ userStore.userInfo?.email }}</p>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-value">12</span>
                <span class="stat-label">已学课程</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">5</span>
                <span class="stat-label">完成实验</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">89%</span>
                <span class="stat-label">学习进度</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <el-tabs class="custom-tabs">
        <el-tab-pane label="学习记录">
          <div class="learning-history">
            <div class="section-title">
              <h2>最近学习</h2>
              <el-button type="text">查看全部</el-button>
            </div>
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in learningHistory"
                :key="index"
                :timestamp="activity.time"
                :type="activity.type"
              >
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-tab-pane>

        <el-tab-pane label="我的收藏">
          <div class="favorites">
            <div class="section-title">
              <h2>收藏的课程</h2>
            </div>
            <el-row :gutter="20">
              <el-col :span="8" v-for="(course, index) in favoriteCourses" :key="index">
                <el-card class="course-card" shadow="hover">
                  <img :src="course.cover" class="course-image">
                  <div class="course-info">
                    <h3>{{ course.title }}</h3>
                    <p>{{ course.description }}</p>
                    <el-progress 
                      :percentage="course.progress" 
                      :status="course.progress === 100 ? 'success' : ''"
                    />
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <el-tab-pane label="账号设置">
          <div class="account-settings">
            <el-form 
              :model="settingsForm"
              label-width="100px"
              class="settings-form"
            >
              <el-form-item label="用户名">
                <el-input v-model="settingsForm.username" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="settingsForm.email" />
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input 
                  v-model="settingsForm.bio" 
                  type="textarea" 
                  :rows="4"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveSettings">保存修改</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog
      v-model="cropperVisible"
      title="裁剪头像"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="cropper-container">
        <canvas
          ref="previewCanvas"
          class="preview-canvas"
        ></canvas>
      </div>
      <template #footer>
        <el-button @click="cropperVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCropImage">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../store'

const userStore = useUserStore()
const fileInput = ref<HTMLInputElement | null>(null)
const previewCanvas = ref<HTMLCanvasElement | null>(null)
const cropperVisible = ref(false)
const uploadedImage = ref<HTMLImageElement | null>(null)

// 学习历史数据
const learningHistory = [
  {
    content: '完成 Web安全基础 课程学习',
    time: '2024-01-15 14:30',
    type: 'success'
  },
  {
    content: '参与 SQL注入实验',
    time: '2024-01-14 16:20',
    type: 'primary'
  },
  {
    content: '开始学习 网络安全入门',
    time: '2024-01-13 09:45',
    type: 'info'
  }
]

// 收藏的课程
const favoriteCourses = [
  {
    title: 'Web安全渗透测试',
    description: '系统学习Web安全测试方法',
    cover: '/images/courses/web-security.jpg',
    progress: 80
  },
  {
    title: '网络攻防实战',
    description: '实践网络安全防护技能',
    cover: '/images/courses/network-security.jpg',
    progress: 60
  },
  {
    title: '漏洞挖掘专项班',
    description: '深入学习漏洞挖掘技术',
    cover: '/images/courses/vulnerability.jpg',
    progress: 30
  }
]

// 设置表单
const settingsForm = reactive({
  username: userStore.userInfo?.username || '',
  email: userStore.userInfo?.email || '',
  bio: ''
})

// 处理头像点击
const handleAvatarClick = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  
  if (file) {
    // 检查文件类型
    if (!file.type.includes('image/')) {
      ElMessage.error('请选择图片文件')
      return
    }
    
    // 检查文件大小（2MB）
    if (file.size > 2 * 1024 * 1024) {
      ElMessage.error('图片大小不能超过2MB')
      return
    }
    
    // 读取文件并预览
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        uploadedImage.value = img
        drawPreview()
        cropperVisible.value = true
      }
      img.src = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
  
  // 清除文件选择，以便可以选择相同的文件
  input.value = ''
}

// 绘制预览
const drawPreview = () => {
  if (!previewCanvas.value || !uploadedImage.value) return
  
  const canvas = previewCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  const img = uploadedImage.value
  const size = Math.min(img.width, img.height)
  const x = (img.width - size) / 2
  const y = (img.height - size) / 2
  
  canvas.width = 200
  canvas.height = 200
  
  ctx.fillStyle = '#f8f8f8'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  ctx.drawImage(
    img,
    x, y, size, size,
    0, 0, canvas.width, canvas.height
  )
}

// 处理图片裁剪
const handleCropImage = () => {
  if (!previewCanvas.value) return
  
  try {
    const dataUrl = previewCanvas.value.toDataURL('image/jpeg', 0.8)
    userStore.setUserInfo({
      ...userStore.userInfo!,
      avatar: dataUrl
    })
    
    ElMessage.success('头像更新成功')
    cropperVisible.value = false
  } catch (error) {
    ElMessage.error('图片裁剪失败')
  }
}

// 组件卸载时清理
onUnmounted(() => {
  uploadedImage.value = null
})

// 保存设置
const saveSettings = () => {
  // TODO: 实现保存设置功能
  ElMessage.success('设置已保存')
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.profile-header {
  background: linear-gradient(135deg, #1890ff 0%, #1d39c4 100%);
  padding: 60px 0 40px;
  color: #fff;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 40px;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.avatar-edit {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 32px;
  height: 32px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-wrapper:hover .avatar-edit {
  opacity: 1;
}

.avatar-edit i {
  color: #fff;
  font-size: 16px;
}

.user-details h1 {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px;
}

.email {
  font-size: 16px;
  opacity: 0.8;
  margin: 0 0 20px;
}

.user-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  display: block;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.profile-content {
  max-width: 1200px;
  margin: -30px auto 0;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.custom-tabs {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.course-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.course-card:hover {
  transform: translateY(-4px);
}

.course-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.course-info {
  padding: 16px;
}

.course-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
}

.course-info p {
  font-size: 14px;
  color: #666;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.settings-form {
  max-width: 500px;
}

.cropper-container {
  padding: 20px;
  text-align: center;
  background: #f8f8f8;
  border-radius: 4px;
}

.preview-canvas {
  max-width: 100%;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

@media screen and (max-width: 768px) {
  .user-info {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .user-stats {
    justify-content: center;
  }

  .profile-content {
    padding: 0 16px;
  }
}
</style> 