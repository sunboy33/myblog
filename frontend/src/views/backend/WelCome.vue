<script>
import Header from '@/components/backend/Header.vue'
import SideBar from '@/components/backend/SideBar.vue'

export default 
{
    components: { Header, SideBar }
}
</script>


<template>
    <div>
        <Header></Header>
        <SideBar></SideBar>
        <div style="display: flex;align-items: center;justify-content: center;">
            <h1>欢迎来到后台管理系统</h1>
        </div>
    </div>
</template>