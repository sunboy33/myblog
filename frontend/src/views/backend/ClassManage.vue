<script setup>
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import { ElMessageBox } from 'element-plus'
import { ref, reactive, onMounted } from 'vue'
import { getSortOperation, addSort, updateSort, deleteSort } from '@/api/index.js'
import { showError, showSuccess } from '@/utils/message.js'

const addDialogVisible = ref(false)
const tableData = ref([])
const typeMessage = reactive({ type: '', desc: '', priority: '' })
const isEditMode = ref(false)
const editId = ref(0)

async function fetchTypeList() {
    try {
        const response = await getSortOperation()
        tableData.value = response.data.types
    } catch (error) {
        showError(error.message)
    }
}

function format(row, column, cellValue) {
    return cellValue || '-'
}

async function handleAddConfirm() {
    if (typeMessage.type === '' || typeMessage.desc === '' || typeMessage.priority === '') {
        showError('请先填写完整的分类信息!')
        return
    }
    try {
        await addSort(typeMessage)
        showSuccess('添加成功!')
        fetchTypeList()
        resetForm()
        addDialogVisible.value = false
    } catch (error) {
        showError(error.response?.data?.message)
    }
}

function resetForm() {
    typeMessage.type = ''
    typeMessage.desc = ''
    typeMessage.priority = ''
}

function cancel() {
    resetForm()
    addDialogVisible.value = false
    isEditMode.value = false
}

function handleEdit(row) {
    editId.value = row.id
    isEditMode.value = true
    addDialogVisible.value = true
    typeMessage.type = row.type
    typeMessage.desc = row.desc
    typeMessage.priority = row.priority
}

async function handleEditConfirm() {
    const data = {
        id: editId.value,
        type: typeMessage.type,
        desc: typeMessage.desc,
        priority: typeMessage.priority
    }
    try {
        await updateSort(data)
        showSuccess('修改成功!')
        fetchTypeList()
        resetForm()
        addDialogVisible.value = false
        isEditMode.value = false
    } catch (error) {
        showError(error.response?.data?.message)
    }
}

function handleDelete(id) {
    ElMessageBox.confirm(
        '确定删除该类别?该操作不可撤销!',
        'warning',
        {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
        }
    ).then(() => {
        confirmDelete(id)
    }).catch(() => { })
}

async function confirmDelete(id) {
    try {
        await deleteSort(id)
        showSuccess('删除成功!')
        fetchTypeList()
    } catch (error) {
        showError(error.response?.data?.message)
    }
}

onMounted(() => {
    fetchTypeList()
})
</script>

<template>
    <Header></Header>
    <SideBar></SideBar>
    <div class="content-box">
        <div class="admin-content">
            <div class="handle-box">
                <div class="item" style="width: 130px;">
                    <el-button type="primary" size="large" @click="addDialogVisible = true">新增分类</el-button>
                    <el-dialog v-model="addDialogVisible" :center="true" title="分类" width="500" class="dialog"
                        :before-close="cancel">
                        <div>
                            <el-input v-model="typeMessage.type" style="max-width: 400px" size="large"
                                placeholder="请输入分类名称">
                                <template #prepend>分类名称</template>
                            </el-input>
                        </div>
                        <div>
                            <el-input v-model="typeMessage.desc" style="max-width: 400px" size="large"
                                placeholder="请输入分类描述">
                                <template #prepend>分类描述</template>
                            </el-input>
                        </div>
                        <div>
                            <el-input v-model="typeMessage.priority" style="max-width: 400px" size="large"
                                placeholder="请输入分类优先级">
                                <template #prepend>分类优先级</template>
                            </el-input>
                        </div>
                        <div style="display: flex;align-items: center;justify-content: center;margin-top: 50px;">
                            <el-button size="large" @click="cancel">取消</el-button>
                            <el-button size="large" type="primary"
                                @click="isEditMode ? handleEditConfirm() : handleAddConfirm()">确定</el-button>
                        </div>
                    </el-dialog>
                </div>
            </div>
            <div>
                <el-table :data="tableData" style="width: 100%; border-radius: 5px;" :border="true">
                    <el-table-column prop="s_id" label="ID" :align="'center'" />
                    <el-table-column prop="type" label="分类名称" :align="'center'" />
                    <el-table-column prop="desc" label="分类描述" :align="'center'" :formatter="format" />
                    <el-table-column prop="priority" label="优先级" :align="'center'" />
                    <el-table-column prop="article_count" label="文章数量" :align="'center'" />
                    <el-table-column prop="operation" label="操作" :align="'center'">
                        <template #default="scope">
                            <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                            <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
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


.dialog div {
    margin-left: 10px;
    margin-top: 10px;
}

:deep(.el-input-group__prepend) {
    width: 90px !important;
    text-align: center;
}
</style>