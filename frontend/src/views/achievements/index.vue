<template>
  <div class="achievement-page">
    <div class="main-content">
      <!-- 分类标签栏 -->
      <div class="category-nav">
        <div 
          v-for="category in categories" 
          :key="category.key"
          class="category-item"
          :class="{ active: currentCategory === category.key }"
          @click="currentCategory = category.key"
        >
          <el-icon><component :is="getCategoryIcon(category.key)" /></el-icon>
          <span>{{ category.label }}</span>
          <div class="category-progress" v-if="category.key !== 'all'">
            {{ getCategoryProgress(category.key) }}%
          </div>
        </div>
      </div>

      <!-- 分类说明 -->
      <div class="category-header" v-if="currentCategory !== 'all'">
        <div class="category-title">
          <h2>{{ getCurrentCategory.label }}</h2>
          <div class="category-stats">
            <el-progress 
              :percentage="getCategoryProgress(currentCategory)"
              :color="progressColors"
              :stroke-width="4"
              :show-text="false"
            />
            <span class="progress-text">{{ getCategoryProgress(currentCategory) }}% 完成</span>
          </div>
        </div>
        <p class="category-desc">{{ getCurrentCategory.description }}</p>
      </div>

      <!-- 成就列表 -->
      <div class="achievements-grid">
        <achievement-card
          v-for="achievement in currentAchievements"
          :key="achievement.id"
          v-bind="achievement"
          @unlock="handleUnlock"
        />
      </div>

      <!-- 空状态 -->
      <div class="empty-state" v-if="currentAchievements.length === 0">
        <el-empty 
          description="暂无成就" 
          :image-size="200"
        >
          <template #image>
            <el-icon size="60"><Trophy /></el-icon>
          </template>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Trophy, Star, Timer, Medal, Monitor, Lock, ChatDotSquare } from '@element-plus/icons-vue'
import AchievementCard from './components/AchievementCard.vue'

// 当前选中的分类
const currentCategory = ref('all')

// 成就分类
const categories = [
  { 
    key: 'all', 
    label: '全部成就',
    description: '展示所有可获得的成就'
  },
  { 
    key: 'beginner', 
    label: '新手成就',
    description: '适合初学者的基础成就，帮助你熟悉平台的各项功能'
  },
  { 
    key: 'challenge', 
    label: '挑战成就',
    description: '通过完成特定挑战获得的成就，展示你的技术实力'
  },
  { 
    key: 'master', 
    label: '大师成就',
    description: '需要深厚的技术功底和持续的努力才能获得的高级成就'
  },
  { 
    key: 'special', 
    label: '特殊成就',
    description: '通过特殊途径或活动获得的独特成就'
  }
]

// 进度条颜色
const progressColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 }
]

// 成就数据
const achievements = ref([
  {
    id: 1,
    title: '初出茅庐',
    description: '完成第一个靶场训练',
    icon: 'Medal',
    category: 'beginner',
    isUnlocked: true,
    progress: 100,
    reward: 100,
    unlockedDate: new Date('2024-01-20'),
    rarity: 'common'
  },
  {
    id: 2,
    title: '坚持不懈',
    description: '连续7天完成训练',
    icon: 'Timer',
    category: 'beginner',
    isUnlocked: false,
    progress: 70,
    reward: 200,
    rarity: 'rare'
  },
  {
    id: 3,
    title: '全能选手',
    description: '在每个类别中完成至少一个挑战',
    icon: 'Star',
    category: 'challenge',
    isUnlocked: false,
    progress: 60,
    reward: 500,
    rarity: 'epic'
  },
  {
    id: 4,
    title: '速战速决',
    description: '在30分钟内完成一个困难级别的挑战',
    icon: 'Timer',
    category: 'master',
    isUnlocked: true,
    progress: 100,
    reward: 300,
    unlockedDate: new Date('2024-01-22'),
    rarity: 'rare'
  },
  {
    id: 5,
    title: '系统专家',
    description: '完成所有系统安全类的挑战',
    icon: 'Monitor',
    category: 'master',
    isUnlocked: false,
    progress: 45,
    reward: 1000,
    rarity: 'legendary'
  },
  {
    id: 6,
    title: '密码大师',
    description: '完成所有密码学相关的挑战',
    icon: 'Lock',
    category: 'master',
    isUnlocked: false,
    progress: 30,
    reward: 800,
    rarity: 'epic'
  },
  {
    id: 7,
    title: '社区贡献者',
    description: '发布3个高质量的解题思路',
    icon: 'ChatDotSquare',
    category: 'special',
    isUnlocked: false,
    progress: 20,
    reward: 300,
    rarity: 'rare'
  }
])

// 计算属性
const getCurrentCategory = computed(() => 
  categories.find(c => c.key === currentCategory.value)
)

const currentAchievements = computed(() => 
  currentCategory.value === 'all' 
    ? achievements.value 
    : achievements.value.filter(a => a.category === currentCategory.value)
)

// 方法
const getCategoryIcon = (category: string) => {
  const iconMap: Record<string, string> = {
    all: 'Trophy',
    beginner: 'Medal',
    challenge: 'Star',
    master: 'Monitor',
    special: 'ChatDotSquare'
  }
  return iconMap[category]
}

const getCategoryProgress = (category: string) => {
  const categoryAchievements = achievements.value.filter(a => a.category === category)
  if (!categoryAchievements.length) return 0
  
  const unlockedInCategory = categoryAchievements.filter(a => a.isUnlocked).length
  return Math.round((unlockedInCategory / categoryAchievements.length) * 100)
}

const handleUnlock = (achievementId: number) => {
  const achievement = achievements.value.find(a => a.id === achievementId)
  if (achievement && !achievement.isUnlocked) {
    achievement.isUnlocked = true
    achievement.progress = 100
    achievement.unlockedDate = new Date()
  }
}
</script>

<style scoped lang="scss">
.achievement-page {
  padding: 24px;
  min-height: 100vh;
  background: #1a1b2e;

  .main-content {
    background: rgba(30, 35, 45, 0.95);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
    
    .category-nav {
      display: flex;
      gap: 4px;
      padding: 16px;
      background: rgba(0, 0, 0, 0.2);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);

      .category-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.6);
        cursor: pointer;
        transition: all 0.3s ease;

        .el-icon {
          font-size: 18px;
        }

        .category-progress {
          font-size: 12px;
          color: var(--el-color-primary);
          margin-left: 4px;
        }

        &:hover {
          color: rgba(255, 255, 255, 0.9);
          background: rgba(255, 255, 255, 0.05);
        }

        &.active {
          color: var(--el-color-primary);
          background: rgba(64, 158, 255, 0.1);
        }
      }
    }

    .category-header {
      padding: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);

      .category-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;

        h2 {
          margin: 0;
          font-size: 24px;
          color: #fff;
        }

        .category-stats {
          display: flex;
          align-items: center;
          gap: 12px;

          :deep(.el-progress) {
            width: 120px;
          }

          .progress-text {
            font-size: 14px;
            color: var(--el-color-primary);
          }
        }
      }

      .category-desc {
        margin: 0;
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
        line-height: 1.5;
      }
    }

    .achievements-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px;
      padding: 24px;
    }

    .empty-state {
      padding: 48px;
      text-align: center;

      :deep(.el-empty) {
        padding: 40px;

        .el-icon {
          color: rgba(255, 255, 255, 0.1);
        }

        .el-empty__description {
          color: rgba(255, 255, 255, 0.4);
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .achievement-page {
    padding: 16px;

    .main-content {
      .category-nav {
        flex-wrap: wrap;
        
        .category-item {
          flex: 1;
          min-width: 120px;
          justify-content: center;
        }
      }

      .category-header {
        .category-title {
          flex-direction: column;
          align-items: flex-start;
          gap: 12px;
        }
      }

      .achievements-grid {
        grid-template-columns: 1fr;
        padding: 16px;
        gap: 16px;
      }
    }
  }
}
</style> 