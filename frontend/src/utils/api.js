import axios from "axios"
import { useAuthStore } from "@/stores/auth.js"
import {showError} from "@/utils/message.js"

const BASE_URL = import.meta.env.VITE_API_BASE_URL

const REFRESH_URL = `${BASE_URL}/authority/refreshToken`
const httptool = axios.create({
    baseURL: BASE_URL,
    timeout: 30000,
})

// 请求拦截器
httptool.interceptors.request.use(config => {
    const token = window.localStorage.getItem('accessToken')
    if (token) {
        config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
}, error => {
    return Promise.reject(error)
})

// 是否正在刷新token的标记
let isRefreshing = false
// 重试队列
let failedQueue = []

// 处理队列中的请求
const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error)
        } else {
            prom.resolve(token)
        }
    })
    failedQueue = []
}

// 响应拦截器
httptool.interceptors.response.use(
    response => {
        return response
    }, 
    async error => {
        const originalRequest = error.config
        
        // 如果是token过期错误
        if (error.response?.status === 401 && 
            error.response?.data?.code === "token_not_valid" &&
            !originalRequest._retry) {
            
            // 如果已经在刷新token，将当前请求加入队列
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject })
                }).then(token => {
                    originalRequest.headers['Authorization'] = 'Bearer ' + token
                    return httptool(originalRequest)
                }).catch(err => {
                    return Promise.reject(err)
                })
            }
            
            originalRequest._retry = true
            isRefreshing = true
            
            try {
                const refreshToken = window.localStorage.getItem('refreshToken')
                if (!refreshToken) {
                    throw new Error('No refresh token available')
                }
                
                // 刷新token
                const response = await axios.post(REFRESH_URL, { 
                    refresh: refreshToken 
                })
                
                const newAccessToken = response.data.access
                
                // 保存新token
                window.localStorage.setItem('accessToken', newAccessToken)

                // 更新请求头
                originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken
                
                // 处理队列中的请求
                processQueue(null, newAccessToken)
                
                // 重试原始请求
                return httptool(originalRequest)
                
            } catch (refreshError) {
                // 刷新失败，清空token并跳转到登录页
                processQueue(refreshError, null)
                const authStore = useAuthStore();
                authStore.logout()
                showError("用户登录已过期，请重新登录!")
                return Promise.reject(refreshError)
            } finally {
                isRefreshing = false
            }
        }
        
        return Promise.reject(error)
    }
)

export default httptool