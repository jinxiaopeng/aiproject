<template>
  <div class="terminal-window">
    <div class="terminal-header">
      <div class="terminal-title">Web安全实验环境</div>
      <div class="terminal-controls">
        <span class="control minimize"></span>
        <span class="control maximize"></span>
        <span class="control close"></span>
      </div>
    </div>
    <div class="terminal-content">
      <div class="terminal-output">
        <div class="line">Welcome to Web Security Lab Environment</div>
        <div class="line">System initialized...</div>
        <div class="line">Starting vulnerable application...</div>
        <div class="line">Application started on port 8080</div>
        <div class="line">Target URL: http://localhost:8080</div>
        <div class="line">------------------------</div>
        <div class="line">Instructions:</div>
        <div class="line">1. Switch to Browser tab to access the target application</div>
        <div class="line">2. Follow the challenge description</div>
        <div class="line">3. Try to find and exploit vulnerabilities</div>
        <div class="line">4. Submit the flag when you find it</div>
        <div class="line">------------------------</div>
        <div class="line blink">root@websec:~# <span class="cursor">_</span></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'LabTerminal'
})
</script>

<style scoped>
.terminal-window {
  height: 400px;
  background: #1e1e1e;
  border-radius: 4px;
  overflow: hidden;
  font-family: 'Courier New', Courier, monospace;
}

.terminal-header {
  background: #323232;
  padding: 8px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #424242;
}

.terminal-title {
  color: #e5eaf3;
  font-size: 14px;
}

.terminal-controls {
  display: flex;
  gap: 8px;
}

.control {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.control.close {
  background: #ff5f56;
}

.control.minimize {
  background: #ffbd2e;
}

.control.maximize {
  background: #27c93f;
}

.terminal-content {
  padding: 16px;
  height: calc(100% - 37px);
  overflow-y: auto;
}

.terminal-output {
  color: #e5eaf3;
  font-size: 14px;
  line-height: 1.6;
}

.terminal-output .line {
  margin-bottom: 4px;
  white-space: pre-wrap;
  word-break: break-all;
}

.terminal-output .cursor {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.blink {
  animation: cursor-blink 1.2s infinite;
}

@keyframes cursor-blink {
  0%, 100% { border-right-color: transparent; }
  50% { border-right-color: #e5eaf3; }
}
</style> 