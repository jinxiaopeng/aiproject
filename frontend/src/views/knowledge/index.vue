<template>
  <div class="app-container">
    <el-container>
      <el-aside width="240px">
        <sidebar-menu />
      </el-aside>

      <el-container>
        <el-header height="64px">
          <graph-toolbar />
        </el-header>

        <el-main>
          <el-row :gutter="16" class="main-content">
            <el-col :span="4">
              <graph-filters />
            </el-col>

            <el-col :span="14" class="graph-col">
              <knowledge-graph />
            </el-col>

            <el-col :span="6">
              <node-detail />
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import SidebarMenu from './components/SidebarMenu.vue'
import GraphToolbar from './components/GraphToolbar.vue'
import GraphFilters from './components/GraphFilters.vue'
import KnowledgeGraph from './components/KnowledgeGraph.vue'
import NodeDetail from './components/NodeDetail.vue'
</script>

<style scoped>
.app-container {
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  background: #1a1d21;
  background-image: 
    radial-gradient(circle at 25px 25px, rgba(65, 184, 131, 0.15) 2%, transparent 0%),
    radial-gradient(circle at 75px 75px, rgba(66, 184, 231, 0.15) 2%, transparent 0%);
  background-size: 100px 100px;
}

.el-container {
  height: 100%;
  background: rgba(30, 35, 40, 0.95);
  border-radius: 4px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.el-aside {
  background: #1a1d21;
  border-radius: 4px 0 0 4px;
  border-right: 1px solid rgba(65, 184, 131, 0.1);
}

.el-header {
  background: rgba(26, 29, 33, 0.95);
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
  padding: 0 20px;
  display: flex;
  align-items: center;
}

.el-main {
  padding: 20px;
  height: calc(100vh - 104px);
  overflow: hidden;
  background: rgba(26, 29, 33, 0.5);
}

.main-content {
  height: 100%;
}

.el-col {
  height: 100%;
}

.graph-col {
  min-height: 600px;
  background: rgba(30, 35, 40, 0.5);
  border-radius: 4px;
  border: 1px solid rgba(65, 184, 131, 0.1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
}

:deep(.el-card) {
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
  color: #e5eaf3;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

:deep(.el-button) {
  background: transparent;
  border: 1px solid rgba(65, 184, 131, 0.3);
  color: #e5eaf3;
}

:deep(.el-button:hover) {
  background: rgba(65, 184, 131, 0.1);
  border-color: rgba(65, 184, 131, 0.5);
}

:deep(.el-input__inner) {
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.3);
  color: #e5eaf3;
}

:deep(.el-input__inner:focus) {
  border-color: rgba(65, 184, 131, 0.5);
}
</style>