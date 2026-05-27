<script setup>
import { ref, onMounted } from 'vue'
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import { uploadMedia, updateWebSettings, getWebSettings } from '@/api/index.js'
import { showError, showInfo, showSuccess } from '@/utils/message.js'

const siteSettings = ref({
    title: '',
    poem: '',
    author: '',
    icpNumber: '',
    contactEmail: '',
    copyright: '',
    backGroundPreview: '',
})

const imgOldURL = ref('')

const uploadLoading = ref(false)
const isSaving = ref(false)
const backGroundImageFile = ref(null)
const settingsForm = ref(null)

async function customUpload(file) {
    const allowedTypes = ['image/jpeg', 'image/png']
    const maxSize = 5 * 1024 * 1024 // 5MB

    if (!allowedTypes.includes(file.file.type)) {
        showError('仅支持 JPG 或 PNG 格式')
        return
    }
    if (file.file.size > maxSize) {
        showError('单个文件不能超过 5MB')
        return
    }

    if (file.file) {
        if (siteSettings.value.backGroundPreview) {
            URL.revokeObjectURL(siteSettings.value.backGroundPreview)
        }
        siteSettings.value.backGroundPreview = URL.createObjectURL(file.file)
        backGroundImageFile.value = file
    }
}



async function uploadBackGroundImageToQiniu(file) {
    const formData = new FormData()
    const filename = `sunboy${Date.now()}.jpg`
    formData.append('fileName', filename)
    formData.append('type', 'homebackground')
    formData.append('storeType', 'qiniu')
    formData.append('file', file.file)
    formData.append('old_src_path', imgOldURL.value)

    try {
        const response = await uploadMedia(formData)
        return response.data.data.url
    } catch (error) {
        showError('封面上传失败: ' + error.message)
    }
}

async function saveSettings() {
    if (backGroundImageFile.value) {
        showInfo('正在上传网站背景图片...')
        siteSettings.value.backGroundPreview = await uploadBackGroundImageToQiniu(backGroundImageFile.value)
    }

    isSaving.value = true
    try {
        await updateWebSettings(siteSettings.value)
        localStorage.setItem("webInfo", JSON.stringify(siteSettings.value))
        showSuccess('设置保存成功')
    } catch (error) {
        showError('保存失败，请重试')
    } finally {
        isSaving.value = false
    }
}

async function resetSettings() {
    const response = await getWebSettings()
    siteSettings.value = response.data.data
}

async function fetchSettings() {
    const response = await getWebSettings()
    siteSettings.value = response.data.data
    imgOldURL.value = siteSettings.value.backGroundPreview
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
            <!-- 页面标题 -->
            <div class="page-header">
                <h1 class="page-title">网站设置</h1>
                <p class="page-subtitle">配置您的网站基本信息、样式和功能</p>
            </div>

            <!-- 设置表单 -->
            <el-form ref="settingsForm" :model="siteSettings" label-position="top" class="settings-form">
                <el-row :gutter="24">
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-card class="setting-card">
                            <template #header>
                                <div class="card-header">
                                    <el-icon>
                                        <Edit />
                                    </el-icon>
                                    <span>网站基本信息</span>
                                </div>
                            </template>

                            <el-form-item label="网站名称" prop="title">
                                <el-input v-model="siteSettings.title" placeholder="请输入网站名称" maxlength="50"
                                    show-word-limit />
                            </el-form-item>

                            <el-form-item label="富有诗意的句子" prop="poem">
                                <el-input v-model="siteSettings.poem" type="textarea" :rows="3" placeholder="请输入..."
                                    maxlength="200" show-word-limit />
                            </el-form-item>

                            <el-form-item label="作者" prop="author">
                                <el-input v-model="siteSettings.author" placeholder="请输入作者名称" />
                            </el-form-item>

                            <el-form-item label="备案号" prop="icpNumber">
                                <el-input v-model="siteSettings.icpNumber" placeholder="请输入ICP备案号" />
                            </el-form-item>

                            <el-form-item label="联系邮箱" prop="contactEmail">
                                <el-input v-model="siteSettings.contactEmail" placeholder="请输入联系邮箱" type="email" />
                            </el-form-item>

                            <el-form-item label="版权信息" prop="copyright">
                                <el-input v-model="siteSettings.copyright" placeholder="请输入版权信息" />
                            </el-form-item>
                        </el-card>

                    </el-col>

                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <el-card class="setting-card">
                            <template #header>
                                <div class="card-header">
                                    <el-icon>
                                        <Picture />
                                    </el-icon>
                                    <span>背景设置</span>
                                </div>
                            </template>

                            <el-form-item label="背景图片">
                                <el-upload class="upload-demo" drag ref="upload" :auto-upload="true"
                                    :show-file-list="false" :http-request="customUpload">
                                    <div v-if="siteSettings.backGroundPreview" class="image-preview">
                                        <img :src="siteSettings.backGroundPreview" alt="背景预览" class="preview-image" />
                                    </div>
                                    <div v-else class="upload-area">
                                        <el-icon class="el-icon--upload" v-if="!uploadLoading">
                                            <UploadFilled />
                                        </el-icon>
                                        <div v-if="!uploadLoading" class="el-upload__text">
                                            拖拽图片到此处或 <em>点击上传</em>
                                        </div>
                                        <div v-if="uploadLoading" class="el-upload__text">
                                            上传中...
                                        </div>
                                    </div>
                                </el-upload>
                                <div class="form-tip">建议尺寸：1920x1080，支持 JPG、PNG 格式，单个文件不能超过 5MB</div>
                            </el-form-item>
                        </el-card>
                    </el-col>
                </el-row>

                <div class="action-buttons">
                    <el-button type="primary" :loading="isSaving" @click="saveSettings" size="large">
                        保存设置
                    </el-button>
                    <el-button @click="resetSettings" size="large">
                        重置
                    </el-button>
                </div>
            </el-form>
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
    max-width: 1200px;
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


.setting-card {
    margin-bottom: 0;
    border-radius: 8px;
    border: 1px solid #ebeef5;
    transition: all 0.3s ease;
    height: 100%;
}

.setting-card:hover {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
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

/* 表单样式 */
.settings-form {
    padding: 20px 0;
}

:deep(.el-form-item) {
    margin-bottom: 10px;
}

:deep(.el-form-item__label) {
    font-weight: 800;
    color: #606266;
    margin-bottom: 8px;
    padding: 0;
}

:deep(.el-input) .el-input__inner,
:deep(.el-textarea) .el-textarea__inner {
    border-radius: 6px;
    transition: all 0.3s ease;
}

:deep(.el-input) .el-input__inner:focus,
:deep(.el-textarea) .el-textarea__inner:focus {
    border-color: #409EFF;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

.form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 4px;
    line-height: 1.4;
}

.form-tip.warning {
    color: #e6a23c;
}


/* 上传组件 */
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

.image-preview {
    position: relative;
    padding: 20px 0;
}

.pdf-preview {
    padding: 40px 0;
    text-align: center;
    color: #67c23a;
}

.pdf-preview .el-icon {
    font-size: 48px;
    margin-bottom: 16px;
}

.preview-image {
    max-width: 100%;
    max-height: 200px;
    display: block;
    margin: 0 auto;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-actions {
    margin-top: 70px;
    text-align: center;
    margin: auto;
}

/* 预览容器 */
.preview-container {
    padding: 20px 0;
}

.preview-box {
    width: 100%;
    height: 200px;
    border-radius: 8px;
    border: 2px dashed #dcdfe6;
    overflow: hidden;
    position: relative;
    background-size: cover;
    background-position: center;
}

.preview-placeholder {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #909399;
    font-size: 14px;
}

/* 操作按钮 */
.action-buttons {
    margin-top: 40px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.action-buttons .el-button {
    min-width: 120px;
    margin: 0 8px;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .content-box {
        left: 0;
        padding: 10px;
    }

    .setting-card:deep(.el-card__body) {
        padding: 15px;
    }

    .page-header {
        padding: 15px;
    }

    .action-buttons {
        padding: 15px;
    }
}
</style>
