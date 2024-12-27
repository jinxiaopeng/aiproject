#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def cleanup_monitor_files():
    # 需要删除的监控相关重复文件列表
    files_to_delete = [
        # 前端重复的监控组件
        "frontend/src/views/monitor/LearningMonitor.vue",  # 已合并到 SystemMonitor.vue
        "frontend/src/views/monitor/SecurityMonitor.vue",  # 已合并到 SystemMonitor.vue
        "frontend/src/components/monitor/AlertRuleForm.vue",  # 重复的告警规则表单
        "frontend/src/components/monitor/AlertRuleList.vue",  # 重复的告警规则列表
        "frontend/src/components/monitor/RealtimeMonitor.vue",  # 重复的实时监控组件
        
        # 前端重复的测试文件
        "frontend/src/components/feedback/__tests__/feedback.spec.ts",  # 未使用的测试文件
        
        # 前端重复的图标定义
        "frontend/src/components/icons.ts",  # 已在 @element-plus/icons-vue 中定义
        
        # 前端重复的类型定义
        "frontend/components.d.ts",  # 已在 src/components.d.ts 中定义
        "frontend/auto-imports.d.ts",  # 已在 src/auto-imports.d.ts 中定义
    ]
    
    # 获取项目根目录
    root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # 删除文件
    for file_path in files_to_delete:
        full_path = root_dir / file_path
        if full_path.exists():
            try:
                if full_path.is_dir():
                    shutil.rmtree(full_path)
                    print(f"已删除目录: {file_path}")
                else:
                    full_path.unlink()
                    print(f"已删除文件: {file_path}")
            except Exception as e:
                print(f"删除 {file_path} 时出错: {str(e)}")
        else:
            print(f"文件不存在: {file_path}")

if __name__ == "__main__":
    cleanup_monitor_files() 