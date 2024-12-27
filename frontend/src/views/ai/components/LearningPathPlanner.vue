<template>
  <div class="learning-path-planner">
    <el-form :model="form" label-width="100px">
      <el-form-item label="目标技能">
        <el-cascader
          v-model="form.targetSkill"
          :options="skillTree"
          :props="{ checkStrictly: true }"
          placeholder="选择目标技能"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item label="当前水平">
        <el-select v-model="form.currentLevel" placeholder="选择当前水平" style="width: 100%">
          <el-option v-for="item in levels" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="学习时间">
        <el-select v-model="form.timeCommitment" placeholder="每周可投入时间" style="width: 100%">
          <el-option v-for="item in timeOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="generatePath" :loading="loading">生成学习路径</el-button>
      </el-form-item>
    </el-form>

    <div v-if="learningPath" class="learning-path-result">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>个性化学习路径</span>
            <el-tag type="success">预计完成时间: {{ learningPath.estimatedTime }}</el-tag>
          </div>
        </template>

        <div class="path-content">
          <el-timeline>
            <el-timeline-item
              v-for="(stage, index) in learningPath.stages"
              :key="index"
              :type="getStageType(stage.status)"
              :color="getStageColor(stage.status)"
              :timestamp="stage.duration"
            >
              <h4>{{ stage.title }}</h4>
              <p class="stage-description">{{ stage.description }}</p>
              
              <div class="stage-skills">
                <el-tag
                  v-for="skill in stage.skills"
                  :key="skill"
                  size="small"
                  style="margin-right: 5px"
                >
                  {{ skill }}
                </el-tag>
              </div>

              <div class="stage-resources" v-if="stage.resources">
                <h5>学习资源</h5>
                <el-collapse>
                  <el-collapse-item title="查看资源">
                    <el-table :data="stage.resources" style="width: 100%">
                      <el-table-column prop="name" label="资源名称" />
                      <el-table-column prop="type" label="类型" width="100" />
                      <el-table-column prop="difficulty" label="难度" width="100" />
                      <el-table-column label="操作" width="150">
                        <template #default="scope">
                          <el-button type="primary" link @click="openResource(scope.row)">
                            开始学习
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-collapse-item>
                </el-collapse>
              </div>
            </el-timeline-item>
          </el-timeline>

          <div class="progress-tracking" v-if="learningPath.progress">
            <h4>学习进度</h4>
            <el-progress
              :percentage="learningPath.progress.percentage"
              :status="getProgressStatus(learningPath.progress.percentage)"
            />
            <div class="progress-stats">
              <div class="stat-item">
                <span class="label">已完成课程</span>
                <span class="value">{{ learningPath.progress.completedCourses }}</span>
              </div>
              <div class="stat-item">
                <span class="label">学习时长</span>
                <span class="value">{{ learningPath.progress.totalHours }}小时</span>
              </div>
              <div class="stat-item">
                <span class="label">获得积分</span>
                <span class="value">{{ learningPath.progress.points }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAiStore } from '@/stores/ai'
import { ElMessage } from 'element-plus'

const aiStore = useAiStore()
const loading = ref(false)
const learningPath = ref<any>(null)

const form = ref({
  targetSkill: [],
  currentLevel: '',
  timeCommitment: ''
})

const skillTree = [
  {
    value: 'web_security',
    label: 'Web安全',
    children: [
      {
        value: 'web_pentest',
        label: 'Web渗透测试',
        children: [
          { value: 'sql_injection', label: 'SQL注入' },
          { value: 'xss', label: 'XSS跨站脚本' },
          { value: 'csrf', label: 'CSRF跨站请求伪造' }
        ]
      },
      {
        value: 'secure_development',
        label: '安全开发',
        children: [
          { value: 'input_validation', label: '输入验证' },
          { value: 'authentication', label: '身份认证' },
          { value: 'authorization', label: '访问控制' }
        ]
      }
    ]
  },
  {
    value: 'system_security',
    label: '系统安全',
    children: [
      {
        value: 'system_pentest',
        label: '系统渗透测试',
        children: [
          { value: 'privilege_escalation', label: '权限提升' },
          { value: 'remote_execution', label: '远程执行' }
        ]
      }
    ]
  }
]

const levels = [
  { label: '入门新手', value: 'beginner' },
  { label: '初级学习者', value: 'elementary' },
  { label: '中级实践者', value: 'intermediate' },
  { label: '高级专家', value: 'advanced' }
]

const timeOptions = [
  { label: '每周5小时以下', value: 'very_low' },
  { label: '每周5-10小时', value: 'low' },
  { label: '每周10-20小时', value: 'medium' },
  { label: '每周20小时以上', value: 'high' }
]

const getStageType = (status: string) => {
  const types: Record<string, string> = {
    completed: 'success',
    in_progress: 'primary',
    pending: 'info'
  }
  return types[status] || 'info'
}

const getStageColor = (status: string) => {
  const colors: Record<string, string> = {
    completed: '#67C23A',
    in_progress: '#409EFF',
    pending: '#909399'
  }
  return colors[status] || '#909399'
}

const getProgressStatus = (percentage: number) => {
  if (percentage >= 100) return 'success'
  if (percentage >= 50) return 'primary'
  return 'normal'
}

const generatePath = async () => {
  if (!form.value.targetSkill.length || !form.value.currentLevel || !form.value.timeCommitment) {
    ElMessage.warning('请完整填写学习计划信息')
    return
  }

  try {
    loading.value = true
    const result = await aiStore.generateLearningPath(
      form.value.targetSkill[form.value.targetSkill.length - 1],
      form.value.currentLevel,
      form.value.timeCommitment
    )
    learningPath.value = result
    ElMessage.success('学习路径生成成功')
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
.learning-path-planner {
  padding: 20px;

  .learning-path-result {
    margin-top: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .path-content {
      .stage-description {
        margin: 10px 0;
        color: var(--el-text-color-regular);
      }

      .stage-skills {
        margin: 10px 0;
      }

      .stage-resources {
        margin-top: 15px;
        
        h5 {
          margin-bottom: 10px;
          color: var(--el-text-color-primary);
        }
      }

      .progress-tracking {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid var(--el-border-color-lighter);

        h4 {
          margin-bottom: 15px;
        }

        .progress-stats {
          margin-top: 20px;
          display: flex;
          justify-content: space-around;

          .stat-item {
            text-align: center;

            .label {
              display: block;
              color: var(--el-text-color-secondary);
              font-size: 14px;
            }

            .value {
              display: block;
              margin-top: 5px;
              font-size: 20px;
              font-weight: bold;
              color: var(--el-color-primary);
            }
          }
        }
      }
    }
  }
}
</style> 