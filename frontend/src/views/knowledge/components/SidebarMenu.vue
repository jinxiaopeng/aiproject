<template>
  <div class="sidebar">
    <div class="logo">
      <el-icon :size="24"><Monitor /></el-icon>
      <span>Web安全学习导航</span>
    </div>

    <el-menu
      :default-active="activeMenu"
      class="el-menu-vertical"
      :collapse="isCollapse"
      @select="handleSelect"
    >
      <el-menu-item index="knowledge">
        <el-icon><Share /></el-icon>
        <template #title>知识图谱</template>
      </el-menu-item>

      <el-menu-item index="learning-path">
        <el-icon><Histogram /></el-icon>
        <template #title>学习路径</template>
      </el-menu-item>

      <el-sub-menu index="resources">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>学习资源</span>
        </template>
        <el-menu-item index="articles">
          <el-icon><Reading /></el-icon>
          <template #title>技术文章</template>
        </el-menu-item>
        <el-menu-item index="videos">
          <el-icon><VideoPlay /></el-icon>
          <template #title>视频教程</template>
        </el-menu-item>
        <el-menu-item index="tools">
          <el-icon><Tools /></el-icon>
          <template #title>安全工具</template>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="practice">
        <template #title>
          <el-icon><Operation /></el-icon>
          <span>实战演练</span>
        </template>
        <el-menu-item index="labs">
          <el-icon><Monitor /></el-icon>
          <template #title>靶场实验</template>
        </el-menu-item>
        <el-menu-item index="challenges">
          <el-icon><Trophy /></el-icon>
          <template #title>挑战题目</template>
        </el-menu-item>
      </el-sub-menu>

      <el-menu-item index="settings">
        <el-icon><Setting /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>

    <div class="sidebar-footer">
      <el-tooltip
        :content="isCollapse ? '展开菜单' : '收起菜单'"
        placement="right"
      >
        <el-button
          class="collapse-btn"
          @click="toggleCollapse"
        >
          <el-icon>
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </el-button>
      </el-tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Monitor,
  Share,
  Histogram,
  Document,
  Reading,
  VideoPlay,
  Tools,
  Operation,
  Trophy,
  Setting,
  Expand,
  Fold
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)

// 当前激活的菜单项
const activeMenu = computed(() => {
  return route.name?.toString() || 'knowledge'
})

// 处理菜单选择
const handleSelect = (index: string) => {
  if (['articles', 'videos', 'tools', 'labs', 'challenges'].includes(index)) {
    ElMessage.info('该功能正在开发中')
    return
  }

  if (index === 'settings') {
    ElMessage.info('设置功能正在开发中')
    return
  }

  router.push({ name: index })
}

// 切换菜单展开/收起
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}
</script>

<style scoped>
.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(30, 35, 40, 0.95);
  border-right: 1px solid rgba(65, 184, 131, 0.1);
  transition: all 0.3s;
}

.logo {
  height: 64px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #e5eaf3;
  font-size: 18px;
  font-weight: 500;
  background: rgba(26, 29, 33, 0.5);
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
  overflow: hidden;
  white-space: nowrap;
}

.el-menu {
  flex: 1;
  border-right: none;
  background: transparent;
}

.sidebar-footer {
  padding: 12px;
  display: flex;
  justify-content: center;
  background: rgba(26, 29, 33, 0.5);
  border-top: 1px solid rgba(65, 184, 131, 0.1);
}

.collapse-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e5eaf3;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

:deep(.el-menu) {
  --el-menu-bg-color: transparent;
  --el-menu-text-color: #e5eaf3;
  --el-menu-hover-bg-color: rgba(255, 255, 255, 0.05);
  --el-menu-active-color: #409eff;
  --el-menu-item-height: 50px;
}

:deep(.el-menu-item) {
  border-left: 3px solid transparent;
}

:deep(.el-menu-item.is-active) {
  background: rgba(64, 158, 255, 0.1);
  border-left-color: #409eff;
}

:deep(.el-sub-menu__title) {
  color: #e5eaf3;
}

:deep(.el-sub-menu__title:hover) {
  background: rgba(255, 255, 255, 0.05);
}

:deep(.el-menu--collapse) {
  width: 64px;
}

:deep(.el-menu--collapse .el-sub-menu__title span) {
  display: none;
}

:deep(.el-menu--collapse .el-sub-menu__title .el-sub-menu__icon-arrow) {
  display: none;
}
</style> 