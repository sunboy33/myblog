<script setup>
import { ref } from 'vue'

defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send'])
const message = ref('')

const handleSend = () => {
  if (message.value.trim()) {
    emit('send', message.value)
    message.value = ''
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="input-container">
    <div class="input-box">
      <textarea
        v-model="message"
        placeholder="输入消息..."
        rows="1"
        @keydown="handleKeydown"
        :disabled="disabled"
      ></textarea>
      <button class="send-btn" @click="handleSend" :disabled="!message.trim() || disabled">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M3 9l12 3-12 3V9z" fill="currentColor"/>
        </svg>
      </button>
    </div>
    <p class="input-hint">AI 助手可能会产生不准确的信息，请仔细核对。</p>
  </div>
</template>

<style scoped>
.input-container {
  padding: 16px 24px 24px;
  background: var(--bg-primary);
}

.input-box {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px 16px;
  max-width: 800px;
  margin: 0 auto;
}

.input-box:focus-within {
  border-color: var(--accent-color);
}

textarea {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  outline: none;
  min-height: 24px;
  max-height: 200px;
  color: var(--text-primary);
}

textarea::placeholder {
  color: var(--text-secondary);
}

textarea:disabled {
  opacity: 0.5;
}

.send-btn {
  width: 32px;
  height: 32px;
  background: var(--accent-color);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-hint {
  text-align: center;
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 8px;
}
</style>
