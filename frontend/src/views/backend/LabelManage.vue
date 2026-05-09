<script>
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'
import httptool from '@/utils/api.js'
import { getLabels } from '@/api/index.js'
import { showError } from '@/utils/message.js'

export default {
    components: { Header, SideBar },
    data() {
        return {
            tableData: [],
        }
    },
    async mounted() {
        await getLabels().then(response => {
                this.tableData = response.data.labels
            })
            .catch(error => {
                showError(error.message)
            })
    }
}
</script>


<template>
    <Header></Header>
    <SideBar></SideBar>
    <div class="content-box">
        <div class="admin-content">
            <div class="handle-box">
                <div class="item" style="width: 130px;">
                </div>
            </div>
            <div>
                <el-table :data="tableData" style="width: 100%; border-radius: 5px;" :border="true">
                    <el-table-column prop="s_id" label="ID" :align="'center'" />
                    <el-table-column prop="label" label="标签名称" :align="'center'" />
                    <!-- <el-table-column prop="desc" label="标签描述" :align="'center'" /> -->
                    <el-table-column prop="type_name" label="所属分类" :align="'center'" />
                    <el-table-column prop="articleCount" label="文章数量" :align="'center'" />
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
</style>