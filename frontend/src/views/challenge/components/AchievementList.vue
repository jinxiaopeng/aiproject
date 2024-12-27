<template>
  <div class="achievement-list">
    <div class="achievement-header">
      <h2 class="section-title">
        <el-icon><Medal /></el-icon>
        成就系统
      </h2>
      <div class="achievement-stats">
        <div class="stat-item">
          <span class="label">已解锁</span>
          <span class="value">{{ unlockedCount }}/{{ totalCount }}</span>
        </div>
        <div class="stat-item">
          <span class="label">完成度</span>
          <span class="value">{{ completionRate }}%</span>
        </div>
      </div>
    </div>

    <el-tabs class="achievement-tabs">
      <el-tab-pane 
        v-for="category in categories" 
        :key="category.key"
        :label="category.label"
      >
        <div class="achievement-grid">
          <AchievementCard
            v-for="achievement in filterAchievements(category.key)"
            :key="achievement.id"
            v-bind="achievement"
          />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Medal } from '@element-plus/icons-vue'
import AchievementCard from './AchievementCard.vue'

// 成就分类
const categories = [
  { key: 'all', label: '全部' },
  { key: 'beginner', label: '新手成就' },
  { key: 'challenge', label: '挑战成就' },
  { key: 'master', label: '大师成就' },
  { key: 'special', label: '特殊成就' }
]

// 成就数据
const achievements = ref([
  {
    id: 1,
    title: '初出茅庐',
    description: '完成第一个靶场训练',
    icon: 'Sunrise',
    category: 'beginner',
    isUnlocked: true,
    progress: 100,
    reward: '100 积分',
    unlockedDate: new Date('2024-01-20')
  },
  {
    id: 2,
    title: '坚持不懈',
    description: '连续7天完成训练',
    icon: 'Calendar',
    category: 'beginner',
    isUnlocked: false,
    progress: 70,
    reward: '200 积分'
  },
  {
    id: 3,
    title: '全能选手',
    description: '在每个类别中完成至少一个挑战',
    icon: 'Star',
    category: 'challenge',
    isUnlocked: false,
    progress: 60,
    reward: '500 积分'
  },
  {
    id: 4,
    title: '速战速决',
    description: '在30分钟内完成一个困难级别的挑战',
    icon: 'Timer',
    category: 'master',
    isUnlocked: true,
    progress: 100,
    reward: '300 积分',
    unlockedDate: new Date('2024-01-22')
  },
  {
    id: 5,
    title: '系统专家',
    description: '完成所有系统安全类的挑战',
    icon: 'Monitor',
    category: 'master',
    isUnlocked: false,
    progress: 45,
    reward: '1000 积分'
  },
  {
    id: 6,
    title: '密码大师',
    description: '完成所有密码学相关的挑战',
    icon: 'Lock',
    category: 'master',
    isUnlocked: false,
    progress: 30,
    reward: '800 积分'
  }
])

// 计算属性
const unlockedCount = computed(() => 
  achievements.value.filter(a => a.isUnlocked).length
)

const totalCount = computed(() => achievements.value.length)

const completionRate = computed(() => 
  Math.round((unlockedCount.value / totalCount.value) * 100)
)

// 过滤成就
const filterAchievements = (category: string) => {
  if (category === 'all') return achievements.value
  return achievements.value.filter(a => a.category === category)
}
</script>

<style scoped>
.achievement-list {
  padding: 24px;
  background: rgba(30, 35, 45, 0.95);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.achievement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 8px;
}

.achievement-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.stat-item .label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.stat-item .value {
  font-size: 20px;
  font-weight: 600;
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.achievement-tabs {
  :deep(.el-tabs__header) {
    border-bottom-color: rgba(255, 255, 255, 0.1);
    margin-bottom: 24px;
  }

  :deep(.el-tabs__nav-wrap::after) {
    background-color: rgba(255, 255, 255, 0.1);
  }

  :deep(.el-tabs__item) {
    color: rgba(255, 255, 255, 0.6);
    font-size: 16px;
    padding: 0 24px;
    height: 48px;
    line-height: 48px;
    transition: all 0.3s ease;

    &:hover {
      color: rgba(255, 255, 255, 0.8);
    }

    &.is-active {
      color: #ffd700;
    }
  }

  :deep(.el-tabs__active-bar) {
    background-color: #ffd700;
    height: 3px;
    border-radius: 1.5px;
  }
}

.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  padding: 8px;
}

@media (max-width: 768px) {
  .achievement-grid {
    grid-template-columns: 1fr;
  }

  .achievement-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .achievement-stats {
    width: 100%;
    justify-content: space-around;
  }
}
</style> 