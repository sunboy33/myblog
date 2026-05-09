<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { ElMessageBox } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import moment from 'moment'
import { useAuthStore } from '@/stores/auth.js'
import { uploadMedia, deleteMedia, getSortOperation, addLabel, addArticle, updateArticle, getArticleById } from '@/api/index.js'
import { showError, showSuccess } from '@/utils/message.js'
import { ElLoading } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
let loadingInstance = null

const title = ref('')
const cover = ref('')
const text = ref('')
const isComment = ref(true)
const isRecommend = ref(false)
const types = ref([])
const label = ref([])
const permissions = [
    { value: '公开', label: '公开' },
    { value: '登录', label: '登录' }
]
const type = ref('')
const limit = ref('')
const coverDialogVisible = ref(false)
const fileList = ref([])
const fileNums = 1
const isEditMode = ref(false)
const id = ref(0)
const toolbarsExcludeArray = ['github', 'htmlPreview', 'fullscreen']
const coverName = ref('')
const upload = ref(null)
let tempCoverFile = null
let tempCoverPreview = null

/** 正则表达式提取图片链接 */
const extractImgUrls = (markdown) => {
    const regex = /!\[.*?\]\((.*?)\)/g
    const urls = []
    let match
    while ((match = regex.exec(markdown)) !== null) {
        urls.push(match[1])
    }
    return urls
}

/** 监听文本变化， 是否删除图片 */
watch(text, async (newText, oldText) => {
    const oldUrls = extractImgUrls(oldText)
    const newUrls = extractImgUrls(newText)
    const deletedUrls = oldUrls.filter(url => !newUrls.includes(url))
    for (const url of deletedUrls) {
        try {
            await deleteMedia(url)
        } catch (error) {
            const serverMsg = error.response?.data?.message
            const defaultMsg = '网络请求失败，请检查网络或稍后重试'
            showError(serverMsg || defaultMsg)
        }
    }
})

const handleExceed = (files) => {
    fileList.value = [files[0]]
}

const customUpload = (file) => {
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
        tempCoverFile = file
        tempCoverPreview = URL.createObjectURL(file.file)
        cover.value = tempCoverPreview
        coverName.value = tempCoverPreview
    }
}

const uploadCoverToQiniu = async (file, type) => {
    const formData = new FormData()
    const filename = `${authStore.user.userName}${Date.now()}.jpg`
    formData.append('fileName', filename)
    formData.append('type', type)
    formData.append('storeType', 'qiniu')
    formData.append('file', file.file)

    try {
        const response = await uploadMedia(formData)
        return response.data.data.url
    } catch (error) {
        const serverMsg = error.response?.data?.message
        const defaultMsg = '网络请求失败，请检查网络或稍后重试'
        showError(serverMsg || defaultMsg)
    }
}


/** 富文本编辑器上传图片 */
const onUploadImg = async (files, callback) => {
    const res = await Promise.all(
        files.map((file, index) => {
            return new Promise((rev, rej) => {
                const ext = file.name.split('.').pop()
                const filename = `${authStore.user.userName}${Date.now()}_${index}.${ext}`
                const formData = new FormData();
                formData.append('fileName', filename)
                formData.append('type', 'image')
                formData.append('storeType', 'qiniu')
                formData.append('file', file)

                uploadMedia(formData).then((res) => rev(res))
                    .catch((error) => rej(error));
            });
        })
    );

    callback(res.map((item) => item.data.data.url))
}

const resetForm = () => {
    title.value = ''
    cover.value = ''
    text.value = ''
    isComment.value = true
    isRecommend.value = false
    type.value = ''
    label.value = []
    limit.value = ''
}

const uploadCover = () => {
    coverDialogVisible.value = true
}

const cancel = () => {
    coverDialogVisible.value = false
    fileList.value = []
}

const handleUpLoadImg = async () => {
    upload.value?.submit()
    fileList.value = []
    coverDialogVisible.value = false
}

const handleAddSave = async () => {
    loadingInstance = ElLoading.service({ text: '正在保存文章，请稍候...' })
    if (tempCoverFile) {
        cover.value = await uploadCoverToQiniu(tempCoverFile, 'background')
        coverName.value = cover.value  // 上传成功后显示服务器 URL
    }
    const now = moment()
    if (cover.value === '') {
        const coverFiles = import.meta.glob('/cover/*', { eager: true })
        const keys = Object.keys(coverFiles)
        const randomKey = keys[Math.floor(Math.random() * keys.length)]
        cover.value = randomKey.replace('/public', '')
    }
    const articleData = {
        author: authStore.user.userName,
        title: title.value,
        type: type.value,
        label: label.value,
        limit: limit.value,
        cover: cover.value,
        comment: isComment.value,
        recommend: isRecommend.value,
        text: text.value,
        createtime: now.format('YYYY-MM-DD HH:mm:ss'),
        finalltime: now.format('YYYY-MM-DD HH:mm:ss')
    }
    console.log(articleData)
    const labelData = { label: label.value, type: type.value }
    try {
        await addLabel(labelData)
        await addArticle(articleData)
        loadingInstance.close()
        showSuccess('保存成功!')
        router.push('/ArticleManage')
    } catch (error) {
        loadingInstance.close()
        const serverMsg = error.response?.data?.message
        const defaultMsg = '网络请求失败，请检查网络或稍后重试'
        showError(serverMsg || defaultMsg)
    }
}

const handleEditSave = async () => {
    loadingInstance = ElLoading.service({ text: '正在保存文章，请稍候...' })
    const now = moment()
    const articleData = {
        author: authStore.user.userName,
        title: title.value,
        type: type.value,
        label: label.value,
        limit: limit.value,
        cover: cover.value,
        comment: isComment.value,
        recommend: isRecommend.value,
        text: text.value,
        finalltime: now.format('YYYY-MM-DD HH:mm:ss')
    }
    const labelData = { label: label.value, type: type.value }
    try {
        await addLabel(labelData)
        await updateArticle(id.value, articleData)
        loadingInstance.close()
        showSuccess('保存成功!')
        router.push('/ArticleManage')
    } catch (error) {
        loadingInstance.close()
        const serverMsg = error.response?.data?.message
        const defaultMsg = '网络请求失败，请检查网络或稍后重试'
        showError(serverMsg || defaultMsg)
    }
}

onMounted(async () => {
    try {
        const response = await getSortOperation()
        types.value = response.data.types
    } catch (error) {
        const serverMsg = error.response?.data?.message
        const defaultMsg = '网络请求失败，请检查网络或稍后重试'
        showError(serverMsg || defaultMsg)
    }

    if (route.query.articleId !== undefined) {
        try {
            const response = await getArticleById(route.query.articleId)
            id.value = response.data.article.id
            title.value = response.data.article.title
            cover.value = response.data.article.cover
            coverName.value = response.data.article.cover  // 编辑时显示服务器上的封面路径
            text.value = response.data.article.text
            isComment.value = response.data.article.comment
            isRecommend.value = response.data.article.recommend
            type.value = response.data.article.type
            label.value = response.data.article.label
            limit.value = response.data.article.limit
            isEditMode.value = true
        } catch (error) {
            const serverMsg = error.response?.data?.message
            const defaultMsg = '网络请求失败，请检查网络或稍后重试'
            showError(serverMsg || defaultMsg)
        }
    }
})
</script>

<template>
    <Header></Header>
    <SideBar></SideBar>
    <div class="content-box">
        <div class="admin-content">
            <div>
                <el-tag type="primary" class="my-tag">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <el-icon :size="20">
                            <Document />
                        </el-icon>
                        <span>文章信息</span>
                    </div>
                </el-tag>
                <el-form>
                    <el-form-item class="is-required">
                        <label class="el-form-item__label" for="articleTitle" style="width: 80px;">标题</label>
                        <el-input v-model="title" type="text" autocomplete="off" size="large" />
                    </el-form-item>

                    <el-form-item>
                        <label class="el-form-item__label" for="articleCover" style="width: 80px;">封面</label>
                        <div style="display: flex;width: 100%;">
                            <el-input v-model="coverName" type="text" placeholder="默认使用随机图片" autocomplete="off"
                                size="large" style="flex: 1;" />
                            <div class="el-image" style="margin-left: 10px;">
                                <div v-if="cover === ''" class="el-image__error">无</div>
                                <div v-else>
                                    <el-image :src="cover" fit="cover">
                                    </el-image>
                                </div>
                            </div>
                            <el-button class="upload-button" @click="uploadCover">上传</el-button>

                            <el-dialog v-model="coverDialogVisible" :center="true" title="文件" width="500"
                                :before-close="cancel">
                                <el-upload ref="upload" :drag="true" :limit="fileNums" v-model:file-list="fileList"
                                    :on-exceed="handleExceed" :auto-upload="false" :http-request="customUpload">
                                    <el-icon><upload-filled /></el-icon>
                                    <div>
                                        拖拽上传或者
                                        <em>点击上传</em>
                                    </div>
                                    <template #tip>
                                        <div>单个文件不能超过5Mb，仅支持 JPG 或 PNG 格式~</div>
                                    </template>
                                </el-upload>
                                <template #footer>
                                    <div class="dialog-footer">
                                        <el-button type="primary" @click="handleUpLoadImg">
                                            上传
                                        </el-button>
                                    </div>
                                </template>
                            </el-dialog>
                        </div>
                    </el-form-item>

                    <el-form-item class="is-required">
                        <MdEditor v-model="text" :toolbarsExclude="toolbarsExcludeArray" @onUploadImg="onUploadImg" />
                    </el-form-item>

                    <el-form-item>
                        <label class="el-form-item__label" style="width: 80px;">启用评论</label>
                        <el-tag :type="isComment == true ? 'success' : 'danger'" size="large" class="my-center">{{
                            isComment === true ? '是' : '否' }}</el-tag>
                        <el-switch v-model="isComment" style="margin-left: 10px;" />
                    </el-form-item>

                    <el-form-item>
                        <label class="el-form-item__label" style="width: 80px;">是否推荐</label>
                        <el-tag :type="isRecommend == true ? 'success' : 'danger'" size="large" class="my-center">{{
                            isRecommend === true ? '是' : '否' }}</el-tag>
                        <el-switch v-model="isRecommend" style="margin-left: 10px;" />
                    </el-form-item>

                    <el-form-item>
                        <label class="el-form-item__label" style="width: 80px;">文章类别</label>
                        <el-select v-model="type" placeholder="请选择分类" size="large" style="width: 240px">
                            <el-option v-for="item in types" :key="item.value" :label="item.type" :value="item.type" />
                        </el-select>
                    </el-form-item>

                    <el-form-item>
                        <label class="el-form-item__label" style="width: 80px;">文章标签</label>
                        <el-input-tag size="large" v-model="label" :max="3" placeholder="最多选择3个标签"
                            style="width: 40%;" />
                    </el-form-item>

                    <el-divider border-style="dashed" style="border-width: 3px;" />

                    <el-form-item>
                        <label class="el-form-item__label" style="width: 80px;">文章权限</label>
                        <el-select v-model="limit" placeholder="文章访问类型" size="large" style="width: 240px">
                            <el-option v-for="item in permissions" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" style="margin-left: 40%;"
                            @click="isEditMode ? handleEditSave() : handleAddSave()">保存</el-button>
                        <el-button type="danger" @click="resetForm">重置信息</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.content-box {
    position: absolute;
    left: 130px;
    right: 0;
    top: 70px;
    bottom: 0;
    transition: left .3s ease-in-out;
}

.admin-content {
    width: auto;
    height: 100%;
    padding: 30px;
    overflow-y: scroll;
}

.my-tag {
    display: inline-block;
    margin-bottom: 20px;
    width: 100%;
    background: #f4e1c0;
    border: none;
    height: 40px;
    line-height: 40px;
    font-size: 16px;
    color: #000;
}

.el-form-item__label {
    align-items: center;
    text-align: right;
    vertical-align: middle;
    float: left;
    font-size: 14px;
    color: #606266;
    line-height: 40px;
    padding: 0 12px 0 0;
    box-sizing: border-box;
}

.el-form-item__label[for="articleTitle"]::before {
    content: "*";
    color: #f56c6c;
    margin-right: 4px;
}

:deep(.el-form-item__content) {
    align-items: center;
    display: flex;
    flex: 1;
    flex-wrap: nowrap;
    font-size: 14px;
    line-height: 32px;
    min-width: 0;
    position: relative;
}

.el-image {
    border-radius: 2px;
    width: 40px;
    height: 40px;
    position: relative;
    display: inline-block;
    overflow: hidden;
}

.upload-button {
    text-align: center;
    cursor: pointer;
    margin: 4px 0 0 10px;
    width: 50px;
    height: 30px;
    line-height: 30px;
    color: #fff;
    border-radius: 4px;
    background: #837bc7;
}

.my-center {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>