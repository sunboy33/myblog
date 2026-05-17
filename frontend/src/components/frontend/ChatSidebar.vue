<script setup>
defineProps({
  conversations: Array,
  currentId: Number,
  username: {
    type: String,
    default: '用户'
  },
  avatar: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['select', 'newChat', 'delete'])
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <button class="new-chat-btn" @click="emit('newChat')">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        新建对话
      </button>
    </div>

    <div class="search-area">
      <button class="search-btn">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/>
          <path d="M11 11l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        搜索对话
      </button>
    </div>

    <div class="conversations-list">
      <div
        v-for="conv in conversations"
        :key="conv.id"
        class="conversation-item"
        :class="{ active: conv.id === currentId }"
        @click="emit('select', conv.id)"
      >
        <svg class="conv-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M14 2H2a1 1 0 00-1 1v9a1 1 0 001 1h4l3 3 3-3h2a1 1 0 001-1V3a1 1 0 00-1-1z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="conv-title">{{ conv.title.length > 15 ? conv.title.slice(0, 15) + '...' : conv.title }}</span>
        <button class="delete-btn" @click="emit('delete', conv.id)">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="sidebar-footer">
      <div class="user-info">
        <el-image class="avatar" :src="avatar" fit="cover">
          <template #error>
            <div class="avatar-fallback">{{ username?.charAt(0).toUpperCase() || 'U' }}</div>
          </template>
        </el-image>
        <span>{{ username || '用户' }}</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sidebar-header {
  padding: 12px;
}

.new-chat-btn {
  width: 100%;
  padding: 10px 14px;
  background: var(--accent-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.new-chat-btn:hover {
  opacity: 0.9;
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}

.search-area {
  padding: 0 12px 12px;
}

.search-btn {
  width: 100%;
  padding: 10px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.search-btn:hover {
  border-color: var(--accent-color);
  color: var(--accent-color);
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 2px;
}

.conversation-item:hover {
  background: var(--hover-bg);
}

.conversation-item.active {
  background: var(--bg-tertiary);
}

.conv-icon {
  color: var(--text-secondary);
  flex-shrink: 0;
}

.conv-title {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-btn {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: transparent;
  border: none;
  color: #666;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
}

.conversation-item:hover .delete-btn {
  display: flex;
}

.delete-btn:hover {
  background: #ddd;
  color: #333;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid var(--border-color);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
}

.user-info:hover {
  background: var(--hover-bg);
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  flex-shrink: 0;
}

.avatar-fallback {
  width: 28px;
  height: 28px;
  background: var(--accent-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
}
</style>
