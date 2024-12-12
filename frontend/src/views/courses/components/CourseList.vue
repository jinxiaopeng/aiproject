<template>
  <div class="course-list" v-loading="loading">
    <el-empty
      v-if="!loading && !courses.length"
      description="暂无课程"
    />
    
    <div class="courses-grid">
      <CourseCard
        v-for="course in courses"
        :key="course.id"
        :course="course"
        @click="$emit('view', course.id)"
        @start="$emit('start', course.id)"
        @continue="$emit('continue', course.id)"
      />
    </div>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 36, 48]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CourseCard from './CourseCard.vue'

const props = defineProps<{
  courses: any[]
  loading: boolean
  total: number
}>()

const emit = defineEmits<{
  (e: 'view', id: number): void
  (e: 'start', id: number): void
  (e: 'continue', id: number): void
  (e: 'page-change', page: number): void
  (e: 'size-change', size: number): void
}>()

const currentPage = ref(1)
const pageSize = ref(12)

const handleSizeChange = (size: number) => {
  pageSize.value = size
  emit('size-change', size)
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  emit('page-change', page)
}
</script>

<style lang="scss" scoped>
.course-list {
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 30px;
    margin-bottom: 40px;
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin: 40px 0;
    
    :deep(.el-pagination) {
      --el-pagination-bg-color: transparent;
      --el-pagination-text-color: #fff;
      --el-pagination-border-radius: 4px;
      
      .el-pager li {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        
        &:hover {
          border-color: var(--el-color-primary);
        }
        
        &.is-active {
          background: var(--el-color-primary);
          border-color: var(--el-color-primary);
        }
      }
      
      .btn-prev,
      .btn-next {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        
        &:hover {
          border-color: var(--el-color-primary);
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .course-list {
    .courses-grid {
      grid-template-columns: 1fr;
      gap: 20px;
    }
  }
}
</style> 