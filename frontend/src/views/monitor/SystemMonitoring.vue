<template>
  <div class="monitor-page">
    <el-card class="monitor-card">
      <template #header>
        <div class="card-header">
          <h3>系统监控</h3>
        </div>
      </template>
      
      <div class="monitor-content">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="网络监控" name="network">
            <network-monitor />
          </el-tab-pane>
          <el-tab-pane label="系统监控" name="system">
            <system-monitor />
          </el-tab-pane>
          <el-tab-pane label="安全监控" name="security">
            <security-monitor />
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NetworkMonitor from './components/NetworkMonitor.vue'
import SystemMonitor from './components/SystemMonitor.vue'
import SecurityMonitor from './components/SecurityMonitor.vue'

const activeTab = ref('network')
</script>

<style lang="scss" scoped>
.monitor-page {
  padding: 20px;
  
  .monitor-card {
    margin-bottom: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h3 {
      margin: 0;
    }
  }
  
  .monitor-content {
    min-height: 500px;
  }
}
</style> 