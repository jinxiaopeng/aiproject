/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '*.svg' {
  const content: string
  export default content
}

declare module '*.png' {
  const content: string
  export default content
}

declare module '*.jpg' {
  const content: string
  export default content
}

declare module '*.jpeg' {
  const content: string
  export default content
}

declare module '@element-plus/icons-vue' {
  import type { Component } from 'vue'
  const content: { [key: string]: Component }
  export const Monitor: Component
  export const Lock: Component
  export const Key: Component
  export const Document: Component
  export const DataAnalysis: Component
  export const Connection: Component
  export default content
} 