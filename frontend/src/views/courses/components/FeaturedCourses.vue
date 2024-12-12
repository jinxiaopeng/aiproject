<template>
  <div class="featured-courses" v-if="courses.length">
    <h2 class="section-title">推荐课程</h2>
    <div class="featured-grid">
      <CourseCard
        v-for="course in courses"
        :key="course.id"
        :course="course"
        @click="$emit('view', course.id)"
        @start="$emit('start', course.id)"
        @continue="$emit('continue', course.id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import CourseCard from './CourseCard.vue'

defineProps<{
  courses: any[]
}>()

defineEmits<{
  (e: 'view', id: number): void
  (e: 'start', id: number): void
  (e: 'continue', id: number): void
}>()
</script>

<style lang="scss" scoped>
.featured-courses {
  margin: -60px 0 80px;
  position: relative;
  z-index: 2;
  
  .section-title {
    font-size: 2rem;
    font-weight: 600;
    margin: 0 0 2rem;
    background: linear-gradient(to right, #fff, #64ffda);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .featured-courses {
    margin: -40px 0 60px;
    
    .section-title {
      font-size: 1.75rem;
    }
    
    .featured-grid {
      grid-template-columns: 1fr;
      gap: 20px;
    }
  }
}
</style> 