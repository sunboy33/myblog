<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import { getArticleList, deleteArticle } from '@/api/index.js'
import { showError, showSuccess } from '@/utils/message.js'
import {ElMessageBox} from 'element-plus'

const router = useRouter()

const isRecommendOptions = [
    { value: 1, label: '是' },
    { value: 0, label: '否' }
]
const isRecommendValue = ref('')

const ArticleLimitOptions = [
    { value: '公开', label: '公开' },
    { value: '登录', label: '登录' }
]
const ArticleLimitValue = ref('')

const ArticleTypeOptions = ref([])
const ArticleTypeValue = ref('')

const ArticleLabelOptions = ref([])
const ArticleLabelValue = ref('')

const articleTitleInput = ref('')

const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(5)
const count = ref(0)


const search = async () => {
        await fetchArticleList(1)

}

const formatTime = (row, column, cellValue) => {
    return cellValue ? cellValue : '--'
}

const clearParams = () => {
    isRecommendValue.value = ''
    ArticleLimitValue.value = ''
    ArticleTypeValue.value = ''
    ArticleLabelValue.value = ''
    articleTitleInput.value = ''
}

const addArticle = () => {
    router.push('/AddArticle')
}

const fetchArticleList = async (page) => {
    try {
        const params = {
            pageSize: pageSize.value,
            currentPage: page,
            is_recommend: isRecommendValue.value,
            limit: ArticleLimitValue.value,
            sort: ArticleTypeValue.value,
            label: ArticleLabelValue.value,
            title: articleTitleInput.value
        }
        const response = await getArticleList(params)
        tableData.value = response.data.articles
        count.value = response.data.count

        const types = []
        const labels = []
        for (const item of tableData.value) {
            if (!types.includes(item.type)) {
                types.push(item.type)
                if (!ArticleTypeOptions.value.some(opt => opt.value === item.type)) {
                    ArticleTypeOptions.value.push({ value: item.type, label: item.type })
                }
            }
            for (const label of item.label) {
                if (!labels.includes(label)) {
                    labels.push(label)
                    if (!ArticleLabelOptions.value.some(opt => opt.value === label)) {
                        ArticleLabelOptions.value.push({ value: label, label: label })
                    }
                }
            }
        }
        currentPage.value = page
    } catch (error) {
        showError(error.response?.data?.message)
    }
}

const handleEdit = (row) => {
    router.push({
        path: '/AddArticle',
        query: {
            articleId: row.id
        }
    })
}

const confirmDelete = async (id) => {
    try {
        await deleteArticle(id)
        showSuccess('删除成功!')
        fetchArticleList(currentPage.value)
    } catch (error) {
        showError(error.response?.data?.message)
    }
}

const handleDelete = (id) => {
    ElMessageBox.confirm(
        '确定删除此文章?该操作不可撤销!',
        'warning',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning'
        }
    ).then(() => {
        confirmDelete(id)
    }).catch(() => { })
}

const currentChange = (page) => {
    fetchArticleList(page)
}

onMounted(() => {
    fetchArticleList(1)
})
</script>

<template>
    <Header></Header>
    <SideBar></SideBar>
    <div class="content-box">
        <div class="admin-content">
            <div class="handle-box">
                <div class="item" style="width: 130px;">
                    <el-select v-model="isRecommendValue" placeholder="是否推荐" size="large">
                        <el-option v-for="item in isRecommendOptions" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="item" style="width: 130px;">
                    <el-select v-model="ArticleLimitValue" placeholder="文章权限" size="large">
                        <el-option v-for="item in ArticleLimitOptions" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="item" style="width: 130px;">
                    <el-select v-model="ArticleTypeValue" placeholder="请选择分类" size="large">
                        <el-option v-for="item in ArticleTypeOptions" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="item" style="width: 130px;">
                    <el-select v-model="ArticleLabelValue" placeholder="请选择标签" size="large">
                        <el-option v-for="item in ArticleLabelOptions" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="item" style="width: 170px;">
                    <el-input v-model="articleTitleInput" placeholder="文章标题" size="large" />
                </div>
                <div class="item">
                    <el-button type="primary" size="large" icon="Search" @click="search" style="font-weight: bold;">
                        搜索
                    </el-button>
                </div>
                <div class="item">
                    <el-button type="danger" size="large" style="font-weight: bold;" @click="clearParams">
                        清除参数
                    </el-button>
                </div>
                <div class="item">
                    <el-button type="primary" size="large" style="font-weight: bold;" @click="addArticle">
                        新增文章
                    </el-button>
                </div>
            </div>
            <div>
                <el-table :data="tableData" style="width: 100%;border-radius: 5px;" :fit="true" :border="true">
                    <el-table-column prop="s_id" label="ID" :align="'center'" width="50px" />
                    <el-table-column prop="author" label="作者" :align="'center'" />
                    <el-table-column prop="title" label="文章标题" :align="'center'" />
                    <el-table-column prop="type" label="文章类型" :align="'center'" />
                    <el-table-column prop="label" label="标签" :align="'center'" />
                    <el-table-column prop="limit" label="文章权限" :align="'center'">
                        <template #default="scope">
                            <el-tag size="large" type="success">{{ scope.row.limit }}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="cover" label="封面" :align="'center'">
                        <template #default="scope">
                            <el-image :src="scope.row.cover" fit="cover" style="width: 50px;height: 50px;"></el-image>
                        </template>
                    </el-table-column>
                    <el-table-column prop="show" label="是否展示" :align="'center'">
                        <template #default="scope">
                            <el-tag v-if="scope.row.show === true" type="success" size="large">是</el-tag>
                            <el-tag v-else type="danger" size="large">否</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="comment" label="能否评论" :align="'center'">
                        <template #default="scope">
                            <el-tag v-if="scope.row.comment === true" type="success" size="large">是</el-tag>
                            <el-tag v-else type="danger" size="large">否</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="recommend" label="是否推荐" :align="'center'">
                        <template #default="scope">
                            <el-tag v-if="scope.row.recommend === true" type="success" size="large">是</el-tag>
                            <el-tag v-else type="danger" size="large">否</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="pageviews" label="浏览量" :align="'center'" />
                    <el-table-column prop="comments" label="评论数" :align="'center'" />
                    <el-table-column prop="createtime" label="创建时间" :align="'center'" />
                    <el-table-column prop="finalltime" label="最终修改时间" :formatter="formatTime" :align="'center'" />
                    <el-table-column prop="operation" label="操作" :align="'center'">
                        <template #default="scope">
                            <div>
                                <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                                <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="myCenter" style="margin-top: 2%; color: #a8abb2;">
                <span style="margin-right: 10px;">共 {{ count }} 条</span>
                <el-pagination :current-page="currentPage" :background="true" :layout="'prev, pager, next'"
                    :page-size="pageSize" :total="count" :pager-count="5" @current-change="currentChange"
                    @prev-click="() => { }" @next-click="() => { }" />
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

.handle-box {
    margin-bottom: 20px;
}

.item {
    margin-right: 10px;
    margin-bottom: 10px;
    display: inline-block;
    position: relative;
}

:deep(.el-button+.el-button) {
    margin-left: 0;
    margin-top: 5px;
}
</style>