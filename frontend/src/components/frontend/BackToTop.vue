<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ArrowUp } from '@element-plus/icons-vue'

const showBackToTop = ref(false)

const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
}

const handleScroll = () => {
    showBackToTop.value = window.scrollY > 300
}

onMounted(() => {
    window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
    <transition name="fade">
        <div v-if="showBackToTop" class="back-to-top" @click="scrollToTop">
            <el-icon :size="20"><ArrowUp /></el-icon>
        </div>
    </transition>
</template>

<style scoped>
.back-to-top {
    position: fixed;
    right: 20px;
    bottom: 80px;
    width: 44px;
    height: 44px;
    background: rgba(131, 123, 199, 0.9);
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: background 0.3s;
}

.back-to-top:hover {
    background: rgb(131, 123, 199);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
