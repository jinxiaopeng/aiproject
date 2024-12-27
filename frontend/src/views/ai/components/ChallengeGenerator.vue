<template>
  <div class="challenge-generator">
    <el-form :model="form" label-width="100px">
      <el-form-item label="难度">
        <el-select v-model="form.difficulty" placeholder="选择难度" style="width: 100%">
          <el-option v-for="item in difficulties" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="类型">
        <el-select v-model="form.category" placeholder="选择类型" style="width: 100%">
          <el-option v-for="item in categories" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="知识点">
        <el-select v-model="form.skills" multiple placeholder="选择相关知识点" style="width: 100%">
          <el-option v-for="item in skillOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="generateChallenge" :loading="loading">生成题目</el-button>
      </el-form-item>
    </el-form>

    <div v-if="challenge" class="challenge-result">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>{{ challenge.title }}</span>
            <el-tag :type="getDifficultyType">{{ form.difficulty }}</el-tag>
          </div>
        </template>
        
        <div class="challenge-content">
          <div class="description">
            <h4>题目描述</h4>
            <div v-html="formattedDescription"></div>
          </div>

          <div class="hints">
            <h4>提示</h4>
            <el-collapse>
              <el-collapse-item v-for="(hint, index) in challenge.hints" :key="index" :title="'提示 ' + (index + 1)">
                {{ hint }}
              </el-collapse-item>
            </el-collapse>
          </div>

          <div class="resources" v-if="challenge.resources">
            <h4>相关资源</h4>
            <el-table :data="challenge.resources" style="width: 100%">
              <el-table-column prop="name" label="资源名称" />
              <el-table-column prop="type" label="类型" width="100" />
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button type="primary" link @click="openResource(scope.row)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAiStore } from '@/stores/ai'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

const aiStore = useAiStore()
const loading = ref(false)
const challenge = ref<any>(null)

const form = ref({
  difficulty: '',
  category: '',
  skills: []
})

const difficulties = [
  { label: '入门', value: 'beginner' },
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' },
  { label: '专家', value: 'expert' }
]

const categories = [
  { label: 'Web安全', value: 'web' },
  { label: '系统安全', value: 'system' },
  { label: '密码学', value: 'crypto' },
  { label: '逆向工程', value: 'reverse' },
  { label: '二进制漏洞', value: 'pwn' }
]

const skillOptions = [
  { label: 'SQL注入', value: 'sql_injection' },
  { label: 'XSS', value: 'xss' },
  { label: 'CSRF', value: 'csrf' },
  { label: '文件上传', value: 'file_upload' },
  { label: '命令注入', value: 'command_injection' },
  { label: '权限提升', value: 'privilege_escalation' }
]

const getDifficultyType = computed(() => {
  const types: Record<string, string> = {
    beginner: 'info',
    easy: 'success',
    medium: 'warning',
    hard: 'danger',
    expert: 'danger'
  }
  return types[form.value.difficulty] || 'info'
})

const formattedDescription = computed(() => {
  return challenge.value ? marked(challenge.value.description) : ''
})

const generateChallenge = async () => {
  if (!form.value.difficulty || !form.value.category) {
    ElMessage.warning('请选择难度和类型')
    return
  }

  try {
    loading.value = true
    const result = await aiStore.generateChallenge(
      form.value.difficulty,
      form.value.category,
      form.value.skills
    )
    challenge.value = result
    ElMessage.success('题目生成成功')
  } catch (error: any) {
    ElMessage.error(error.message || '生成失败')
  } finally {
    loading.value = false
  }
}

const openResource = (resource: any) => {
  if (resource.url) {
    window.open(resource.url, '_blank')
  } else {
    ElMessage.info('资源暂未开放')
  }
}
</script>

<style lang="scss" scoped>
.challenge-generator {
  padding: 20px;

  .challenge-result {
    margin-top: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .challenge-content {
      .description {
        margin-bottom: 20px;
      }

      .hints {
        margin-bottom: 20px;
      }

      h4 {
        margin-bottom: 10px;
        color: var(--el-text-color-primary);
      }
    }
  }
}
</style> 