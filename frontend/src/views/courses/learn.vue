<template>
  <div class="course-learn">
    <div class="video-container">
      <VideoPlayer
        v-if="videoInfo"
        ref="playerRef"
        :src="videoInfo.video_url"
        :poster="course?.cover_url"
        @timeupdate="handleTimeUpdate"
        @ended="handleVideoEnded"
      />
    </div>
    
    <div class="learn-content">
      <div class="chapter-info">
        <h2>{{ currentChapter?.title }}</h2>
        <p>{{ currentChapter?.description }}</p>
      </div>
      
      <div class="chapter-list">
        <h3>课程大纲</h3>
        <el-menu
          :default-active="String(chapterId)"
          class="chapter-menu"
        >
          <el-menu-item
            v-for="chapter in course?.chapters"
            :key="chapter.id"
            :index="String(chapter.id)"
            @click="switchChapter(chapter.id)"
          >
            <div class="chapter-item">
              <span class="title">{{ chapter.title }}</span>
              <div class="meta">
                <span class="duration">
                  <el-icon><VideoPlay /></el-icon>
                  {{ chapter.duration }}分钟
                </span>
                <el-tag
                  v-if="chapter.progress !== undefined"
                  :type="chapter.progress === 100 ? 'success' : 'warning'"
                  size="small"
                >
                  {{ chapter.progress === 100 ? '已完成' : '进行中' }}
                </el-tag>
              </div>
            </div>
          </el-menu-item>
        </el-menu>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { VideoPlay } from '@element-plus/icons-vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import * as courseApi from '@/api/course'
import type { Course, VideoInfo, ChapterProgress } from '@/types/course'

const route = useRoute()
const router = useRouter()
const courseId = Number(route.params.courseId)
const chapterId = Number(route.params.chapterId)

const course = ref<Course | null>(null)
const videoInfo = ref<VideoInfo | null>(null)
const playerRef = ref<InstanceType<typeof VideoPlayer> | null>(null)

// 获取当前章节信息
const currentChapter = computed(() => {
  return course.value?.chapters.find(chapter => chapter.id === chapterId)
})

// 加载课程信息
const loadCourse = async () => {
  try {
    const data = await courseApi.getCourse(courseId)
    course.value = data
  } catch (error) {
    ElMessage.error('加载课程信息失败')
  }
}

// 加载视频信息
const loadVideo = async () => {
  try {
    const { data } = await courseApi.getChapterVideo(chapterId)
    videoInfo.value = data
  } catch (error) {
    ElMessage.error('加载视频信息失败')
  }
}

// 切换章节
const switchChapter = async (newChapterId: number) => {
  router.push(`/courses/${courseId}/learn/${newChapterId}`)
  await loadVideo()
}

// 处理视频播放进度更新
const handleTimeUpdate = async (currentTime: number) => {
  const progress: ChapterProgress = {
    chapter_id: chapterId,
    progress: Math.floor((currentTime / (currentChapter.value?.duration || 1)) * 100),
    last_position: currentTime,
    completed: false
  }
  
  try {
    await courseApi.updateChapterProgress(chapterId, progress)
  } catch (error) {
    console.error('更新进度失败:', error)
  }
}

// 处理视频播放结束
const handleVideoEnded = async () => {
  const progress: ChapterProgress = {
    chapter_id: chapterId,
    progress: 100,
    last_position: currentChapter.value?.duration || 0,
    completed: true
  }
  
  try {
    await courseApi.updateChapterProgress(chapterId, progress)
    ElMessage.success('本章学习完成！')
  } catch (error) {
    console.error('更新进度失败:', error)
  }
}

onMounted(async () => {
  await loadCourse()
  await loadVideo()
})
</script>

<style lang="scss" scoped>
.course-learn {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  min-height: calc(100vh - 60px);

  .video-container {
    flex: 1;
    max-width: 1000px;
  }

  .learn-content {
    width: 300px;
    
    .chapter-info {
      margin-bottom: 2rem;
      
      h2 {
        margin: 0 0 1rem;
        font-size: 1.5rem;
      }
      
      p {
        color: var(--el-text-color-secondary);
        line-height: 1.6;
      }
    }

    .chapter-list {
      h3 {
        margin: 0 0 1rem;
        font-size: 1.2rem;
      }
    }

    .chapter-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      
      .title {
        flex: 1;
        margin-right: 1rem;
      }
      
      .meta {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        
        .duration {
          display: flex;
          align-items: center;
          gap: 0.25rem;
          color: var(--el-text-color-secondary);
          font-size: 0.9rem;
        }
      }
    }
  }
}
</style> 