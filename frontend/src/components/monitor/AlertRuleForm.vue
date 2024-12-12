<template>
  <el-form
    ref="formRef"
    :model="formData"
    :rules="rules"
    label-width="120px"
    class="alert-rule-form"
  >
    <el-form-item label="规则名称" prop="name">
      <el-input v-model="formData.name" placeholder="请输入规则名称" />
    </el-form-item>

    <el-form-item label="规则描述" prop="description">
      <el-input
        v-model="formData.description"
        type="textarea"
        placeholder="请输入规则描述"
      />
    </el-form-item>

    <el-form-item label="监控指标" prop="metricType">
      <el-select v-model="formData.metricType" placeholder="请选择监控指标">
        <el-option
          v-for="item in metricTypeOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </el-form-item>

    <el-form-item label="比较运算符" prop="operator">
      <el-select v-model="formData.operator" placeholder="请选择比较运算符">
        <el-option
          v-for="item in operatorOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </el-form-item>

    <el-form-item label="阈值" prop="threshold">
      <el-input-number
        v-model="formData.threshold"
        :precision="2"
        :step="0.1"
        :min="0"
      />
    </el-form-item>

    <el-form-item label="持续时间" prop="duration">
      <el-input-number
        v-model="formData.duration"
        :min="0"
        :step="1"
      >
        <template #suffix>秒</template>
      </el-input-number>
    </el-form-item>

    <el-form-item label="冷却时间" prop="cooldown">
      <el-input-number
        v-model="formData.cooldown"
        :min="0"
        :step="1"
      >
        <template #suffix>秒</template>
      </el-input-number>
    </el-form-item>

    <el-form-item label="通知方式" prop="notifyMethods">
      <el-checkbox-group v-model="formData.notifyMethods">
        <el-checkbox label="email">邮件</el-checkbox>
        <el-checkbox label="web">站内信</el-checkbox>
        <el-checkbox label="sms">短信</el-checkbox>
      </el-checkbox-group>
    </el-form-item>

    <el-form-item label="是否启用" prop="enabled">
      <el-switch v-model="formData.enabled" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
      <el-button @click="handleReset">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance } from 'element-plus'
import { MetricType, ComparisonOperator } from '@/types/alert'
import type { AlertRuleBase } from '@/types/alert'

const props = defineProps<{
  initialData?: Partial<AlertRuleBase>
}>()

const emit = defineEmits<{
  (e: 'submit', data: AlertRuleBase): void
}>()

const formRef = ref<FormInstance>()

const formData = reactive<AlertRuleBase>({
  name: '',
  description: '',
  metricType: MetricType.CPU,
  operator: ComparisonOperator.GT,
  threshold: 0,
  duration: 0,
  cooldown: 300,
  enabled: true,
  notifyMethods: ['web'],
  ...props.initialData
})

const metricTypeOptions = [
  { label: 'CPU使用率', value: MetricType.CPU },
  { label: '内存使用率', value: MetricType.MEMORY },
  { label: '磁盘使用率', value: MetricType.DISK },
  { label: '网络流量', value: MetricType.NETWORK },
  { label: '系统负载', value: MetricType.SYSTEM_LOAD },
  { label: '进程数', value: MetricType.PROCESS }
]

const operatorOptions = [
  { label: '大于', value: ComparisonOperator.GT },
  { label: '大于等于', value: ComparisonOperator.GTE },
  { label: '小于', value: ComparisonOperator.LT },
  { label: '小于等于', value: ComparisonOperator.LTE },
  { label: '等于', value: ComparisonOperator.EQ },
  { label: '不等于', value: ComparisonOperator.NEQ }
]

const rules = {
  name: [
    { required: true, message: '请输入规则名称', trigger: 'blur' },
    { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  metricType: [
    { required: true, message: '请选择监控指标', trigger: 'change' }
  ],
  operator: [
    { required: true, message: '请选择比较运算符', trigger: 'change' }
  ],
  threshold: [
    { required: true, message: '请输入阈值', trigger: 'blur' }
  ],
  notifyMethods: [
    { required: true, message: '请选择至少一种通知方式', trigger: 'change' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid, fields) => {
    if (valid) {
      emit('submit', { ...formData })
    }
  })
}

const handleReset = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}
</script>

<style lang="scss" scoped>
.alert-rule-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
</style> 