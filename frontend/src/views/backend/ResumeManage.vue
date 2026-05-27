<script setup>
import { ref, onMounted } from 'vue'
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import { uploadMedia, updateWebSettings, getWebSettings } from '@/api/index.js'
import { showError, showInfo, showSuccess } from '@/utils/message.js'

const siteSettings = ref({
    resumeUrl: '',
})

const resumeOldURL = ref('')
const resumeFile = ref(null)
const isSaving = ref(false)

async function customUploadResume(file) {
    const allowedTypes = ['application/pdf']
    const maxSize = 10 * 1024 * 1024 // 10MB

    if (!allowedTypes.includes(file.file.type)) {
        showError('仅支持 PDF 格式')
        return
    }
    if (file.file.size > maxSize) {
        showError('文件不能超过 10MB')
        return
    }

    if (file.file) {
        siteSettings.value.resumeUrl = URL.createObjectURL(file.file)
        resumeFile.value = file
    }
}

async function uploadResumeToQiniu(file) {
    const formData = new FormData()
    const filename = `resume${Date.now()}.pdf`
    formData.append('fileName', filename)
    formData.append('type', 'resume')
    formData.append('storeType', 'qiniu')
    formData.append('file', file.file)
    formData.append('old_src_path', resumeOldURL.value)

    try {
        const response = await uploadMedia(formData)
        return response.data.data.url
    } catch (error) {
        showError('简历上传失败: ' + error.message)
    }
}

async function saveSettings() {
    if (resumeFile.value) {
        showInfo('正在上传简历...')
        siteSettings.value.resumeUrl = await uploadResumeToQiniu(resumeFile.value)
    }

    isSaving.value = true
    try {
        await updateWebSettings(siteSettings.value)
        localStorage.setItem("webInfo", JSON.stringify(siteSettings.value))
        showSuccess('简历保存成功')
        resumeFile.value = null
    } catch (error) {
        showError('保存失败，请重试')
    } finally {
        isSaving.value = false
    }
}

async function fetchSettings() {
    const response = await getWebSettings()
    siteSettings.value.resumeUrl = response.data.data.resumeUrl || ''
    resumeOldURL.value = siteSettings.value.resumeUrl
}

onMounted(() => {
    fetchSettings()
})
</script>

<template>
    <Header></Header>
    <SideBar></SideBar>

    <div class="content-box">
        <div class="settings-container">
            <div class="page-header">
                <h1 class="page-title">简历管理</h1>
                <p class="page-subtitle">上传和管理您的简历 PDF</p>
            </div>

            <div class="resume-content">
                <el-card class="setting-card">
                    <template #header>
                        <div class="card-header">
                            <el-icon>
                                <Document />
                            </el-icon>
                            <span>简历 PDF</span>
                        </div>
                    </template>

                    <el-form-item label="上传简历">
                        <el-upload class="upload-demo" drag :auto-upload="true"
                            :show-file-list="false" :http-request="customUploadResume" accept=".pdf">
                            <div v-if="siteSettings.resumeUrl" class="pdf-preview">
                                <el-icon><Document /></el-icon>
                                <span>已上传简历，点击可重新上传</span>
                            </div>
                            <div v-else class="upload-area">
                                <el-icon class="el-icon--upload">
                                    <UploadFilled />
                                </el-icon>
                                <div class="el-upload__text">
                                    拖拽 PDF 到此处或 <em>点击上传</em>
                                </div>
                            </div>
                        </el-upload>
                        <div class="form-tip">仅支持 PDF 格式，单个文件不能超过 10MB</div>
                    </el-form-item>

                    <div class="action-buttons">
                        <el-button type="primary" :loading="isSaving" @click="saveSettings" size="large">
                            保存简历
                        </el-button>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>

<style scoped>
.content-box {
    position: absolute;
    left: 0px;
    right: 0;
    top: 70px;
    bottom: 0;
    transition: left .3s ease-in-out;
    background: #f5f7fa;
    padding: 20px;
    overflow-y: auto;
}

.settings-container {
    max-width: 800px;
    margin: 0 auto;
}

.page-header {
    margin-bottom: 5px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.page-title {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
    margin: 0 0 8px 0;
}

.page-subtitle {
    font-size: 14px;
    color: #909399;
    margin: 0;
}

.resume-content {
    padding: 20px 0;
}

.setting-card {
    border-radius: 8px;
    border: 1px solid #ebeef5;
}

.setting-card:deep(.el-card__header) {
    border-bottom: 1px solid #ebeef5;
    background: #fafbfc;
    padding: 18px 20px;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #303133;
}

.card-header .el-icon {
    font-size: 18px;
    color: #409EFF;
}

.setting-card:deep(.el-card__body) {
    padding: 20px;
}

:deep(.el-form-item) {
    margin-bottom: 10px;
}

.form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 4px;
    line-height: 1.4;
}

.upload-demo {
    width: 100%;
}

.upload-area {
    padding: 40px 0;
    text-align: center;
    color: #909399;
}

.upload-area .el-icon--upload {
    font-size: 48px;
    color: #c0c4cc;
    margin-bottom: 16px;
}

.pdf-preview {
    padding: 40px 0;
    text-align: center;
    color: #67c23a;
}

.pdf-preview .el-icon {
    font-size: 48px;
    margin-bottom: 16px;
    display: block;
}

.action-buttons {
    margin-top: 30px;
    text-align: center;
}

.action-buttons .el-button {
    min-width: 120px;
}
</style>