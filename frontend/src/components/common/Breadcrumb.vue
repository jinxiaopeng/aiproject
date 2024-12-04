<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item 
      v-for="(item, index) in breadcrumbItems" 
      :key="index"
      :to="item.path"
    >
      {{ item.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useRoute } from 'vue-router'

interface BreadcrumbItem {
  title: string
  path?: string
}

export default defineComponent({
  name: 'Breadcrumb',
  setup() {
    const route = useRoute()
    
    const breadcrumbItems = computed(() => {
      const { matched } = route
      const items: BreadcrumbItem[] = []
      
      matched.slice(1).forEach(item => {
        if (item.meta?.title) {
          items.push({
            title: item.meta.title as string,
            path: item.path
          })
        }
      })
      
      return items
    })
    
    return {
      breadcrumbItems
    }
  }
})
</script>

<style scoped>
.el-breadcrumb {
  line-height: 40px;
  font-size: 14px;
  color: #666;
  padding: 0 20px;
}
</style> 