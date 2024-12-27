<template>
  <div class="challenge-progress">
    <!-- 总体进度卡片 -->
    <div class="progress-card cyber-card">
      <div class="card-header">
        <h3>训练进度</h3>
        <div class="progress-circle">
          <el-progress
            type="dashboard"
            :percentage="completionRate"
            :color="progressColor"
            :stroke-width="10"
          >
            <template #default="{ percentage }">
              <div class="progress-info">
                <span class="percentage">{{ percentage }}%</span>
                <span class="label">完成率</span>
              </div>
            </template>
          </el-progress>
        </div>
      </div>

      <!-- 进度统计 -->
      <div class="progress-stats">
        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-value">{{ props.stats.totalChallenges }}</div>
            <div class="stat-label">总靶场数</div>
          </div>
          <div class="stat-item highlight">
            <div class="stat-value">{{ props.stats.completedChallenges }}</div>
            <div class="stat-label">已完成</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ props.stats.inProgressChallenges }}</div>
            <div class="stat-label">进行中</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类进度卡片 -->
    <div class="category-card cyber-card">
      <h3>分类进度</h3>
      <div class="category-list">
        <div 
          v-for="category in categoryProgress" 
          :key="category.name"
          class="category-item"
        >
          <div class="category-header">
            <span class="category-name">{{ category.name }}</span>
            <span class="category-ratio">{{ category.completed }}/{{ category.total }}</span>
          </div>
          <el-progress 
            :percentage="(category.completed / category.total) * 100"
            :color="category.color"
            :stroke-width="8"
            :show-text="false"
          />
        </div>
      </div>
    </div>

    <!-- 最近完成卡片 -->
    <div class="recent-card cyber-card">
      <h3>最近完成</h3>
      <div class="timeline-container">
        <el-timeline>
          <el-timeline-item
            v-for="item in recentCompleted"
            :key="item.id"
            :type="item.type"
            :color="item.color"
            :timestamp="item.completedAt"
          >
            <div class="timeline-content">
              <div class="challenge-title">{{ item.title }}</div>
              <div class="challenge-points">+{{ item.points }} pts</div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>

    <!-- 成就卡片 -->
    <div class="achievements-card cyber-card">
      <h3>成就</h3>
      <div class="achievements-grid">
        <div 
          v-for="achievement in achievements" 
          :key="achievement.id"
          class="achievement-item"
          :class="{ 'unlocked': achievement.unlocked }"
        >
          <div class="achievement-icon">
            <component :is="achievement.icon" />
            <div class="achievement-glow"></div>
          </div>
          <div class="achievement-name">{{ achievement.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  Trophy,
  Medal,
  Star,
  Lightning,
  Cpu,
  Key,
  Lock,
  Unlock
} from '@element-plus/icons-vue'

interface Props {
  stats: {
    totalChallenges: number
    completedChallenges: number
    inProgressChallenges: number
    totalPoints: number
  }
}

const props = defineProps<Props>()

// 计算完成率
const completionRate = computed(() => {
  return Math.round((props.stats.completedChallenges / props.stats.totalChallenges) * 100)
})

// 进度颜色
const progressColor = computed(() => {
  if (completionRate.value < 30) return '#f56c6c'
  if (completionRate.value < 70) return '#e6a23c'
  return '#67c23a'
})

// 分类进度数据
const categoryProgress = ref([
  {
    name: 'Web安全',
    completed: 8,
    total: 20,
    color: '#409eff'
  },
  {
    name: '系统安全',
    completed: 3,
    total: 10,
    color: '#67c23a'
  },
  {
    name: '密码学',
    completed: 2,
    total: 8,
    color: '#e6a23c'
  },
  {
    name: '逆向工程',
    completed: 1,
    total: 7,
    color: '#f56c6c'
  },
  {
    name: '二进制',
    completed: 1,
    total: 5,
    color: '#909399'
  }
])

// 最近完成数据
const recentCompleted = ref([
  {
    id: 1,
    title: 'SQL注入基础训练',
    points: 100,
    completedAt: '2023-12-15 14:30',
    type: 'success',
    color: '#67c23a'
  },
  {
    id: 2,
    title: 'XSS跨站脚本攻击',
    points: 150,
    completedAt: '2023-12-14 16:20',
    type: 'primary',
    color: '#409eff'
  },
  {
    id: 3,
    title: '基础密码学挑战',
    points: 80,
    completedAt: '2023-12-13 09:45',
    type: 'warning',
    color: '#e6a23c'
  }
])

// 成就数据
const achievements = ref([
  {
    id: 1,
    name: '初出茅庐',
    description: '完成第一个靶场训练',
    icon: Trophy,
    unlocked: true
  },
  {
    id: 2,
    name: '坚持不懈',
    description: '连续7天完成训练',
    icon: Medal,
    unlocked: true
  },
  {
    id: 3,
    name: '全能选手',
    description: '每个分类至少完成一个靶场',
    icon: Star,
    unlocked: false
  },
  {
    id: 4,
    name: '速战速决',
    description: '30分钟内完成一个高难度靶场',
    icon: Lightning,
    unlocked: false
  },
  {
    id: 5,
    name: '系统专家',
    description: '完成所有系统安全靶场',
    icon: Cpu,
    unlocked: false
  },
  {
    id: 6,
    name: '密码大师',
    description: '完成所有密码学靶场',
    icon: Key,
    unlocked: false
  }
])
</script>

<style scoped lang="scss">
.challenge-progress {
  .cyber-card {
    background: var(--card-background);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px var(--glow-color);

    h3 {
      margin: 0 0 20px;
      color: var(--text-color);
      font-size: 18px;
      font-weight: 600;
    }

    &:hover {
      border-color: var(--primary-color);
      box-shadow: 0 0 30px var(--glow-color);
    }
  }

  // 总体进度卡片
  .progress-card {
    .card-header {
      text-align: center;
    }

    .progress-circle {
      margin: 20px 0;

      :deep(.el-progress) {
        --el-progress-bg-color: rgba(255, 255, 255, 0.1);
      }

      .progress-info {
        display: flex;
        flex-direction: column;
        align-items: center;

        .percentage {
          font-size: 24px;
          font-weight: bold;
          color: var(--primary-color);
        }

        .label {
          font-size: 14px;
          color: var(--text-secondary);
          margin-top: 5px;
        }
      }
    }

    .progress-stats {
      .stat-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
      }

      .stat-item {
        text-align: center;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        transition: transform 0.3s ease;

        &:hover {
          transform: translateY(-3px);
        }

        &.highlight {
          background: rgba(0, 255, 157, 0.1);

          .stat-value {
            color: var(--primary-color);
          }
        }

        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: var(--text-color);
        }

        .stat-label {
          font-size: 12px;
          color: var(--text-secondary);
          margin-top: 5px;
        }
      }
    }
  }

  // 分类进度卡片
  .category-card {
    .category-list {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }

    .category-item {
      .category-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        color: var(--text-secondary);
        font-size: 14px;
      }

      :deep(.el-progress-bar__outer) {
        background-color: rgba(255, 255, 255, 0.1) !important;
      }
    }
  }

  // 最近完成卡片
  .recent-card {
    .timeline-container {
      padding: 0 10px;
      max-height: 300px;
      overflow-y: auto;

      &::-webkit-scrollbar {
        width: 4px;
      }

      &::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
      }

      &::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 2px;
      }
    }

    :deep(.el-timeline) {
      --el-timeline-node-size: 12px;

      .el-timeline-item__node {
        background-color: var(--el-color-primary);
      }

      .el-timeline-item__tail {
        border-left-color: rgba(255, 255, 255, 0.1);
      }

      .el-timeline-item__content {
        color: var(--text-color);
      }

      .el-timeline-item__timestamp {
        color: var(--text-secondary);
      }
    }

    .timeline-content {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .challenge-title {
        font-weight: 500;
      }

      .challenge-points {
        color: #67c23a;
        font-size: 14px;
      }
    }
  }

  // 成就卡片
  .achievements-card {
    .achievements-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 15px;
    }

    .achievement-item {
      text-align: center;
      padding: 15px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-3px);

        &:not(.unlocked) .achievement-glow {
          opacity: 1;
        }
      }

      &.unlocked {
        opacity: 0.5;

        .achievement-icon {
          color: var(--text-secondary);
        }
      }

      .achievement-icon {
        position: relative;
        display: inline-flex;
        padding: 15px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        color: var(--primary-color);
        margin-bottom: 10px;

        .achievement-glow {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          border-radius: 50%;
          background: radial-gradient(circle at center, var(--primary-color) 0%, transparent 70%);
          opacity: 0;
          transition: opacity 0.3s ease;
        }
      }

      .achievement-name {
        font-size: 12px;
        color: var(--text-color);
      }
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .challenge-progress {
    .achievements-card {
      .achievements-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
  }
}
</style> 