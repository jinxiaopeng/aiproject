<!-- 奖励页面组件 -->
<template>
  <div class="rewards-page">
    <el-page-header 
      title="返回"
      content="我的成就与等级"
      @back="$router.back()"
    />

    <div class="rewards-content">
      <el-tabs v-model="activeTab" class="rewards-tabs">
        <el-tab-pane label="等级与积分" name="level">
          <user-level />
        </el-tab-pane>
        <el-tab-pane label="成就系统" name="achievements">
          <achievement-list />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import UserLevel from '@/components/rewards/UserLevel.vue'
import AchievementList from '@/components/rewards/AchievementList.vue'

export default defineComponent({
  name: 'RewardsPage',
  components: {
    UserLevel,
    AchievementList
  },
  setup() {
    const activeTab = ref('level')

    return {
      activeTab
    }
  }
})
</script>

<style scoped>
.rewards-page {
  padding: 24px;
}

.rewards-content {
  margin-top: 24px;
}

.rewards-tabs {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

:deep(.el-tabs__header) {
  margin-bottom: 24px;
}
</style> 