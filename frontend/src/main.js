import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router.js'
import '@/assets/css/font-awesome.min.css'
import '@/assets/css/index.css'
import ElemetPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'
import { ElImageViewer } from 'element-plus'



const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(ElemetPlus);
app.use(pinia);
app.component('el-image-viewer', ElImageViewer);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}


app.mount('#app');









