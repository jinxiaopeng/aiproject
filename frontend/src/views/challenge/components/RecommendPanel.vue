<template>
  <div class="recommend-panel">
    <!-- 相关题目推荐 -->
    <div class="recommend-section">
      <h3>相关题目推荐</h3>
      <el-row :gutter="20">
        <el-col :span="8" v-for="challenge in relatedChallenges" :key="challenge.id">
          <el-card class="challenge-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>{{ challenge.title }}</span>
                <el-tag size="small" :type="challenge.difficulty">
                  {{ challenge.difficultyLabel }}
                </el-tag>
              </div>
            </template>
            <div class="card-content">
              <p class="description">{{ challenge.description }}</p>
              <div class="tags">
                <el-tag 
                  v-for="tag in challenge.tags" 
                  :key="tag"
                  size="small"
                  effect="plain"
                >
                  {{ tag }}
                </el-tag>
              </div>
              <div class="card-footer">
                <span class="points">{{ challenge.points }} pts</span>
                <el-button type="primary" link @click="startChallenge(challenge.id)">
                  开始挑战
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 进阶学习路径 -->
    <div class="learning-path">
      <h3>进阶学习路径</h3>
      <el-steps :active="currentStep" finish-status="success">
        <el-step 
          v-for="step in learningPath" 
          :key="step.id"
          :title="step.title"
          :description="step.description"
        >
          <template #icon>
            <el-icon>
              <component :is="step.icon" />
            </el-icon>
          </template>
        </el-step>
      </el-steps>
    </div>

    <!-- 技能提升建议 -->
    <div class="skill-suggestions">
      <h3>技能提升建议</h3>
      <el-collapse>
        <el-collapse-item
          v-for="skill in skillSuggestions"
          :key="skill.id"
          :title="skill.name"
          :name="skill.id"
        >
          <div class="skill-content">
            <div class="skill-progress">
              <span class="label">当前水平</span>
              <el-progress 
                :percentage="skill.currentLevel"
                :color="getProgressColor(skill.currentLevel)"
              />
            </div>
            <div class="skill-tips">
              <h4>提升建议：</h4>
              <ul>
                <li v-for="(tip, index) in skill.tips" :key="index">
                  {{ tip }}
                </li>
              </ul>
            </div>
            <div class="skill-resources">
              <h4>推荐资源：</h4>
              <el-button 
                v-for="resource in skill.resources"
                :key="resource.id"
                type="primary"
                link
                @click="openResource(resource.url)"
              >
                {{ resource.name }}
              </el-button>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 相关题目数据
const relatedChallenges = ref([
  {
    id: 1,
    title: 'SQL注入进阶',
    difficulty: 'warning',
    difficultyLabel: '中等',
    description: '深入学习SQL注入的高级技巧',
    tags: ['SQL注入', '数据库安全'],
    points: 200
  },
  {
    id: 2,
    title: 'NoSQL注入基础',
    difficulty: 'success',
    difficultyLabel: '简单',
    description: '学习NoSQL数据库的基本注入技术',
    tags: ['NoSQL', 'MongoDB'],
    points: 150
  }
])

// 学习路径数据
const learningPath = ref([
  {
    id: 1,
    title: 'SQL注入基础',
    description: '掌握基本注入技术',
    icon: 'Edit'
  },
  {
    id: 2,
    title: '高级SQL注入',
    description: '学习盲注和时间注入',
    icon: 'Setting'
  },
  {
    id: 3,
    title: '防护技术',
    description: '学习SQL注入防御方法',
    icon: 'Shield'
  }
])

const currentStep = ref(1)

// 技能提升建议
const skillSuggestions = ref([
  {
    id: 1,
    name: 'SQL注入技能',
    currentLevel: 65,
    tips: [
      '练习更多的盲注技术',
      '学习时间注入方法',
      '掌握WAF绕过技术'
    ],
    resources: [
      { id: 1, name: 'SQL注入进阶教程', url: '/courses/sql-advanced' },
      { id: 2, name: 'WAF绕过技术', url: '/courses/waf-bypass' }
    ]
  },
  {
    id: 2,
    name: '数据库安全',
    currentLevel: 45,
    tips: [
      '学习数据库安全配置',
      '了解权限管理最佳实践',
      '掌握数据库审计技术'
    ],
    resources: [
      { id: 3, name: '数据库安全课程', url: '/courses/db-security' },
      { id: 4, name: '安全配���指南', url: '/guides/security-config' }
    ]
  }
])

// 进度条颜色
const getProgressColor = (percentage: number) => {
  if (percentage < 30) return '#f56c6c'
  if (percentage < 70) return '#e6a23c'
  return '#67c23a'
}

// 开始挑战
const startChallenge = (id: number) => {
  router.push(`/challenge/${id}`)
}

// 打开资源链接
const openResource = (url: string) => {
  router.push(url)
}
</script>

<style scoped>
.recommend-panel {
  padding: 20px;
}

.recommend-section,
.learning-path,
.skill-suggestions {
  margin-bottom: 30px;
}

h3 {
  margin-bottom: 20px;
  color: var(--el-text-color-primary);
}

.challenge-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.description {
  margin: 10px 0;
  color: var(--el-text-color-regular);
}

.tags {
  margin: 10px 0;
}

.tags .el-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.points {
  color: var(--el-color-primary);
  font-weight: bold;
}

.skill-content {
  padding: 10px;
}

.skill-progress {
  margin-bottom: 15px;
}

.skill-progress .label {
  display: block;
  margin-bottom: 5px;
  color: var(--el-text-color-secondary);
}

.skill-tips,
.skill-resources {
  margin-top: 15px;
}

.skill-tips h4,
.skill-resources h4 {
  margin-bottom: 10px;
  color: var(--el-text-color-primary);
}

.skill-tips ul {
  padding-left: 20px;
  color: var(--el-text-color-regular);
}

.skill-resources .el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}
</style> 