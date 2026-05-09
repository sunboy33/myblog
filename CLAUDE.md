# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 项目概述

个人博客，前端使用 Vue 3，后端使用 Django REST API。功能包括文章发布（分类/标签）、评论、用户认证和网站流量统计。

## 技术栈

- **前端**: Vue 3 + Vite, Element Plus, Pinia, Vue Router, Markdown 渲染 (md-editor-v3, marked, highlight.js)
- **后端**: Django + Django REST Framework, SimpleJWT, MySQL, Redis
- **存储**: 七牛云用于媒体文件存储
- **邮件**: 通过 nodemailer 使用 SMTP

## 后端架构

Django 项目位于 `backend/backend/`，包含以下应用：
- `article` — 文章内容和增删改查
- `categorie` — 文章分类和标签
- `comment` — 文章评论
- `media` — 文件上传和访问量追踪
- `authority` — 管理员权限
- `user` — 自定义用户模型（以 `userName` 作为 `USERNAME_FIELD`）

### API 路由（均以 `/api/` 为前缀）
| 前缀 | 应用 | 用途 |
|--------|-----|---------|
| `/api/article/` | article | 文章 |
| `/api/sort/` | categorie | 分类/标签 |
| `/api/media/` | media | 文件上传、访问量 |
| `/api/comment/` | comment | 评论 |
| `/api/authority/` | authority | 管理操作 |
| `/api/user/` | user | 认证、用户信息 |

### 后端关键模式
- Redis 客户端是 `backend/backend/redis_client.py` 中的模块级单例
- 自定义 User 模型以 `userId` 为主键；JWT 使用 `USER_ID_FIELD = "userId"`
- `ACCESS_TOKEN_LIFETIME` = 1 天，`REFRESH_TOKEN_LIFETIME` = 7 天
- 数据库配置、密钥、邮件、七牛云和 Redis 设置从 `config.ini` 读取（不提交到 git）

## 前端架构

Vue 3 单页应用，视图分为 `frontend`（前台）和 `backend`（后台管理面板）。

### Store（Pinia）
- `stores/auth.js` — JWT 令牌和用户状态
- `stores/web.js` — 全站网页状态

### 关键视图
- `/` — 首页，按分类展示文章列表
- `/Article/:id` — 文章详情
- `/Article/type/:type_id` — 按分类查看文章
- `/adminPanel` — 管理后台欢迎页
- `/ArticleManage`, `/AddArticle`, `/ClassManage`, `/LabelManage`, `/UserManage`, `/WebSiteSettings` — 后台增删改查

## 命令

```bash
# 后端
cd backend
python manage.py runserver          # 启动开发服务器
python manage.py migrate           # 执行数据库迁移
python manage.py createsuperuser    # 创建超级管理员用户

# 前端
cd frontend
npm install                         # 安装依赖
npm run dev                        # 启动 Vite 开发服务器
npm run build                      # 生产环境构建
npm run preview                    # 预览生产构建
```

## 配置

`backend/config.ini` 包含所有密钥和外部服务凭据（数据库、Redis、七牛云、SMTP）。此文件不提交到 git 仓库。
