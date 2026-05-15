<script setup>
import { onMounted, computed } from 'vue'
import { useChatStore } from '@/stores/chat.js'
import { useAuthStore } from '@/stores/auth.js'
import ChatSidebar from '@/components/frontend/ChatSidebar.vue'
import ChatArea from '@/components/frontend/ChatArea.vue'
import InputBox from '@/components/frontend/InputBox.vue'

const chatStore = useChatStore()
const authStore = useAuthStore()

// 当前对话
const currentConversation = computed(() => {
    if (!chatStore.currentSessionId) {
        return { id: null, title: '新对话', messages: [] }
    }
    const session = chatStore.sessions.find(s => s.id === chatStore.currentSessionId)
    return {
        id: session?.id || null,
        title: session?.title || '新对话',
        messages: chatStore.messages
    }
})

// 发送消息
const handleSend = async (message) => {
    if (!message.trim() || chatStore.isLoading) return
    await chatStore.sendMessage(message)
}

// 新建对话
const handleNewChat = () => {
    chatStore.clearMessages()
}

// 选择会话
const handleSelectSession = async (sessionId) => {
    await chatStore.loadSession(sessionId)
}

// 删除会话
const handleDeleteSession = async (sessionId) => {
    await chatStore.deleteSessionAPI(sessionId)
}


onMounted(async () => {
    if (authStore.hasLogin()) {
        await chatStore.loadSessions()
        if (chatStore.currentSessionId) {
            await chatStore.loadSession(chatStore.currentSessionId)
        }
    }
})
</script>

<template>
    <div class="app-container">
        <ChatSidebar
            :conversations="chatStore.sessions"
            :currentId="chatStore.currentSessionId"
            :username="authStore.user.userName || '用户'"
            :avatar="authStore.user.avatar || ''"
            @select="handleSelectSession"
            @newChat="handleNewChat"
            @delete="handleDeleteSession"
        />
        <main class="main-content">
            <ChatArea
                :conversation="currentConversation"
                :username="authStore.user.userName || '用户'"
                :avatar="authStore.user.avatar || ''"
            />
            <InputBox
                :disabled="chatStore.isLoading"
                @send="handleSend"
            />
        </main>
    </div>
</template>

<style>
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f7f7f8;
    --bg-tertiary: #ececf1;
    --text-primary: #000000;
    --text-secondary: #8e8e8e;
    --border-color: #e5e5e5;
    --accent-color: #10a37f;
    --hover-bg: rgba(0, 0, 0, 0.05);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    height: 100vh;
    overflow: hidden;
}

#app {
    height: 100vh;
}

.app-container {
    display: flex;
    height: 100vh;
}

.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--bg-primary);
    overflow: hidden;
}
</style>
