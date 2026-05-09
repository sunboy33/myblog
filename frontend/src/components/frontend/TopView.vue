<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

const webInfo = JSON.parse(localStorage.getItem('webInfo'))

const showTopView = ref(true)
const isRunning = ref(true)
const bgImage = computed(() => webInfo.backGroundPreview)
const title = computed(() => webInfo.title)
const poem = ref('')

function sleep(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000))
}

function scrollDown() {
    const scrollY = window.innerHeight * 0.5;
    window.scrollTo({
        top: scrollY,
        behavior: "smooth"
    });
}

async function poemChange() {
    const sourcePoem = webInfo.poem
    
    const len = sourcePoem.length
    poem.value = ""
    await sleep(2)
    while (isRunning.value) {
        for (let i = 0; i <= len; i++) {
            if (!isRunning.value) return
            poem.value = sourcePoem.substring(0, i);
            await sleep(0.1);
        }
        if (!isRunning.value) return
        await sleep(2);
        for (let i = len + 1; i >= 0; i--) {
            if (!isRunning.value) return
            poem.value = sourcePoem.substring(0, i);
            await sleep(0.1);
        }
        if (!isRunning.value) return
        await sleep(2);
    }
}

onMounted(async () => {
    // await webSetting.initialize()
    poemChange()
})

onBeforeUnmount(() => {
    isRunning.value = false
})
</script>

<template>
    <div class="topview-container">
        <div class="el-image" v-if="bgImage">
            <img :src="bgImage" style="object-fit: cover;" class="el-image__inner">
        </div>
        <div class="el-image" v-else>
            <img src="@/assets/home_bg.webp" style="object-fit: cover;" class="el-image__inner">
        </div>

        <div class="signature-wall myCenter my-animation-hideToShow" style="height: 50vh;">
            <h1 class="playful">
                <span>{{ title }}</span>
            </h1>
            <div class="printer">
                <div>
                    <h3>
                        {{ poem }}
                        <span class="cursor">|</span>
                    </h3>
                </div>
            </div>
            <div id="bannerWave1"></div>
            <div id="bannerWave2"></div>
            <i class="el-icon-arrow-down" @click="scrollDown"></i>
        </div>
    </div>



</template>


<style scoped>
.el-image {
    height: 50vh;
    width: 100vw;
    position: fixed;
    z-index: -1;
    animation: header-effect 2s ease 0s 1 normal none running;
    display: inline-block;
    overflow: hidden;
}

.el-image__inner {
    vertical-align: top;
    width: 100%;
    height: 100%;
    filter: brightness(0.8);
}

.signature-wall {
    display: flex;
    flex-direction: column;
    position: relative;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    overflow: hidden;
}

.signature-wall.myCenter {
    margin-top: 20px;
}

.playful {
    color: var(--color-white);
}

h1 {
    display: block;
    font-size: 40px;
    margin-block-start: 0.67em;
    margin-block-end: 0.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.printer {
    cursor: pointer;
    color: var(--color-white);
    background: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
    padding-left: 10px;
    padding-right: 10px;
}

h3 {
    display: block;
    font-size: 1.17em;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.cursor {
    margin-left: 1px;
    animation: hideToShow .7s infinite;
    font-weight: 200;
}

#bannerWave1,
#bannerWave2 {
    position: absolute;
    bottom: 0px;
    animation: gradientBG 120s linear infinite;
}

#bannerWave1 {
    height: 84px;
    background: url('@/assets/bannerWave1.png') repeat-x;
    width: 200%;
    z-index: 10;
}

#bannerWave2 {
    height: 100px;
    background: url('@/assets/bannerWave2.png') repeat-x;
    width: 400%;
    z-index: 5;
}

.el-icon-arrow-down {
    font-size: 40px;
    font-weight: 700;
    color: var(--color-white);
    animation: my-shake 1.5s ease-out infinite;
    z-index: 15;
    cursor: pointer;
}

.el-icon-arrow-down:before {
    content: "\e6df";
}

@font-face {
    font-family: element-icons;
    src: url(@/assets/element-icons.535877f5.woff) format("woff");
    font-weight: 400;
    font-display: "auto";
    font-style: normal
}
</style>