<script>
import { useAuthStore } from '@/stores/auth.js'
import { showWarning } from '@/utils/message.js'

const authStore = useAuthStore()

export default {
    data() {
        return {
            showHeader: true,
            lastScrollPosition: 0,
            isShow: false,
            display: ''
        }
    },
    computed: {
        hasLogin() {
            return authStore.user === null
        },
        avatar() {
            return authStore.user === null ? null : authStore.user.avatar
        },
        username() {
            return authStore.user === null ? null : authStore.user.userName
        },
        isHead(){
            return authStore.user !== null && authStore.user.userType === "head"
        },

    },
    methods: {
        login() {
            this.$router.push('/login')
        },
        logout() {
            authStore.logout()
        },
        onScroll() {
            const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop
            if (currentScrollPosition > 40) {
                this.showHeader = false
            } else {
                this.showHeader = true

            }
            this.lastScrollPosition = currentScrollPosition
        },
        errorHandler() {
            return true
        },
        toBackstage() {
            this.$router.push('/adminPanel')
        },
        toHome() {
            this.$router.push('/')
        },
        enter() {
            this.isShow = true
            this.display = 'unset'
        },
        leave() {
            this.isShow = false
            this.display = 'none'
        },
        toUserCenter(){
            this.$router.push('/userCenter')
        },
        toChat() {
            if (this.hasLogin) {
                showWarning('请先登录后再使用AI助手')
            } else {
                this.$router.push('/chat')
            }
        }

    },
    mounted() {
        window.addEventListener('scroll', this.onScroll);
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.onScroll)
    }
}

</script>


<template>
    <div class="toolbar-container myBetween" v-show="showHeader">
        <div class="toolbar-title">
            <h2>CODEJOURNEY</h2>
        </div>
        <div>
            <ul class="scroll-menu">
                <li>
                    <div class="my-menu" @click="toHome">
                        <span>🏡 首页</span>
                    </div>
                </li>
                <li>
                    <div class="my-menu" @click="toChat">
                        <span>💬 AI</span>
                    </div>
                </li>
                <li>
                    <div class="my-menu" @click="toBackstage" v-show="isHead">
                        <span>💻️ 后台</span>
                    </div>
                </li>
                <li>
                    <div class="header-avatar-wrap" v-if="hasLogin" @click="login">
                        <div class="default-login"> 登录 </div>
                    </div>
                    <div class="header-avatar-wrap" v-else @mouseenter="enter" @mouseleave="leave">
                        <div class="header-wrap-hover" :style="{ display: display }"></div>
                        <el-avatar :size="40" :src="avatar" @error="errorHandler"
                            style="border: 2px solid #fff;transition: transform 0.3s ease;" class="my-avatar">
                            <img src="https://niu.codejourney.cn/default_avatar.jpeg" />
                        </el-avatar>
                        <div class="v-popover">
                            <div class="avatar-panel-popover" :class="{ 'popShow': isShow, 'popHide': !isShow }"
                                v-show="isShow">
                                <div
                                    style="color: rgb(24, 25, 28); text-align: center; font-weight: bold; font-size: 18px; margin-top: 25px;">
                                    <span>{{ username }}</span>
                                </div>
                                <div class="single-item" @click="toUserCenter">
                                    <div>
                                        <i aria-hidden="true" class="fa fa-user-circle"></i>
                                        <span style="margin-left: 5px;">个人中心</span>
                                    </div>
                                    <el-icon>
                                        <ArrowRight />
                                    </el-icon>
                                </div>
                                <div class="placeholder"></div>
                                <div class="single-item" @click="logout">
                                    <div>
                                        <i aria-hidden="true" class="fa fa-sign-out"></i>
                                        <span style="margin-left: 5px;">退出登录</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>

    </div>
</template>


<style scoped>
.toolbar-container {
    width: 100%;
    height: 60px;
    color: var(--color-white);
    position: fixed;
    z-index: 100;
    user-select: none;
    transition: all 0.3s ease-in-out;
}

.toolbar-container:hover {
    background-color: rgba(0, 0, 0, 0.5);
}

.toolbar-title {
    margin-left: 30px;
}

.scroll-menu {
    margin: 0 25px 0 0;
    display: flex;
    justify-content: flex-end;
    padding: 0;
}

.scroll-menu li {
    list-style: none;
    margin: 0 8px;
    font-size: 17px;
    height: 60px;
    line-height: 60px;
    position: relative;
    cursor: pointer;
}

.my-menu:after {
    content: "";
    display: block;
    position: absolute;
    bottom: 0;
    height: 6px;
    background-color: var(--color-orange);
    width: 100%;
    max-width: 0;
    transition: max-width .25s ease-in-out;
}

.my-menu:hover:after {
    max-width: 100%;
}

.my-menu:hover {
    color: var(--color-orange);
}

.header-avatar-wrap {
    position: relative;
    margin-top: 10px;
    width: 40px;
    height: 40px;
    cursor: pointer;
}

.header-avatar-wrap:hover .my-avatar {
    transform: translate(-100px, 40px) scale(1.6);
    position: relative;
    z-index: 2;
}

.default-login {
    font-size: 15px;
    border-radius: 50%;
    background-color: #ff8cb0;
    text-align: center;
    line-height: 40px;
    color: var(--color-white);
}

.v-popover {
    position: absolute;
    z-index: 1;
    padding-top: 20px;
    margin-left: -110px;
    top: 100%;
    left: 50%;
    transform: translate3d(-50%, 0, 0);
}

.single-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 14px;
    height: 38px;
    border-radius: 8px;
    color: #61666d;
    font-size: 14px;
    cursor: pointer;
    transition: background-color .3s;
    margin-bottom: 2px;
}

.single-item:hover {
    background-color: #f1f2f3;
}

.popHide {
    animation: fade-out .2s ease-out forwards;
    transform-origin: top;
}

.popShow {
    animation: fade-in .2s ease-out forwards;
    transform-origin: top;
}

.avatar-panel-popover {
    width: 300px;
    background-color: var(--color-white);
    border-radius: 8px;
    padding: 0 24px 18px;
    box-shadow: 0 0 30px rgba(0, 0, 0, .1);
    border: 1px solid #e3e5e7;
}

.placeholder {
    margin: 6px 0 12px 0;
    border-bottom: 1px solid #ddd;
}

.header-wrap-hover {
    position: absolute;
    width: 160px;
    height: 70px;
    top: -10px;
    left: -120px;
}
</style>
