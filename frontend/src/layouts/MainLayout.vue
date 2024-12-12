<template>
  <div class="layout-container">
    <el-container>
      <el-header>
        <nav-bar />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <footer-bar />
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/layout/NavBar.vue'
import FooterBar from '@/components/layout/FooterBar.vue'
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.el-header {
  padding: 0;
  height: auto;
}

.el-main {
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.el-footer {
  padding: 0;
  height: auto;
}
</style> 