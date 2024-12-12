<template>
  <div class="stats-bar">
    <div class="stat-item">
      <div class="stat-value">{{ totalCourses }}</div>
      <div class="stat-label">精品课程</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">{{ totalStudents }}</div>
      <div class="stat-label">学习人数</div>
    </div>
    <div class="stat-item">
      <div class="stat-value">{{ averageRating }}</div>
      <div class="stat-label">平均评分</div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  totalCourses: number
  totalStudents: number
  averageRating: number
}>()
</script>

<style lang="scss" scoped>
.stats-bar {
  display: flex;
  gap: 40px;
  
  .stat-item {
    .stat-value {
      font-size: 2.5rem;
      font-weight: 600;
      color: #64ffda;
      line-height: 1.2;
    }
    
    .stat-label {
      font-size: 1rem;
      color: rgba(255, 255, 255, 0.7);
    }
  }
}

@media (max-width: 1024px) {
  .stats-bar {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .stats-bar {
    flex-wrap: wrap;
    gap: 20px;
    
    .stat-item {
      flex: 1;
      min-width: 120px;
      
      .stat-value {
        font-size: 2rem;
      }
    }
  }
}
</style> 