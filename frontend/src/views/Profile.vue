<template>
  <div class="profile">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人资料</h2>
          <el-button 
            type="primary"
            :loading="saving"
            @click="handleSave"
          >
            保存修改
          </el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="profileForm"
        :rules="rules"
        label-width="100px"
      >
        <!-- 头像上传 -->
        <el-form-item label="头像">
          <div class="avatar-upload">
            <el-avatar
              :size="100"
              :src="profileForm.avatar || defaultAvatar"
              class="avatar-preview"
            />
            <div class="upload-actions">
              <el-upload
                class="avatar-uploader"
                action="#"
                :show-file-list="false"
                :before-upload="beforeAvatarUpload"
                :http-request="handleAvatarUpload"
              >
                <el-button type="primary">更换头像</el-button>
              </el-upload>
              <p class="upload-tip">支持 jpg、png 格式，文件小于 2MB</p>
            </div>
          </div>
        </el-form-item>

        <!-- 基本信息 -->
        <el-form-item label="用户名" prop="username">
          <el-input v-model="profileForm.username" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profileForm.email" />
        </el-form-item>

        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="profileForm.nickname" />
        </el-form-item>

        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="profileForm.bio"
            type="textarea"
            :rows="4"
            placeholder="介绍一下你自己..."
          />
        </el-form-item>

        <!-- 安全设置 -->
        <div class="section-title">安全设置</div>

        <el-form-item label="原密码" prop="oldPassword">
          <el-input
            v-model="profileForm.oldPassword"
            type="password"
            show-password
            placeholder="请输入原密码"
          />
        </el-form-item>

        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="profileForm.newPassword"
            type="password"
            show-password
            placeholder="请输入新密码"
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="profileForm.confirmPassword"
            type="password"
            show-password
            placeholder="请再次输入新密码"
          />
        </el-form-item>

        <!-- 通知设置 -->
        <div class="section-title">通知设置</div>

        <el-form-item label="系统通知">
          <el-switch v-model="profileForm.notifications.system" />
        </el-form-item>

        <el-form-item label="课程更新">
          <el-switch v-model="profileForm.notifications.course" />
        </el-form-item>

        <el-form-item label="实验提醒">
          <el-switch v-model="profileForm.notifications.lab" />
        </el-form-item>

        <el-form-item label="邮件订阅">
          <el-switch v-model="profileForm.notifications.email" />
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 学习统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <h2>学习统计</h2>
          <el-radio-group v-model="statsRange" size="small">
            <el-radio-button label="week">本周</el-radio-button>
            <el-radio-button label="month">本月</el-radio-button>
            <el-radio-button label="year">全年</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <div class="stats-grid">
        <div class="stats-item">
          <div class="stats-value">{{ stats.courseCount }}</div>
          <div class="stats-label">学习课程</div>
        </div>
        <div class="stats-item">
          <div class="stats-value">{{ stats.labCount }}</div>
          <div class="stats-label">完成实验</div>
        </div>
        <div class="stats-item">
          <div class="stats-value">{{ stats.studyTime }}h</div>
          <div class="stats-label">学习时长</div>
        </div>
        <div class="stats-item">
          <div class="stats-value">{{ stats.points }}</div>
          <div class="stats-label">积分</div>
        </div>
      </div>

      <div class="stats-chart">
        <div ref="chartRef" class="chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import * as echarts from 'echarts'

export default defineComponent({
  name: 'Profile',
  setup() {
    const formRef = ref<FormInstance>()
    const saving = ref(false)
    const statsRange = ref('week')
    const chartRef = ref<HTMLElement>()
    const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
    
    // 表单数据
    const profileForm = ref({
      avatar: '',
      username: 'johndoe',
      email: 'john@example.com',
      nickname: 'John Doe',
      bio: '热爱网络安全技术，致力于学习和分享安全知识。',
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      notifications: {
        system: true,
        course: true,
        lab: true,
        email: false
      }
    })
    
    // 统计数据
    const stats = ref({
      courseCount: 12,
      labCount: 25,
      studyTime: 48,
      points: 1280
    })
    
    // 表单验证规则
    const validatePass = (rule: any, value: string, callback: any) => {
      if (value === '') {
        callback(new Error('请输入新密码'))
      } else {
        if (profileForm.value.confirmPassword !== '') {
          if (formRef.value) {
            formRef.value.validateField('confirmPassword', () => null)
          }
        }
        callback()
      }
    }
    
    const validatePass2 = (rule: any, value: string, callback: any) => {
      if (value === '') {
        callback(new Error('请再次输入新密码'))
      } else if (value !== profileForm.value.newPassword) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    
    const rules: FormRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      nickname: [
        { required: true, message: '请输入昵称', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      bio: [
        { max: 200, message: '不能超过 200 个字符', trigger: 'blur' }
      ],
      newPassword: [
        { validator: validatePass, trigger: 'blur' }
      ],
      confirmPassword: [
        { validator: validatePass2, trigger: 'blur' }
      ]
    }
    
    // 头像上传前的校验
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
    
    // 处理头像上传
    const handleAvatarUpload = async (options: any) => {
      try {
        // TODO: 调用上传API
        await new Promise(resolve => setTimeout(resolve, 1000))
        profileForm.value.avatar = URL.createObjectURL(options.file)
        ElMessage.success('头像上传成功')
      } catch (error) {
        ElMessage.error('头像上传失败')
      }
    }
    
    // 保存修改
    const handleSave = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid, fields) => {
        if (valid) {
          try {
            saving.value = true
            // TODO: 调用保存API
            await new Promise(resolve => setTimeout(resolve, 1000))
            ElMessage.success('保存成功')
          } catch (error) {
            ElMessage.error('保存失败')
          } finally {
            saving.value = false
          }
        }
      })
    }
    
    // 初始化图表
    const initChart = () => {
      if (!chartRef.value) return
      
      const chart = echarts.init(chartRef.value)
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '学习时长',
            type: 'line',
            smooth: true,
            data: [3, 2.5, 4, 3.5, 5, 3, 4],
            areaStyle: {
              opacity: 0.1
            },
            lineStyle: {
              width: 3
            },
            itemStyle: {
              color: '#1890ff'
            }
          }
        ]
      }
      
      chart.setOption(option)
    }
    
    onMounted(() => {
      initChart()
    })
    
    return {
      formRef,
      saving,
      statsRange,
      chartRef,
      defaultAvatar,
      profileForm,
      stats,
      rules,
      beforeAvatarUpload,
      handleAvatarUpload,
      handleSave
    }
  }
})
</script>

<style scoped>
.profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.profile-card,
.stats-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.avatar-upload {
  display: flex;
  gap: 24px;
  align-items: center;
}

.avatar-preview {
  flex-shrink: 0;
}

.upload-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.upload-tip {
  margin: 0;
  font-size: 12px;
  color: var(--text-color-secondary);
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color);
  margin: 24px 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stats-item {
  text-align: center;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 8px;
}

.stats-label {
  font-size: 14px;
  color: var(--text-color-secondary);
}

.stats-chart {
  margin-top: 24px;
}

.chart {
  width: 100%;
  height: 300px;
}

@media (max-width: 768px) {
  .profile {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style> 