<script setup>
import Header from '@/components/frontend/Header.vue'
import BackToTop from '@/components/frontend/BackToTop.vue'
import { useAuthStore } from '@/stores/auth.js'
import { showError, showSuccess } from "@/utils/message.js"
import { sendVerificationCode as sendCodeApi, updateUser, uploadMedia } from '@/api/index.js'
import { ref, reactive } from 'vue'

const authStore = useAuthStore()


const getGender = () => {
    if (authStore.user.userSex === 'notall') return 'notall'
    else if (authStore.user.userSex === 'boy') return 'boy'
    else return 'girl'
}

const avatar = ref(authStore.user.avatar)
const email = ref(authStore.user.email)
const emailTitle = ref(authStore.user.email ? "绑定邮箱" : "修改邮箱")
const emailDialog = ref(false)
const avatarDialog = ref(false)
const fileList = ref([])
const fileNums = 1
const uploadRef = ref()

const formData = reactive({
    username: authStore.user.userName,
    gender: getGender(),
    introduce: authStore.user.introduce
})

const emailForm = reactive({
    email: "",
    password: "",
    code: ""
})

const getVerCode = async () => {
    if (emailForm.email === "") {
        showError("请先填写邮箱!")
        return
    }
    try {
        await sendCodeApi({ email: emailForm.email, type: "bindEmail" })
        showSuccess("验证码发送至邮箱, 请注意查收!")
    } catch (error) {
        const serverMsg = error.response?.data?.message
        showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
    }
}

const submitEmialForm = async () => {
    if (emailForm.email === "" || emailForm.password === "" || emailForm.code === "") {
        showError("信息不完整!")
        return
    }
    try {
        const response = await updateUser(authStore.user.userId, {
            userId: authStore.user.userId,
            email: emailForm.email,
            password: emailForm.password
        })
        localStorage.setItem("user", JSON.stringify(response.data.user))
        showSuccess("绑定成功!")
        email.value = emailForm.email
        emailForm.email = ""
        emailForm.password = ""
        emailForm.code = ""
        emailDialog.value = false
    } catch (error) {
        const serverMsg = error.response?.data?.message
        showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
    }
}

const bindEmail = () => {
    emailDialog.value = true
}

const emailDialogCancel = () => {
    emailDialog.value = false
}

const avatarDialogCancel = () => {
    avatarDialog.value = false
}

const submit = async () => {
    if (formData.username === "") {
        showError("用户名不能为空!")
        return
    }
    try {
        const response = await updateUser(authStore.user.userId, {
            username: formData.username,
            gender: formData.gender,
            introduce: formData.introduce
        })
        const user = response.data.user
        authStore.setUser(user)
        localStorage.setItem("user", JSON.stringify(user))
        showSuccess("保存成功!")
    } catch (error) {
        const serverMsg = error.response?.data?.message
        showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
    }
}

const clickAvatar = () => {
    avatarDialog.value = true
}

const customUpload = async (file) => {
    const allowedTypes = ['image/jpeg', 'image/png']
    const maxSize =  1024 * 1024 // 2MB

    if (!allowedTypes.includes(file.file.type)) {
        showError('仅支持 JPG 或 PNG 格式')
        return
    }
    if (file.file.size > maxSize) {
        showError('单个文件不能超过 1MB')
        return
    }

    let response = null
    const formData = new FormData()
    const filename = `${authStore.user.userName}${Date.now()}.jpg`
    formData.append('fileName', filename)
    formData.append('type', 'userAvatar')
    formData.append('file', file.file)
    formData.append('old_src_path', authStore.user.avatar)

    try {
        response = await uploadMedia(formData)
        avatar.value = response.data.data.url
    } catch (error) {
        const serverMsg = error.response?.data?.message
        showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
        return
    }
    try {
        response = await updateUser(authStore.user.userId, { avatar: avatar.value })
        if (response.data.code === 429) {
            showError(response.data.message || '今天已修改过头像，请明天再试')
            return
        }
        localStorage.setItem("user", JSON.stringify(response.data.user))
        showSuccess("头像更新成功")
        authStore.setUser(response.data.user)
    } catch (error) {
        const serverMsg = error.response?.data?.message
        if (error.response?.data?.code === 429) {
            showError(error.response.data.message || '今天已修改过头像，请明天再试')
            return
        }
        showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
    }
}

const handleSuccess = (response, file) => {
    fileList.value.push(file)
}

const handleExceed = (files) => {
    fileList.value = [files[0]]
}

const errorHandler = () => true

const updateAvatar = async () => {
    await uploadRef.value.submit()
    fileList.value = []
    avatarDialog.value = false
}
</script>


<template>
    <div>
        <Header></Header>
        <div class="main-container">
            <div>
                <el-dialog v-model="emailDialog" :center="true" :title="emailTitle" width="500"
                    :before-close="emailDialogCancel">
                    <div class="my-Center" style="flex-direction: column;">
                        <div>
                            <div>邮箱：</div>
                            <el-input v-model="emailForm.email"></el-input>
                        </div>
                        <div>
                            <div>密码：</div>
                            <el-input v-model="emailForm.password" type="password"></el-input>
                        </div>
                        <div>
                            <div>验证码：</div>
                            <el-input v-model="emailForm.code"></el-input>
                        </div>
                        <div style="flex-direction: row;">
                            <div class="myButton" @click="getVerCode">
                                <div style="background: rgb(131, 123, 199);">获取验证码</div>
                            </div>
                            <div class="myButton" style="margin-left: 12px;" @click="submitEmialForm">
                                <div style="background: rgb(131, 123, 199);">提交</div>
                            </div>
                        </div>
                    </div>
                </el-dialog>
                <el-dialog v-model="avatarDialog" :center="true" title="修改头像" width="500"
                    :before-close="avatarDialogCancel">
                    <el-upload ref="uploadRef" :http-request="customUpload" drag :limit="fileNums"
                        v-model:file-list="fileList" :on-success="handleSuccess" :on-exceed="handleExceed"
                        :auto-upload="false">
                        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                        <div class="el-upload__text">
                            拖拽上传或者 <em>点击上传</em>
                        </div>
                        <template #tip>
                            <div>
                                单个文件不能超过2Mb，仅支持 JPG 或 PNG 格式~
                            </div>
                        </template>
                    </el-upload>
                    <template #footer>
                        <div class="dialog-footer">
                            <el-button type="primary" @click="updateAvatar">
                                上传
                            </el-button>
                        </div>
                    </template>
                </el-dialog>
                <div class="user-container myCenter my-animation-hideToShow">
                    <div class="el-image my-el-image" style="position: absolute;">
                        <div class="image-slot"></div>
                    </div>
                    <div class="shadow-box-mini user-info">
                        <div class="user-left">
                            <div>
                                <el-avatar :size="60" :src="avatar" @error="errorHandler" @click="clickAvatar"
                                    style="border: 2px solid #fff;transition: transform 0.3s ease;" class="my-avatar">
                                    <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png" />
                                </el-avatar>
                            </div>
                            <div class="myCenter" style="margin-top: 12px;">
                                <div class="user-title">
                                    <div>用户名：</div>
                                    <div style="display: none;">手机号：</div>
                                    <div>邮箱：</div>
                                    <div>性别：</div>
                                    <div>简介：</div>
                                </div>
                                <div class="user-content">
                                    <div>
                                        <el-input v-model="formData.username"></el-input>
                                    </div>
                                    <div>
                                        <div>
                                            <span v-if="!email" class="changeInfo" @click="bindEmail">绑定邮箱</span>
                                            <div v-else>
                                                <span>{{ email }}</span>
                                                <span class="changeInfo" @click="bindEmail">修改邮箱</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div>
                                        <el-radio-group v-model="formData.gender">
                                            <el-radio value="notall">薛定谔的猫</el-radio>
                                            <el-radio value="boy">男</el-radio>
                                            <el-radio value="girl">女</el-radio>
                                        </el-radio-group>
                                    </div>
                                    <div>
                                        <el-input type="textarea" :maxlength="60" v-model="formData.introduce"
                                            show-word-limit></el-input>
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top: 20px;">
                                <div class="myButton" @click="submit()">
                                    <div style="background: rgb(131, 123, 199);">提交</div>
                                </div>
                            </div>
                        </div>
                        <div class="user-right"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <BackToTop />
</template>


<style scoped>
.user-container {
    width: 100vw;
    height: 100vh;
    position: relative;
}

.my-animation-hideToShow {
    -webkit-animation-name: hideToShow;
    animation-name: hideToShow;
}

[class*=my-animation-] {
    -webkit-animation-duration: 1s;
    animation-duration: 1s;
    -webkit-animation-timing-function: ease-out;
    animation-timing-function: ease-out;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
}

.my-el-image,
.my-el-image .image-slot {
    width: 100%;
    height: 100%;
}

.el-image {
    position: relative;
    display: inline-block;
    overflow: hidden;
}

.user-info {
    display: flex;
    width: 80%;
    z-index: 10;
    margin-top: 70px;
    height: calc(100vh - 130px);
    margin-bottom: 60px;
    border-radius: 10px;
    overflow: hidden;
}

.shadow-box-mini {
    box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}

.user-left {
    width: 50%;
    background: hsla(0, 0%, 100%, 0.7);
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-y: auto;
    padding: 20px;
}

.user-right {
    width: 50%;
    overflow-y: auto;
    background: hsla(0, 0%, 100%, 0.3);
    padding: 20px;
}

.user-title {
    text-align: right;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.user-title div {
    height: 55px;
    line-height: 55px;
    text-align: center;
}

.user-content>div {
    height: 55px;
    display: flex;
    align-items: center;
}

.user-content {
    text-align: left;
}

.changeInfo {
    color: #fff;
    font-size: .75rem;
    cursor: pointer;
    background: orange;
    padding: 3px;
    border-radius: .2rem;
}

.myButton {
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    position: relative;
    width: 66px;
    height: 33px;
    border-radius: 4px;
    color: #fff;
    font-size: 14px;
    overflow: hidden;
}


.myButton div {
    width: 66px;
    height: 33px;
    line-height: 33px;
    border-radius: 4px;
    text-align: center;
    position: absolute;
}

.my-Center {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 20px;
}

.my-Center div {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

@keyframes hideToShow {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}
</style>