<template>
  <div class="system-settings">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <span>系统设置</span>
          <el-button type="primary" @click="handleSave">
            保存设置
          </el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="140px"
        class="settings-form"
      >
        <!-- 基础设置 -->
        <el-divider>基础设置</el-divider>
        <el-form-item label="系统名称" prop="siteName">
          <el-input v-model="form.siteName" />
        </el-form-item>
        <el-form-item label="系统描述" prop="siteDescription">
          <el-input v-model="form.siteDescription" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="系统Logo">
          <el-upload
            class="logo-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleLogoSuccess"
            :before-upload="beforeLogoUpload"
          >
            <img v-if="form.logo" :src="form.logo" class="logo" />
            <el-icon v-else class="logo-uploader-icon"><plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="ICP备案号" prop="icp">
          <el-input v-model="form.icp" />
        </el-form-item>

        <!-- 安全设置 -->
        <el-divider>安全设置</el-divider>
        <el-form-item label="密码最小长度" prop="passwordMinLength">
          <el-input-number v-model="form.passwordMinLength" :min="6" :max="32" />
        </el-form-item>
        <el-form-item label="密码复杂度要求">
          <el-checkbox-group v-model="form.passwordRequirements">
            <el-checkbox label="uppercase">必须包含大写字母</el-checkbox>
            <el-checkbox label="lowercase">必须包含小写字母</el-checkbox>
            <el-checkbox label="number">必须包含数字</el-checkbox>
            <el-checkbox label="special">必须包含特殊字符</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="登录失败锁定">
          <div class="lock-settings">
            <el-input-number 
              v-model="form.loginMaxAttempts" 
              :min="3" 
              :max="10"
              placeholder="尝试次数"
            />
            <el-input-number 
              v-model="form.loginLockTime" 
              :min="5" 
              :max="60"
              placeholder="锁定时间(分钟)"
            />
          </div>
        </el-form-item>
        <el-form-item label="会话超时时间" prop="sessionTimeout">
          <el-input-number 
            v-model="form.sessionTimeout" 
            :min="15" 
            :max="1440"
            placeholder="超时时间(分钟)"
          />
        </el-form-item>

        <!-- 邮件设置 -->
        <el-divider>邮件设置</el-divider>
        <el-form-item label="SMTP服务器" prop="smtpHost">
          <el-input v-model="form.smtpHost" />
        </el-form-item>
        <el-form-item label="SMTP端口" prop="smtpPort">
          <el-input-number v-model="form.smtpPort" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item label="发件人邮箱" prop="smtpEmail">
          <el-input v-model="form.smtpEmail" />
        </el-form-item>
        <el-form-item label="发件人密码" prop="smtpPassword">
          <el-input v-model="form.smtpPassword" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleTestEmail">
            测试邮件发送
          </el-button>
        </el-form-item>

        <!-- 存储设置 -->
        <el-divider>存储设置</el-divider>
        <el-form-item label="存储类型" prop="storageType">
          <el-radio-group v-model="form.storageType">
            <el-radio label="local">本地存储</el-radio>
            <el-radio label="oss">阿里云OSS</el-radio>
            <el-radio label="cos">腾讯云COS</el-radio>
          </el-radio-group>
        </el-form-item>
        <template v-if="form.storageType === 'oss'">
          <el-form-item label="OSS AccessKey" prop="ossAccessKey">
            <el-input v-model="form.ossAccessKey" />
          </el-form-item>
          <el-form-item label="OSS SecretKey" prop="ossSecretKey">
            <el-input v-model="form.ossSecretKey" type="password" show-password />
          </el-form-item>
          <el-form-item label="OSS Bucket" prop="ossBucket">
            <el-input v-model="form.ossBucket" />
          </el-form-item>
          <el-form-item label="OSS Region" prop="ossRegion">
            <el-input v-model="form.ossRegion" />
          </el-form-item>
        </template>
        <template v-if="form.storageType === 'cos'">
          <el-form-item label="COS SecretId" prop="cosSecretId">
            <el-input v-model="form.cosSecretId" />
          </el-form-item>
          <el-form-item label="COS SecretKey" prop="cosSecretKey">
            <el-input v-model="form.cosSecretKey" type="password" show-password />
          </el-form-item>
          <el-form-item label="COS Bucket" prop="cosBucket">
            <el-input v-model="form.cosBucket" />
          </el-form-item>
          <el-form-item label="COS Region" prop="cosRegion">
            <el-input v-model="form.cosRegion" />
          </el-form-item>
        </template>

        <!-- 其他设置 -->
        <el-divider>其他设置</el-divider>
        <el-form-item label="开启注册" prop="enableRegister">
          <el-switch v-model="form.enableRegister" />
        </el-form-item>
        <el-form-item label="开启评论" prop="enableComment">
          <el-switch v-model="form.enableComment" />
        </el-form-item>
        <el-form-item label="开启实验环境" prop="enableLab">
          <el-switch v-model="form.enableLab" />
        </el-form-item>
        <el-form-item label="开启AI助手" prop="enableAI">
          <el-switch v-model="form.enableAI" />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

// 表单数据
const form = ref({
  siteName: 'Web安全智能学习平台',
  siteDescription: '一个专注于Web安全学习的智能平台',
  logo: '',
  icp: '',
  passwordMinLength: 8,
  passwordRequirements: ['uppercase', 'number'],
  loginMaxAttempts: 5,
  loginLockTime: 30,
  sessionTimeout: 120,
  smtpHost: '',
  smtpPort: 465,
  smtpEmail: '',
  smtpPassword: '',
  storageType: 'local',
  ossAccessKey: '',
  ossSecretKey: '',
  ossBucket: '',
  ossRegion: '',
  cosSecretId: '',
  cosSecretKey: '',
  cosBucket: '',
  cosRegion: '',
  enableRegister: true,
  enableComment: true,
  enableLab: true,
  enableAI: true
})

// 表单验证规则
const rules: FormRules = {
  siteName: [
    { required: true, message: '请输入系统名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  siteDescription: [
    { required: true, message: '请输入系统描述', trigger: 'blur' }
  ],
  passwordMinLength: [
    { required: true, message: '请设置密码最小长度', trigger: 'blur' }
  ],
  smtpHost: [
    { required: true, message: '请输入SMTP服务器地址', trigger: 'blur' }
  ],
  smtpPort: [
    { required: true, message: '请输入SMTP端口', trigger: 'blur' }
  ],
  smtpEmail: [
    { required: true, message: '请输入发件人邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  smtpPassword: [
    { required: true, message: '请输入发件人密码', trigger: 'blur' }
  ]
}

const formRef = ref<FormInstance>()

// 事件处理函数
const handleSave = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid, fields) => {
    if (valid) {
      // TODO: 调用保存API
      ElMessage.success('保存成功')
    }
  })
}

const handleTestEmail = () => {
  // TODO: 调用测试邮件API
  ElMessage.success('测试邮件已发送')
}

const handleLogoSuccess = (res: any, file: File) => {
  form.value.logo = res.url
}

const beforeLogoUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}
</script>

<style scoped>
.system-settings {
  padding: 24px;
}

.settings-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.settings-form {
  max-width: 800px;
  margin: 0 auto;
}

.logo-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.logo-uploader:hover {
  border-color: var(--el-color-primary);
}

.logo-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}

.logo {
  width: 178px;
  height: 100px;
  display: block;
}

.lock-settings {
  display: flex;
  gap: 16px;
  align-items: center;
}

.lock-settings .el-input-number {
  width: 120px;
}

:deep(.el-divider__text) {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}
</style> 