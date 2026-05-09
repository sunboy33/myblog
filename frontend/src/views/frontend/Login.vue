<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/frontend/Header.vue'
import BackToTop from '@/components/frontend/BackToTop.vue'
import bgImage from '@/assets/bg.jpg'

import { register as registerApi, sendVerificationCode as sendCodeApi } from '@/api/index.js'
import { showError, showSuccess } from '@/utils/message.js'
import { useAuthStore } from '@/stores/auth.js'
import { encrypt } from '@/utils/utils.js'

const router = useRouter()
const authStore = useAuthStore()


const bgURL = bgImage
const signUpForm = ref({ name: '', pass: '', pass2: '', email: '', code: '' })
const signInForm = ref({ name: '', pass: '' })
const attr = ref(['in-up'])
const showText = ref(true)
const second = ref(60)
let countdownTimer = null


function signInGhost() {
    attr.value = attr.value.filter(item => item !== 'right-panel-active')
    signUpForm.value = { name: '', pass: '', email: '', code: '' }
}

function signUpGhost() {
    attr.value.push('right-panel-active')
    signInForm.value = { name: '', pass: '' }
}

async function signIn() {
    if (!signInForm.value.name || !signInForm.value.pass) {
        showError('请先输入用户名或密码!')
        return
    }
    const message = await authStore.login({
        userName: signInForm.value.name,
        password: encrypt(signInForm.value.pass)
    })
    if (message === true) {
        showSuccess('登录成功!')
        router.push({ name: 'home' })
    } else {
        const serverMsg = message.response?.data?.message
        showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
    }
}

async function signUp() {
    if (signUpForm.value.name === '' || signUpForm.value.pass === '' || signUpForm.value.email === '') {
        showError('请先输入用户名或密码!')
        return
    }
    if (signUpForm.value.code === '') {
        showError('请输入验证码!')
        return
    }
    if (signUpForm.value.pass !== signUpForm.value.pass2) {
        showError('密码不一致!')
        return
    }

    try {
        const response = await registerApi(signUpForm.value)
        showSuccess('注册成功!')
        signUpForm.value = { name: '', pass: '', pass2: '', email: '', code: '' }
        showText.value = true
    } catch (error) {
        const serverMsg = error.response?.data?.message
        const defaultMsg = '网络请求失败，请检查网络或稍后重试'
        showError(serverMsg || defaultMsg)
    }
}

function changeSecond() {
    showText.value = false
    second.value = '60'

    if (countdownTimer) {
        clearInterval(countdownTimer)
    }

    countdownTimer = setInterval(() => {
        const current = parseInt(second.value)

        if (current <= 1) {
            showText.value = true
            second.value = '0'
            clearInterval(countdownTimer)
            countdownTimer = null
        } else {
            second.value = (current - 1).toString()
        }
    }, 1000)
}

async function getAuCode() {
    if (!signUpForm.value.email) {
        showError('请先输入邮箱号!')
        return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(signUpForm.value.email)) {
        showError('请输入有效的邮箱地址')
        return
    }

    changeSecond()

    try {
        const response = await sendCodeApi({ email: signUpForm.value.email, type: "register" })
        showSuccess('验证码已发送至邮箱, 请注意查看!')
    } catch (error) {
        const errorMessage = error.response?.data?.message || '验证码发送失败，请检查邮箱或稍后重试'
        showError(errorMessage)
    }
}
</script>

<template>
    <div class="container">
        <Header></Header>
        <div class="main-container myCenter">
            <div class="el-image" style="position: fixed;">
                <el-image :src="bgURL" fit="cover" />
            </div>
            <div :class="attr">
                <div class="form-container sign-up-container">
                    <form @submit.prevent="signUp" style="height: 100%;">
                        <div class="myCenter">
                            <h1>注册</h1>
                            <input type="text" placeholder="用户名" v-model="signUpForm.name" autocomplete="username">
                            <input type="password" placeholder="密码" v-model="signUpForm.pass" autocomplete>
                            <input type="password" placeholder="确认密码" v-model="signUpForm.pass2" autocomplete>
                            <input type="text" placeholder="邮箱" v-model="signUpForm.email">
                            <input type="text" placeholder="验证码" v-model="signUpForm.code">
                            <span v-if="showText" @click="getAuCode" class="getcode">获取验证码</span>
                            <span v-else class="getcode" style="cursor: default;">{{ second }}</span>
                            <button type="submit">注册</button>
                        </div>
                    </form>
                </div>
                <div class="form-container sign-in-container">
                    <form @submit.prevent="signIn" style="height: 100%;">
                        <div class="myCenter">
                            <h1 style="margin-bottom: 10%;">登录</h1>
                            <input type="text" placeholder="用户名/邮箱/手机号" v-model="signInForm.name" autocomplete>
                            <input type="password" placeholder="密码" v-model="signInForm.pass"
                                autocomplete="current-password">
                            <a style="margin-top: 4%; margin-bottom: 4%;">修改密码?</a>
                            <button type="submit">登录</button>
                        </div>
                    </form>

                </div>
                <div class="overlay-container">
                    <div class="overlay">
                        <div class="overlay-panel myCenter overlay-left">
                            <h1>已有账号?</h1>
                            <p>请登录🚀</p>
                            <button class="ghost" @click="signInGhost">登录</button>
                        </div>
                        <div class="overlay-panel myCenter overlay-right">
                            <h1 style="margin-bottom: 10%;">没有账号?</h1>
                            <p style="margin-bottom: 20px;">立即注册吧😊</p>
                            <button class="ghost" @click="signUpGhost">注册</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <BackToTop />
</template>

<style scoped>
.main-container {
    height: 100vh;
}

.el-image {
    position: relative;
    display: inline-block;
    overflow: hidden;
    width: 100%;
    height: 100%;
}


.in-up {
    opacity: 0.9;
    border-radius: 10px;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15),
        0 10px 10px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
    width: 750px;
    max-width: 100%;
    min-height: 450px;
    margin: 20px;

}

.form-container {
    position: absolute;
    height: 100%;
    transition: all 0.5s ease-in-out;
}

.sign-up-container {
    left: 0;
    width: 50%;
    opacity: 0;
}

.myCenter {
    display: flex;
    justify-content: center;
    align-items: center;
}

.sign-in-container {
    left: 0;
    width: 50%;
}

.overlay-container {
    position: absolute;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: all 0.5s ease-in-out;
}

.overlay {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: #fff;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
}

.overlay-panel {
    position: absolute;
    top: 0;
    flex-direction: column;
    height: 100%;
    width: 50%;
    transition: all 0.5s ease-in-out;
}

.overlay-left {
    transform: translateY(-20%);
}

.overlay-right {
    right: 0;
    transform: translateY(0);
}


h1 {
    font-weight: bold;
    margin: 0;
}

h2 {
    text-align: center;
}

p {
    font-size: 14px;

}

span {
    font-size: 14px;
}


button {
    border-radius: 20px;
    border: 1px solid #FF4B2B;
    background-color: #FF4B2B;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: bold;
    padding: 12px 45px;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 80ms ease-in;
    cursor: pointer;
}

button:active {
    transform: scale(0.95);
}

button:focus {
    outline: none;
}

button.ghost {
    background-color: transparent;
    border: 1px solid #fff;
}



.form-container input {
    background: #eee;
    border-radius: 2px;
    border: none;
    padding: 12px 15px;
    margin: 10px 0;
    width: 100%;
    outline: none;
}



.form-container div {
    background: #fff;
    flex-direction: column;
    padding: 0 20px;
    height: 100%;
}



.right-panel-active .sign-in-container {
    transform: translateY(100%);
    opacity: 1;
}


.right-panel-active .sign-up-container {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: show 0.6s;
}


.right-panel-active .overlay-container {
    transform: translateX(-100%);
}



.right-panel-active .overlay {
    transform: translateX(50%);
}

.right-panel-active .overlay-left {
    transform: translateY(0);
}

.in-up a,
.getcode {
    color: #000;
    font-size: 14px;
    text-decoration: none;
    margin: 15px 0;
    cursor: pointer;
}


.in-up button:hover {
    transform: scale(1.1);
}


@keyframes show {

    0%,
    49.99% {
        opacity: 0;
        z-index: 1;
    }

    50%,
    100% {
        opacity: 1;
        z-index: 5;
    }
}
</style>
