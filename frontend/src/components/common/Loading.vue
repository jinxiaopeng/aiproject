<template>
  <div class="loading-wrapper" v-if="loading">
    <div class="loading-spinner">
      <el-icon class="is-loading">
        <loading />
      </el-icon>
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Loading } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Loading',
  components: {
    Loading
  },
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: '加载中...'
    }
  }
})
</script>

<style scoped>
.loading-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  text-align: center;
}

.loading-spinner .el-icon {
  font-size: 2em;
  color: #409EFF;
}

.loading-spinner p {
  margin-top: 10px;
  color: #666;
}
</style> 