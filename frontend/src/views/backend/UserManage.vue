<script setup>
import { ref, onMounted } from 'vue'
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import { getUserList, deleteUser as deleteUserApi, updateUserStatus } from '@/api/index.js'
import { showError, showSuccess } from '@/utils/message.js'

const item1Value = ref('')
const item1Options = ref([{ value: 'head', label: '站长' }, { value: 'general', label: '普通用户' }])
const item2Value = ref('')
const item2Options = ref([{ value: 'active', label: '启用' }, { value: 'inactive', label: '禁用' }])
const keyword = ref('')
const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(5)
const count = ref(0)

async function handleDelete(id) {
    try {
        const response = await deleteUserApi(id)
        showSuccess(response.data.message)
        fetchUserList(currentPage.value)
    } catch (error) {
        showError(error.response?.data?.message || '删除失败')
    }
}

function clear() {
    item1Value.value = ''
    item2Value.value = ''
    keyword.value = ''
}

async function search() {
    try {
        const response = await getUserList({
            pageSize: pageSize.value,
            currentPage: 1,
            userType: item1Value.value,
            userStatus: item2Value.value,
            keyword: keyword.value
        })
        tableData.value = response.data.users
        count.value = response.data.count
    } catch (error) {
        showError(error.response?.data?.message || '搜索失败')
    }
}

function format(row, column, cellValue) {
    return cellValue || '-'
}

async function fetchUserList(page) {
    try {
        const response = await getUserList({
            pageSize: pageSize.value,
            currentPage: page
        })
        tableData.value = response.data.users
        count.value = response.data.count
    } catch (error) {
        showError(error.response?.data?.message || '获取用户列表失败')
    }
}

function currentChange(page) {
    currentPage.value = page
    fetchUserList(page)
}

async function handleStatusChange(row) {
    try {
        await updateUserStatus({
            userId: row.userId,
            status: row.status
        })
        let message = ''
        if (row.status === 'inactive') {
            message = `账号"${row.userName}"已被封禁!`
        } else {
            message = `账号"${row.userName}"已启用!`
        }
        showSuccess(message)
    } catch (error) {
        showError('用户状态更新失败!')
    }
}

onMounted(() => {
    fetchUserList(1)
})
</script>

<template>
    <Header></Header>
    <SideBar></SideBar>
    <div class="content-box">
        <div class="admin-content">
            <div class="handle-box">
                <div class="item" style="width: 130px;">
                    <el-select v-model="item1Value" placeholder="用户类型" size="large">
                        <el-option v-for="item in item1Options" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="item" style="width: 130px;">
                    <el-select v-model="item2Value" placeholder="用户状态" size="large">
                        <el-option v-for="item in item2Options" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="item" style="width: 170px;">
                    <el-input v-model="keyword" placeholder="用户名/手机号/邮箱" size="large" />
                </div>
                <div class="item">
                    <el-button type="primary" size="large" icon="Search" @click="search" style="font-weight: bold;">
                        搜索
                    </el-button>
                </div>
                <div class="item">
                    <el-button type="danger" size="large" style="font-weight: bold;" @click="clear">
                        清除参数
                    </el-button>
                </div>

            </div>
            <div>
                <el-table :data="tableData" style="width: 100%; border-radius: 5px;" border>
                    <el-table-column prop="s_id" label="ID" align="center" />
                    <el-table-column prop="userName" label="用户名" align="center" />
                    <el-table-column prop="phone" label="手机号" align="center" :formatter="format" />
                    <el-table-column prop="email" label="邮箱" align="center" :formatter="format" />
                    <el-table-column prop="status" label="状态" align="center">
                        <template #default="scope">
                            <div style="display: flex; align-items: center;">
                                <el-switch v-model="scope.row.status" :active-value="'active'"
                                    :inactive-value="'inactive'" style="margin-right: 8px" active-color="#13ce66"
                                    inactive-color="#ff4949" @change="handleStatusChange(scope.row)" />
                                <el-tag v-if="scope.row.status === 'active'" size="large" type="success">
                                    启用
                                </el-tag>
                                <el-tag v-else size="large" type="danger">
                                    禁用
                                </el-tag>
                            </div>
                        </template>

                    </el-table-column>
                    <el-table-column prop="userSex" label="性别" align="center">
                        <template #default="scope">
                            <el-tag v-if="scope.row.userSex === 'boy'" size="large" type="success">
                                男
                            </el-tag>
                            <el-tag v-else-if="scope.row.userSex === 'girl'" size="large" type="success">
                                女
                            </el-tag>
                            <el-tag v-else size="large" type="success">
                                保密
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="avatar" label="头像" align="center">
                        <template #default="scope">
                            <el-avatar :src="scope.row.avatar"></el-avatar>
                        </template>
                    </el-table-column>
                    <el-table-column prop="introduce" label="简介" align="center" />
                    <el-table-column prop="userType" label="用户类型" align="center">
                        <template #default="scope">
                            <el-tag v-if="scope.row.userType === 'head'" size="large" type="success">
                                站长
                            </el-tag>
                            <el-tag v-else size="large" type="success">
                                普通用户
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="register" label="注册时间" align="center" />
                    <el-table-column prop="operation" label="操作" align="center">
                        <template #default="scope">
                            <el-button size="small" type="danger" @click="handleDelete(scope.row.userId)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="myCenter" style="margin-top: 2%; color: #a8abb2;">
                <span style="margin-right: 10px;">共 {{ count }} 条</span>
                <el-pagination :background="true" :layout="'prev, pager, next'" :page-size="pageSize" :total="count"
                    :pager-count="5" @current-change="currentChange" @prev-click="() => { }" @next-click="() => { }" />
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

.item {
    margin-right: 10px;
    margin-bottom: 10px;
    display: inline-block;
    position: relative;
}

.handle-box {
    margin-bottom: 20px;

}
</style>
