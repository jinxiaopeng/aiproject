<template>
  <div class="practice">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="challenge-card">
          <template #header>
            <div class="card-header">
              <span>实战挑战</span>
              <el-radio-group v-model="difficulty" size="small">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="easy">简单</el-radio-button>
                <el-radio-button label="medium">中等</el-radio-button>
                <el-radio-button label="hard">困难</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <el-table :data="challenges" style="width: 100%">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag>{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="120">
              <template #default="{ row }">
                <el-tag :type="row.difficulty === 'easy' ? 'success' : row.difficulty === 'medium' ? 'warning' : 'danger'">
                  {{ row.difficulty === 'easy' ? '简单' : row.difficulty === 'medium' ? '中等' : '困难' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="points" label="积分" width="100" />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link @click="startChallenge(row)">
                  开始挑战
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="rank-card">
          <template #header>
            <div class="card-header">
              <span>排行榜</span>
              <el-radio-group v-model="rankType" size="small">
                <el-radio-button label="daily">日榜</el-radio-button>
                <el-radio-button label="weekly">周榜</el-radio-button>
                <el-radio-button label="monthly">月榜</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="rank-list">
            <div v-for="(user, index) in rankList" :key="user.id" class="rank-item">
              <div class="rank-index" :class="{ 'top-3': index < 3 }">{{ index + 1 }}</div>
              <el-avatar :size="40" :src="user.avatar" />
              <div class="user-info">
                <div class="username">{{ user.username }}</div>
                <div class="points">{{ user.points }} 分</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'Practice',
  setup() {
    const difficulty = ref('all')
    const rankType = ref('daily')

    // 模拟挑战数据
    const challenges = [
      {
        id: 1,
        title: 'SQL注入实战',
        type: 'Web安全',
        difficulty: 'easy',
        points: 100
      },
      {
        id: 2,
        title: 'XSS跨站攻防',
        type: 'Web安全',
        difficulty: 'medium',
        points: 200
      },
      {
        id: 3,
        title: '高级持续渗透',
        type: '渗透测试',
        difficulty: 'hard',
        points: 500
      }
    ]

    // 模拟排行榜数据
    const rankList = [
      {
        id: 1,
        username: '白帽子',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        points: 2500
      },
      {
        id: 2,
        username: '安全专家',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        points: 2200
      },
      {
        id: 3,
        username: '渗透测试者',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        points: 1800
      }
    ]

    const startChallenge = (challenge: any) => {
      console.log('开始挑战:', challenge)
      // 实现挑战开始逻辑
    }

    return {
      difficulty,
      rankType,
      challenges,
      rankList,
      startChallenge
    }
  }
})
</script>

<style scoped>
.practice {
  padding: 20px;
}

.challenge-card,
.rank-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rank-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f7fa;
}

.rank-index {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #909399;
  color: white;
  font-weight: bold;
}

.rank-index.top-3 {
  background-color: #e6a23c;
}

.rank-index.top-3:first-child {
  background-color: #f56c6c;
}

.user-info {
  flex: 1;
}

.username {
  font-weight: bold;
  margin-bottom: 4px;
}

.points {
  font-size: 12px;
  color: #909399;
}
</style> 