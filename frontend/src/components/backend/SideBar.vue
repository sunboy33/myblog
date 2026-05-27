<script>
import { Menu } from '@element-plus/icons-vue';

export default {
    data() {
        return {
            menuItems: [
                { name: "网站设置", icon: "Tools", path: '/WebSiteSettings' },
                { name: "简历管理", icon: "Document", path: '/ResumeManage' },
                { name: "用户管理", icon: "UserFilled", path: '/UserManage' },
                { name: "分类管理", icon: "Memo", path: '/ClassManage' },
                { name: "标签管理", icon: "PriceTag", path: '/LabelManage' },
                { name: "文章管理", icon: "Document", path: '/ArticleManage' },
            ],
            activeIndex: -1,
            collapsed: false
        }
    },
    created() {
        this.setActiveByPath(this.$route.path);
    },
    methods: {
        setActive(index) {
            this.activeIndex = index;
            this.$router.push(this.menuItems[index].path);
        },
        setActiveByPath(path) {
            const index = this.menuItems.findIndex(item => item.path === path);
            if (index !== -1) {
                this.activeIndex = index;
            }
        },
        toggleCollapse() {
            this.collapsed = !this.collapsed;
        }
    },
    watch: {
        '$route.path'(newPath) {
            this.setActiveByPath(newPath);
        }
    }
}
</script>

<template>
    <div class="side-bar" :class="{ collapsed: collapsed }">
        <!-- 折叠按钮 -->
        <div class="collapse-btn" @click="toggleCollapse">
            <el-icon class="collapse-icon" :class="{ rotated: collapsed }">
                <Menu />
            </el-icon>
            <span v-if="!collapsed" class="collapse-text">折叠</span>
        </div>

        <!-- 菜单项 -->
        <ul class="sidebar-menu">
            <li v-for="(item, index) in menuItems" 
                :key="index" 
                class="menu-item"
                :class="{ 
                    'is-active': activeIndex === index,
                    'collapsed': collapsed
                }" 
                @click="setActive(index)">
                <div class="menu-item-content">
                    <el-icon class="menu-icon">
                        <component :is="item.icon" />
                    </el-icon>
                    <span class="menu-text" v-show="!collapsed">{{ item.name }}</span>
                    
                </div>
                
                <!-- 激活状态背景 -->
                <div v-if="activeIndex === index" class="active-background"></div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.side-bar {
    position: fixed;
    left: 0;
    top: 70px;
    bottom: 0;
    width: 150px;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    border-right: 1px solid #e1e5eb;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05);
    z-index: 1000;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow-x: hidden;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.side-bar.collapsed {
    width: 70px;
}

.side-bar::-webkit-scrollbar {
    width: 4px;
}

.side-bar::-webkit-scrollbar-track {
    background: transparent;
}

.side-bar::-webkit-scrollbar-thumb {
    background: #c1c9d2;
    border-radius: 4px;
}

.side-bar::-webkit-scrollbar-thumb:hover {
    background: #a8b2c1;
}

/* 折叠按钮 */
.collapse-btn {
    display: flex;
    align-items: center;
    padding: 20px 16px;
    color: #5a6270;
    cursor: pointer;
    user-select: none;
    transition: all 0.3s ease;
    border-bottom: 1px solid #e1e5eb;
    background: linear-gradient(to right, #ffffff, #f8fafc);
    margin: 8px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.collapse-btn:hover {
    background: linear-gradient(to right, #f8fafc, #f1f5f9);
    color: #409eff;
    transform: translateX(2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.collapse-icon {
    font-size: 20px;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-right: 12px;
}

.collapse-icon.rotated {
    transform: rotate(180deg);
}

.collapse-text {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    letter-spacing: 0.5px;
}

/* 菜单容器 */
.sidebar-menu {
    list-style: none;
    padding: 12px;
    margin: 0;
    flex: 1;
}

/* 菜单项 */
.menu-item {
    position: relative;
    margin: 4px 0;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-item.collapsed {
    margin: 4px auto;
    width: 44px;
}

.menu-item:hover:not(.is-active) {
    background: rgba(64, 158, 255, 0.08);
    transform: translateX(2px);
}

.menu-item.is-active {
    background: linear-gradient(135deg, #409eff 0%, #2979ff 100%);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
    transform: translateX(2px);
}

.menu-item-content {
    display: flex;
    align-items: center;
    padding: 16px 20px;
    position: relative;
    z-index: 2;
    transition: all 0.3s ease;
}

.menu-item.collapsed .menu-item-content {
    padding: 16px;
    justify-content: center;
}

.menu-icon {
    font-size: 20px;
    margin-right: 12px;
    color: #64748b;
    transition: all 0.3s ease;
    min-width: 20px;
}

.menu-item.is-active .menu-icon {
    color: white;
    transform: scale(1.1);
}

.menu-item:hover:not(.is-active) .menu-icon {
    color: #409eff;
    transform: scale(1.05);
}

.menu-text {
    font-size: 14px;
    font-weight: 500;
    color: #334155;
    white-space: nowrap;
    letter-spacing: 0.3px;
    transition: all 0.3s ease;
    opacity: 1;
    transform: translateX(0);
}

.side-bar.collapsed .menu-text {
    opacity: 0;
    transform: translateX(-10px);
    width: 0;
    position: absolute;
}

.menu-item.is-active .menu-text {
    color: white;
    font-weight: 600;
}

.menu-item.collapsed .active-indicator {
    display: none;
}

/* 激活状态背景 */
.active-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(64, 158, 255, 0.1) 0%, rgba(41, 121, 255, 0.1) 100%);
    border-radius: 12px;
    z-index: 1;
    animation: shimmer 3s infinite;
}

/* 动画 */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 0.9;
    }
    50% {
        transform: scale(1.2);
        opacity: 1;
    }
}

@keyframes shimmer {
    0%, 100% {
        background-position: -200% center;
    }
    100% {
        background-position: 200% center;
    }
}

/* 响应式调整 */
@media (max-height: 600px) {
    .menu-item-content {
        padding: 12px 20px;
    }
    
    .menu-item.collapsed .menu-item-content {
        padding: 12px;
    }
}

/* 加载动画 */
.menu-item {
    animation: fadeInUp 0.4s ease-out;
    animation-fill-mode: both;
}


</style>