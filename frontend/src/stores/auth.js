import { defineStore } from "pinia"
import { ref } from "vue"
import { login as loginApi, verify as verifyApi } from "@/api/index.js"

export const useAuthStore = defineStore("auth", () => {
    const user = ref(null)
    const accessToken = ref(null)
    const refreshToken = ref(null)
    let verifyTimer = null
    const VERIFY_INTERVAL = 30 * 60 * 1000 // 2分钟


    function initialize() {
      const storedUser = localStorage.getItem("user")
      if (storedUser) {
        user.value = JSON.parse(storedUser)
        startVerifyTimer()
      }
    }

    // 启动定时验证
    function startVerifyTimer() {
      stopVerifyTimer()
      verifyTimer = setInterval(async () => {
        try {
          await verifyApi()
        } catch (error) {
          // 验证失败，说明登录已过期
          if (error.response?.status === 401) {
            logout()
          }
        }
      }, VERIFY_INTERVAL)
    }

    // 停止定时验证
    function stopVerifyTimer() {
      if (verifyTimer) {
        clearInterval(verifyTimer)
        verifyTimer = null
      }
    }

    async function login(credentials) {
      try {
        const response = await loginApi(credentials)
        if (response.status == 200) {
          user.value = response.data.data.user
          accessToken.value = response.data.data.accessToken
          refreshToken.value = response.data.data.refreshToken
          localStorage.setItem("user", JSON.stringify(response.data.data.user))
          localStorage.setItem("accessToken", response.data.data.accessToken)
          localStorage.setItem("refreshToken", response.data.data.refreshToken)
          startVerifyTimer() // 登录成功后启动定时验证
          return true
        }
        return false
      } catch (error) {
        return error
      }
    }

    function logout() {
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      stopVerifyTimer()
      localStorage.removeItem("user")
      localStorage.removeItem("accessToken")
      localStorage.removeItem("refreshToken")
    }

    function setUser(updateUser){
      user.value = updateUser
    }

    // 判断是否已登录
    function hasLogin(){
      return user.value
    }

    return {
      user,
      accessToken,
      initialize,
      login,
      logout,
      setUser,
      hasLogin,
      startVerifyTimer,
      stopVerifyTimer
    }
  }
)
