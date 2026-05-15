import { defineStore } from "pinia"
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth.js"
import { ElMessage } from "element-plus"
import httptool from "@/utils/api.js"

export const useChatStore = defineStore("chat", () => {
    const messages = ref([])
    const isLoading = ref(false)
    const error = ref(null)
    const currentSessionId = ref(localStorage.getItem('chatSessionId') || null)
    const sessions = ref([])

    // 加载会话列表
    async function loadSessions() {
        const authStore = useAuthStore()
        if (!authStore.hasLogin()) return

        try {
            const response = await httptool.get('/api/ai/history')
            if (response.data.code === 200) {
                sessions.value = response.data.data || []
            }
        } catch (err) {
            console.error('Load sessions failed:', err)
        }
    }

    // 加载单个会话
    async function loadSession(sessionId) {
        const authStore = useAuthStore()
        if (!authStore.hasLogin()) return

        try {
            const response = await httptool.get(`/api/ai/session/${sessionId}`)
            if (response.data.code === 200) {
                currentSessionId.value = sessionId
                localStorage.setItem('chatSessionId', sessionId)
                messages.value = response.data.data.messages.map(m => ({
                    id: m.id,
                    role: m.role,
                    content: m.content
                }))
            }
        } catch (err) {
            console.error('Load session failed:', err)
        }
    }

    // 创建会话
    async function createSession(title = '新对话') {
        const authStore = useAuthStore()
        if (!authStore.hasLogin()) return null

        try {
            const response = await httptool.post('/api/ai/session', { title })
            if (response.data.code === 200) {
                const newSession = {
                    id: response.data.data.id,
                    title: response.data.data.title
                }
                sessions.value.unshift(newSession)
                currentSessionId.value = response.data.data.id
                localStorage.setItem('chatSessionId', response.data.data.id)
                messages.value = []
                return response.data.data.id
            }
        } catch (err) {
            console.error('Create session failed:', err)
        }
        return null
    }

    // 删除会话
    async function deleteSessionAPI(sessionId) {
        const authStore = useAuthStore()
        if (!authStore.hasLogin()) return

        try {
            const response = await httptool.delete(`/api/ai/session/${sessionId}/delete`)
            if (response.data.code === 200) {
                sessions.value = sessions.value.filter(s => s.id !== sessionId)
                if (currentSessionId.value === sessionId) {
                    if (sessions.value.length > 0) {
                        await loadSession(sessions.value[0].id)
                    } else {
                        currentSessionId.value = null
                        localStorage.removeItem('chatSessionId')
                        messages.value = []
                    }
                }
                ElMessage.success('删除成功')
            }
        } catch (err) {
            console.error('Delete session failed:', err)
        }
    }

    // 发送消息
    async function sendMessage(content) {
        if (!content.trim()) return

        const authStore = useAuthStore()
        if (!authStore.hasLogin()) {
            ElMessage.warning("请先登录后再使用 AI 助手")
            return
        }

        // 如果没有会话，先创建一个
        if (!currentSessionId.value) {
            await createSession()
        }

        const tempId = Date.now()
        messages.value.push({
            id: tempId,
            role: "user",
            content: content.trim()
        })

        messages.value.push({
            id: tempId + 1,
            role: "assistant",
            content: ""
        })

        isLoading.value = true
        error.value = null

        try {
            const history = messages.value
                .filter(m => m.id !== tempId && m.id !== tempId + 1)
                .map(m => ({
                    role: m.role,
                    content: m.content
                }))

            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/ai/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem("accessToken")}`
                },
                body: JSON.stringify({
                    message: content,
                    history: history
                })
            })

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`)
            }

            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let fullContent = ''
            const lastIndex = messages.value.length - 1

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                const chunk = decoder.decode(value)
                fullContent += chunk
                if (lastIndex >= 0 && messages.value[lastIndex].role === 'assistant') {
                    messages.value[lastIndex].content = fullContent.trim()
                }
            }

            // 保存用户消息到后端
            const sessionId = currentSessionId.value
            await httptool.post('/api/ai/message', {
                session_id: sessionId,
                role: 'user',
                content: content.trim()
            })
            await httptool.post('/api/ai/message', {
                session_id: sessionId,
                role: 'assistant',
                content: fullContent.trim()
            })

            // 刷新会话列表（更新标题）
            await loadSessions()
        } catch (err) {
            error.value = err.message || "Failed to get response"
            ElMessage.error('发送消息失败')
        } finally {
            isLoading.value = false
        }
    }

    // 清除消息
    function clearMessages() {
        messages.value = []
        currentSessionId.value = null
        localStorage.removeItem('chatSessionId')
    }

    return {
        messages,
        isLoading,
        error,
        currentSessionId,
        sessions,
        loadSessions,
        loadSession,
        createSession,
        deleteSessionAPI,
        sendMessage,
        clearMessages
    }
})