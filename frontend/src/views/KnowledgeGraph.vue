<template>
  <div class="knowledge-page">
    <div class="page-header">
      <h2>知识图谱</h2>
      <p>探索和学习网络安全知识体系</p>
    </div>
    <div class="graph-view">
      <KnowledgeGraph />
    </div>
  </div>
</template>

<script setup lang="ts">
import KnowledgeGraph from '@/components/KnowledgeGraph.vue'
</script>

<style scoped>
.knowledge-page {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.page-header p {
  margin: 8px 0 0;
  color: #666;
}

.graph-view {
  flex: 1;
  min-height: 0;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style> 