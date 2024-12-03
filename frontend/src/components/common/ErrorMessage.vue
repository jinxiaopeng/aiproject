<template>
  <div class="error-message" v-if="show">
    <el-alert
      :title="title"
      :description="message"
      type="error"
      show-icon
      :closable="closable"
      @close="handleClose"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ErrorMessage',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '错误'
    },
    message: {
      type: String,
      required: true
    },
    closable: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const handleClose = () => {
      emit('close')
    }

    return {
      handleClose
    }
  }
})
</script>

<style scoped>
.error-message {
  margin: 10px 0;
}
</style> 