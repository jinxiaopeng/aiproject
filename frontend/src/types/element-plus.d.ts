declare module 'element-plus/dist/locale/zh-cn.mjs' {
  const zhCn: {
    name: string
    el: {
      [key: string]: any
    }
  }
  export default zhCn
}

declare module '@element-plus/icons-vue' {
  import { FunctionalComponent, SVGAttributes } from 'vue'
  export const Lock: FunctionalComponent<SVGAttributes>
  export const User: FunctionalComponent<SVGAttributes>
  export const CircleCheck: FunctionalComponent<SVGAttributes>
  export const ArrowRightBold: FunctionalComponent<SVGAttributes>
  export const Avatar: FunctionalComponent<SVGAttributes>
  export const Connection: FunctionalComponent<SVGAttributes>
  // 添加其他需要的图标
} 