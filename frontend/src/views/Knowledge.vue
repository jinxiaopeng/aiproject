<template>
  <div class="knowledge">
    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索知识..."
        class="search-input"
        :prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
      <el-select
        v-model="filterCategory"
        placeholder="分类"
        class="filter-select"
        clearable
      >
        <el-option
          v-for="category in categories"
          :key="category.value"
          :label="category.label"
          :value="category.value"
        />
      </el-select>
      <el-select
        v-model="filterTag"
        placeholder="标签"
        class="filter-select"
        clearable
      >
        <el-option
          v-for="tag in tags"
          :key="tag.value"
          :label="tag.label"
          :value="tag.value"
        />
      </el-select>
    </div>

    <!-- 知识列表 -->
    <div class="knowledge-grid">
      <el-row :gutter="20">
        <el-col 
          v-for="article in filteredArticles" 
          :key="article.id" 
          :xs="24" 
          :sm="12" 
          :md="8"
        >
          <el-card class="article-card" shadow="hover">
            <div class="article-cover">
              <img :src="article.cover" :alt="article.title">
              <div class="article-category">
                <el-tag>{{ article.category }}</el-tag>
              </div>
            </div>
            <div class="article-content">
              <h3 class="article-title">{{ article.title }}</h3>
              <p class="article-description">{{ article.description }}</p>
              <div class="article-meta">
                <div class="meta-left">
                  <span class="author">
                    <el-avatar :size="20" :src="article.author.avatar" />
                    {{ article.author.name }}
                  </span>
                  <span class="date">{{ article.date }}</span>
                </div>
                <div class="meta-right">
                  <span class="views">
                    <el-icon><View /></el-icon>
                    {{ article.views }}
                  </span>
                  <span class="likes">
                    <el-icon><Star /></el-icon>
                    {{ article.likes }}
                  </span>
                </div>
              </div>
              <div class="article-tags">
                <el-tag
                  v-for="tag in article.tags"
                  :key="tag"
                  size="small"
                  effect="plain"
                >
                  {{ tag }}
                </el-tag>
              </div>
              <el-button 
                type="primary" 
                text 
                class="read-more"
                @click="handleReadMore(article)"
              >
                阅读全文
                <el-icon class="el-icon--right"><ArrowRight /></el-icon>
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 加载更多 -->
    <div v-if="hasMore" class="load-more">
      <el-button 
        :loading="loading" 
        @click="loadMore"
      >
        加载更多
      </el-button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, View, Star, ArrowRight } from '@element-plus/icons-vue'

interface Article {
  id: number
  title: string
  description: string
  cover: string
  category: string
  tags: string[]
  author: {
    name: string
    avatar: string
  }
  date: string
  views: number
  likes: number
}

export default defineComponent({
  name: 'Knowledge',
  components: {
    Search,
    View,
    Star,
    ArrowRight
  },
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    const filterCategory = ref('')
    const filterTag = ref('')
    const loading = ref(false)
    const hasMore = ref(true)
    
    // 分类数据
    const categories = [
      { label: 'Web安全', value: 'web' },
      { label: '系统安全', value: 'system' },
      { label: '网络安全', value: 'network' },
      { label: '密码学', value: 'crypto' },
      { label: '安全开发', value: 'development' }
    ]
    
    // 标签数据
    const tags = [
      { label: '漏洞分析', value: 'vulnerability' },
      { label: '安全工具', value: 'tools' },
      { label: '最佳实践', value: 'best-practice' },
      { label: '安全架构', value: 'architecture' },
      { label: '安全测试', value: 'testing' }
    ]
    
    // 文章数据
    const articles = ref<Article[]>([
      {
        id: 1,
        title: 'Web应用常见安全漏洞及防护措施',
        description: '本文详细介绍了Web应用中常见的安全漏洞类型，包括SQL注入、XSS、CSRF等，并提供了相应的防护建议和最佳实践。',
        cover: '/images/articles/web-security.jpg',
        category: 'Web安全',
        tags: ['漏洞分析', '最佳实践'],
        author: {
          name: '张三',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        },
        date: '2023-12-01',
        views: 1234,
        likes: 56
      },
      {
        id: 2,
        title: '浅谈Linux系统安全加固',
        description: '本文介绍了Linux系统安全加固的基本原则和具体措施，包括账号安全、文件系统安全、网络安全等多个方面。',
        cover: '/images/articles/linux-security.jpg',
        category: '系统安全',
        tags: ['最佳实践', '安全架构'],
        author: {
          name: '李四',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        },
        date: '2023-11-30',
        views: 890,
        likes: 45
      },
      {
        id: 3,
        title: '常用渗透测试工具介绍',
        description: '本文介绍了一些常用的渗透测试工具，包括信息收集、漏洞扫描、漏洞利用等不同阶段的工具使用方法。',
        cover: '/images/articles/pentest-tools.jpg',
        category: '安全工具',
        tags: ['安全工具', '安全测试'],
        author: {
          name: '王五',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        },
        date: '2023-11-29',
        views: 567,
        likes: 34
      }
    ])
    
    // 过滤文章
    const filteredArticles = computed(() => {
      return articles.value.filter(article => {
        const matchQuery = article.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          article.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchCategory = !filterCategory.value || article.category === filterCategory.value
        const matchTag = !filterTag.value || article.tags.includes(filterTag.value)
        
        return matchQuery && matchCategory && matchTag
      })
    })
    
    // 搜索处理
    const handleSearch = () => {
      // TODO: 实现搜索逻辑
    }
    
    // 加载更多
    const loadMore = async () => {
      try {
        loading.value = true
        // TODO: 实现加载更多逻辑
        await new Promise(resolve => setTimeout(resolve, 1000))
        hasMore.value = false
      } finally {
        loading.value = false
      }
    }
    
    // 阅读文章
    const handleReadMore = (article: Article) => {
      router.push(`/knowledge/${article.id}`)
    }
    
    return {
      searchQuery,
      filterCategory,
      filterTag,
      loading,
      hasMore,
      categories,
      tags,
      filteredArticles,
      handleSearch,
      loadMore,
      handleReadMore
    }
  }
})
</script>

<style scoped>
.knowledge {
  padding: 20px;
}

.filter-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 160px;
}

.knowledge-grid {
  margin-bottom: 24px;
}

.article-card {
  height: 100%;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.article-card:hover {
  transform: translateY(-5px);
}

.article-cover {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-category {
  position: absolute;
  top: 12px;
  right: 12px;
}

.article-content {
  padding: 16px;
}

.article-title {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 500;
  color: var(--text-color);
}

.article-description {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--text-color-secondary);
  height: 60px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--text-color-secondary);
}

.meta-left,
.meta-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.author {
  display: flex;
  align-items: center;
  gap: 8px;
}

.views,
.likes {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.read-more {
  display: flex;
  align-items: center;
  gap: 4px;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
}
</style> 