<template>
  <div class="toolbar">
    <div class="left">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索知识点..."
        class="search-input"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><el-icon-search /></el-icon>
        </template>
      </el-input>
    </div>
    <div class="right">
      <el-button-group>
        <!-- 工具按钮 -->
      </el-button-group>
    </div>
  </div>
</template>

<script setup lang="ts">
// ...
</script> 