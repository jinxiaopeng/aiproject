<template>
  <div class="settings-container">
    <el-tabs>
      <!-- 基本信息设置 -->
      <el-tab-pane label="基本信息">
        <el-form
          ref="baseFormRef"
          :model="baseForm"
          :rules="baseRules"
          label-width="100px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="baseForm.username" />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="baseForm.email" />
          </el-form-item>
          
          <el-form-item label="个人简介" prop="bio">
            <el-input
              v-model="baseForm.bio"
              type="textarea"
              :rows="4"
              placeholder="介绍一下你自己..."
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              @click="handleUpdateBase"
            >
              保存修改
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      
      <!-- 安全设置 -->
      <el-tab-pane label="安全设置">
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="100px"
        >
          <el-form-item label="当前密码" prop="oldPassword">
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
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              @click="handleUpdatePassword"
            >
              修改密码
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      
      <!-- 通知设置 -->
      <el-tab-pane label="通知设置">
        <el-form label-width="200px">
          <el-form-item label="课程更新提醒">
            <el-switch v-model="notifySettings.courseUpdate" />
          </el-form-item>
          
          <el-form-item label="实验室状态变更提醒">
            <el-switch v-model="notifySettings.labStatus" />
          </el-form-item>
          
          <el-form-item label="系统公告">
            <el-switch v-model="notifySettings.systemAnnouncement" />
          </el-form-item>
          
          <el-form-item label="接收方式">
            <el-checkbox-group v-model="notifySettings.methods">
              <el-checkbox label="email">邮件通知</el-checkbox>
              <el-checkbox label="web">站内通知</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              @click="handleUpdateNotify"
            >
              保存设置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import request from '@/utils/request'

const authStore = useAuthStore()
const loading = ref(false)

// 表单引用
const baseFormRef = ref()
const passwordFormRef = ref()

// 基本信息表单
const baseForm = reactive({
  username: authStore.userInfo?.username || '',
  email: authStore.userInfo?.email || '',
  bio: authStore.userInfo?.bio || ''
})

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 通知设置
const notifySettings = reactive({
  courseUpdate: true,
  labStatus: true,
  systemAnnouncement: true,
  methods: ['email', 'web']
})

// 基本信息验证规则
const baseRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 密码验证规则
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 更新基本信息
const handleUpdateBase = async () => {
  if (!baseFormRef.value) return
  
  try {
    await baseFormRef.value.validate()
    loading.value = true
    
    await request.put('/user/profile', baseForm)
    ElMessage.success('基本信息更新成功')
    
    // 更新 store 中的用户信息
    await authStore.getUserInfo()
  } catch (error: any) {
    console.error('Update profile error:', error)
    ElMessage.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}

// 更新密码
const handleUpdatePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    loading.value = true
    
    await request.put('/user/password', {
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })
    
    ElMessage.success('密码修改成功，请重新登录')
    authStore.logout()
  } catch (error: any) {
    console.error('Update password error:', error)
    ElMessage.error(error.message || '修改失败')
  } finally {
    loading.value = false
  }
}

// 更新通知设置
const handleUpdateNotify = async () => {
  try {
    loading.value = true
    await request.put('/user/notifications', notifySettings)
    ElMessage.success('通知设置更新成功')
  } catch (error: any) {
    console.error('Update notification settings error:', error)
    ElMessage.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.settings-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  
  .el-form {
    margin-top: 20px;
  }
}
</style> 