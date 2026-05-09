<script>

const webInfo = JSON.parse(localStorage.getItem('webInfo') || '{}')

export default {
    data() {
        return {
        }
    },
    computed:{
        icpNumber(){
            return webInfo.icpNumber
        },
        contactEmail(){
            return webInfo.contactEmail
        }
    }
}


</script>

<template>
    <div class="myFooter-wrap">
        <div class="myFooter">
            <div class="footer-title">相信记录的力量！</div>
            <div class="icp">
                本网站由 CODEJOURNEY 强力支持
                <a href="https://beian.miit.gov.cn/" target="_blank">{{ icpNumber }}</a>
            </div>
            <div style="font-size: 14px; line-height: 30px;">
                <div> 本网站部分内容来源于网络，仅供大家学习与参考。 </div>
                <div> 本网站一切内容不代表本站立场，并不代表本站赞同其观点和对其真实性负责。 </div>
                <div> 如无意中侵犯了某个企业或个人的知识产权，请及时通过电子邮件({{ contactEmail }})告知我们，本网站将立即给予删除。 </div>
            </div>
        </div>
    </div>
</template>


<style scoped>
.myFooter-wrap {
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    animation: hideToShow 2s;
}


.myFooter {
    background-image: url('https://niu.codejourney.cn/static/homebackground/sunboy1777903069096.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    text-align: center;
    color: #fff;
    padding: 20px 15px 15px;
    position: relative;
    overflow: hidden;
    z-index: 0;

}

.icp {
    padding-top: 10px;
    padding-bottom: 10px;
}

a:-webkit-any-link {
    color: -webkit-link;
    cursor: pointer;
    text-decoration: underline;
}


.icp,
.icp a {
    color: #f4e1c0;
    font-size: 13px;
    text-decoration: none;
    transition: all .3s;
}

.icp a:hover {
    color: orange;
}

.footer-title {
    font-size: 16px;
}



@keyframes hideToShow {
    0% {
        opacity: 0
    }

    100% {
        opacity: 1
    }
}
</style>