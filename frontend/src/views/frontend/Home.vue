<script>
import Header from '@/components/frontend/Header.vue';
import TopView from '@/components/frontend/TopView.vue'
import SideBar from '@/components/frontend/SideBar.vue'
import Content from '@/components/frontend/Content.vue'
import Footer from '@/components/frontend/Footer.vue'
import BackToTop from '@/components/frontend/BackToTop.vue'

export default
    {
        components: { Header, TopView, SideBar, Content, Footer, BackToTop }
    }
</script>

<template>
    <div class="main-container">
        <Header></Header>
        <TopView></TopView>
        <div class="content-container">
            <Content></Content>
            <Footer></Footer>
        </div>
        <BackToTop></BackToTop>
    </div>
</template>

<style scoped>
.main-container {
    display: flex;
    flex-direction: column;

}

.content-container {
    background: #fff;
    position: relative;
}

.page-container {
    display: flex;
    justify-content: center;
    width: 90%;
    max-width: 1400px;
    padding: 0 10px 40px 10px;
    margin: 0 auto;
    flex-direction: row;
}
</style>