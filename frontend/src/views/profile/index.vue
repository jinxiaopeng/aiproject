<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人中心</h2>
        </div>
      </template>
      
      <div class="profile-content">
        <div class="avatar-section">
          <el-avatar :size="100" :src="userInfo?.avatar || defaultAvatar" />
          <el-upload
            class="avatar-uploader"
            action="/api/user/avatar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <el-button size="small" type="primary">更换头像</el-button>
          </el-upload>
        </div>

        <div class="info-section">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="用户名">
              {{ userInfo?.username }}
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ userInfo?.email }}
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
              {{ formatDate(userInfo?.createdAt) }}
            </el-descriptions-item>
            <el-descriptions-item label="最后登录">
              {{ formatDate(userInfo?.lastLoginAt) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const userInfo = computed(() => authStore.userInfo)
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

const formatDate = (date: string | undefined) => {
  if (!date) return '未知'
  return new Date(date).toLocaleString()
}

const handleAvatarSuccess = (response: any) => {
  if (response.code === 0) {
    authStore.updateUserInfo({ ...userInfo.value, avatar: response.data.url })
    ElMessage.success('头像更新成功')
  } else {
    ElMessage.error(response.message || '头像更新失败')
  }
}

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
</script>

<style lang="scss" scoped>
.profile-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h2 {
      margin: 0;
      font-size: 20px;
      color: #303133;
    }
  }
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding: 20px 0;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.info-section {
  :deep(.el-descriptions) {
    width: 100%;
  }
}

.avatar-uploader {
  text-align: center;
}
</style> 