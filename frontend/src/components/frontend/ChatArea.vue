<script setup>
defineProps({
  conversation: Object,
  username: {
    type: String,
    default: '用户'
  },
  avatar: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <div class="chat-area">
    <div class="chat-header">
      <h2>{{ conversation?.title || '新对话' }}</h2>
    </div>

    <div class="messages-container">
      <div v-if="!conversation?.messages?.length" class="empty-state">
        <h3 class="welcome-text">Hi, {{ username }}</h3>
      </div>

      <div v-else class="messages-list">
        <div
          v-for="(msg, index) in conversation.messages"
          :key="index"
          class="message"
          :class="msg.role"
        >
          <div class="message-avatar">
            <el-image v-if="msg.role === 'user'" class="user-avatar" :src="avatar" fit="cover">
              <template #error>
                <div class="avatar-fallback">{{ username?.charAt(0).toUpperCase() || 'U' }}</div>
              </template>
            </el-image>
            <div v-else class="ai-avatar">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2L3 7l7 5 7-5-7-5zM3 13l7 5 7-5M3 17l7 5 7-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(msg.content)"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    formatMessage(content) {
      return content
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
    }
  }
}
</script>

<style scoped>
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color);
  text-align: center;
}

.chat-header h2 {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.welcome-text {
  font-size: 24px;
  font-weight: 500;
  color: var(--text-primary);
}

.messages-list {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  gap: 16px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
}

.avatar-fallback {
  width: 32px;
  height: 32px;
  background: var(--accent-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  background: var(--bg-tertiary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-color);
}

.message-content {
  flex: 1;
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--bg-secondary);
}

.message.user .message-content {
  background: var(--accent-color);
  color: white;
}

.message-text {
  font-size: 14px;
  line-height: 1.6;
}
</style>
