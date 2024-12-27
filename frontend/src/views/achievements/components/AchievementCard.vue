<template>
  <div 
    class="achievement-card" 
    :class="{ 
      'unlocked': isUnlocked,
      'locked': !isUnlocked,
      'rare': rarity === 'rare',
      'epic': rarity === 'epic',
      'legendary': rarity === 'legendary'
    }"
  >
    <div class="card-content">
      <div class="achievement-icon">
        <el-icon :class="{ 'animate-unlock': isUnlocked }">
          <component :is="icon" />
        </el-icon>
        <div class="achievement-glow"></div>
      </div>
      
      <div class="achievement-info">
        <div class="achievement-header">
          <h3 class="achievement-title">{{ title }}</h3>
          <div class="achievement-reward">
            <el-icon><Trophy /></el-icon>
            <span>{{ reward }} 积分</span>
          </div>
        </div>
        
        <p class="achievement-description">{{ description }}</p>
        
        <div class="achievement-progress" v-if="showProgress">
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :style="{ width: `${progress}%` }"
            ></div>
            <div class="progress-sparkles">
              <span v-for="n in 3" :key="n" class="sparkle"></span>
            </div>
          </div>
          <span class="progress-text">{{ progress }}%</span>
        </div>
      </div>
    </div>

    <div class="achievement-footer">
      <div class="achievement-date" v-if="unlockedDate">
        解锁于: {{ formatDate(unlockedDate) }}
      </div>
      <div class="achievement-status" v-else>
        <el-icon><Lock /></el-icon>
        未解锁
      </div>
    </div>

    <div class="achievement-shine"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Trophy, Lock } from '@element-plus/icons-vue'

interface Props {
  title: string
  description: string
  icon: string
  isUnlocked: boolean
  progress?: number
  reward: number
  unlockedDate?: Date
  showProgress?: boolean
  rarity?: 'common' | 'rare' | 'epic' | 'legendary'
}

const props = withDefaults(defineProps<Props>(), {
  progress: 0,
  showProgress: true,
  rarity: 'common'
})

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}
</script>

<style scoped lang="scss">
.achievement-card {
  position: relative;
  background: rgba(30, 35, 45, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0) 100%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    
    &::before {
      opacity: 1;
    }

    .achievement-shine {
      transform: translateX(100%);
    }
  }

  .card-content {
    padding: 20px;
    display: flex;
    gap: 16px;
  }

  .achievement-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-shrink: 0;

    .el-icon {
      font-size: 28px;
      color: rgba(255, 255, 255, 0.5);
      transition: all 0.3s ease;
    }

    .achievement-glow {
      position: absolute;
      width: 100%;
      height: 100%;
      background: radial-gradient(
        circle at center,
        rgba(255, 215, 0, 0.2) 0%,
        transparent 70%
      );
      opacity: 0;
      transition: opacity 0.3s ease;
    }
  }

  .achievement-info {
    flex: 1;
    min-width: 0;

    .achievement-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .achievement-title {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
      color: #ffffff;
    }

    .achievement-reward {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
      color: #ffd700;

      .el-icon {
        font-size: 16px;
      }
    }

    .achievement-description {
      margin: 0 0 12px;
      font-size: 14px;
      color: rgba(255, 255, 255, 0.6);
      line-height: 1.4;
    }

    .achievement-progress {
      display: flex;
      align-items: center;
      gap: 12px;

      .progress-bar {
        flex: 1;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
        position: relative;
      }

      .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #ffd700, #ffa500);
        border-radius: 3px;
        transition: width 0.3s ease;
      }

      .progress-sparkles {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        overflow: hidden;

        .sparkle {
          position: absolute;
          width: 4px;
          height: 4px;
          background: #fff;
          border-radius: 50%;
          opacity: 0;

          &:nth-child(1) {
            --position: 30;
            --delay: 0.3;
            left: calc(var(--position) * 1%);
            animation: sparkle 2s calc(var(--delay) * 1s) infinite;
          }
          &:nth-child(2) {
            --position: 60;
            --delay: 0.6;
            left: calc(var(--position) * 1%);
            animation: sparkle 2s calc(var(--delay) * 1s) infinite;
          }
          &:nth-child(3) {
            --position: 90;
            --delay: 0.9;
            left: calc(var(--position) * 1%);
            animation: sparkle 2s calc(var(--delay) * 1s) infinite;
          }
        }
      }

      .progress-text {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        min-width: 40px;
      }
    }
  }

  .achievement-footer {
    padding: 12px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 4px;

    .el-icon {
      font-size: 14px;
    }
  }

  .achievement-shine {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.1),
      transparent
    );
    transition: transform 0.6s ease;
  }

  &.unlocked {
    border-color: rgba(255, 215, 0, 0.3);

    .achievement-icon {
      background: rgba(255, 215, 0, 0.1);

      .el-icon {
        color: #ffd700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
      }

      .achievement-glow {
        opacity: 1;
      }
    }

    &:hover {
      border-color: rgba(255, 215, 0, 0.5);
      box-shadow: 0 8px 24px rgba(255, 215, 0, 0.1);
    }
  }

  &.rare {
    border-color: rgba(64, 158, 255, 0.3);
    
    .achievement-icon {
      background: rgba(64, 158, 255, 0.1);
    }
    
    &.unlocked .achievement-icon .el-icon {
      color: #409eff;
      text-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
    }
  }

  &.epic {
    border-color: rgba(145, 70, 255, 0.3);
    
    .achievement-icon {
      background: rgba(145, 70, 255, 0.1);
    }
    
    &.unlocked .achievement-icon .el-icon {
      color: #9146ff;
      text-shadow: 0 0 10px rgba(145, 70, 255, 0.5);
    }
  }

  &.legendary {
    border-color: rgba(255, 69, 0, 0.3);
    
    .achievement-icon {
      background: rgba(255, 69, 0, 0.1);
    }
    
    &.unlocked .achievement-icon .el-icon {
      color: #ff4500;
      text-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
    }
  }
}

@keyframes sparkle {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(0);
    opacity: 0;
  }
}

@keyframes unlock {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

@media (max-width: 480px) {
  .achievement-card {
    .card-content {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .achievement-info {
      .achievement-header {
        flex-direction: column;
        gap: 8px;
      }
    }
  }
}
</style> 