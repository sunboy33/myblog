import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth.js";
const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/frontend/Home.vue"),
  },
  {
    path: "/adminPanel",
    component: () => import("@/views/backend/WelCome.vue"),
  },
  {
    path: "/login",
    component: () => import("@/views/frontend/Login.vue"),
  },
  {
    path: "/WebSiteSettings",
    component: () => import("@/views/backend/WebSiteSettings.vue"),
  },
  {
    path: "/UserManage",
    component: () => import("@/views/backend/UserManage.vue"),
  },
  {
    path: "/ClassManage",
    component: () => import("@/views/backend/ClassManage.vue"),
  },
  {
    path: "/LabelManage",
    component: () => import("@/views/backend/LabelManage.vue"),
  },
  {
    path: "/ArticleManage",
    component: () => import("@/views/backend/ArticleManage.vue"),
  },
  {
    path: "/AddArticle",
    component: () => import("@/views/backend/AddArticle.vue"),
  },
  {
    path: "/Article/:id",
    name: "article",
    component: () => import("@/views/frontend/Article.vue"),
  },
  {
    path: "/Article/type/:type_id",
    name: "ArticleOfType",
    component: () => import("@/views/frontend/ArticleOfType.vue"),
  },
  {
    path: "/Article/type/:type_id/:label_id",
    name: "ArticleOfTypeWithLabel",
    component: () => import("@/views/frontend/ArticleOfType.vue"),
  },
  {
    path: "/userCenter",
    name: "usercenter",
    component: () => import("@/views/frontend/UserCenter.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  /** 路由跳转时滚动调自动回到顶部 */
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },
});

/** 路由守卫 */
router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();

  // 初始化认证状态
  authStore.initialize();

  return;
});

export default router;
