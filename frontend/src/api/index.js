import httptool from "@/utils/api.js";
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

/** 登录 v1 */
export const login = (data) => axios.post(`${BASE_URL}/api/user/login`, data)

/** 注册 v1 */
export const register = (data) => axios.post(`${BASE_URL}/api/user/register`, data)

/** 获取验证码 v1 */
export const sendVerificationCode = (data) => axios.post(`${BASE_URL}/api/authority/code`, data)

/** 获取网站信息 v1 */
export const getWebSettings = () => axios.get(`${BASE_URL}/api/media/webSettings`)

/** 更新网站设置信息 v1 */
export const updateWebSettings = (data) => httptool.put("/api/media/webSettings", data)

/** 获取主页文章 v1 */
export const getHomeArticles = () => axios.get(`${BASE_URL}/api/article/listSortAticle`)

/** 获取主页推荐文章 v1 */
export const getRecommendedArticles = () => axios.get(`${BASE_URL}/api/article/listRecommend`)

/** 分页获取文章，含关键字  v1 */
export const getArticleList = (params) => axios.get(`${BASE_URL}/api/article/pagination`, { params })

/** 获取某一类别的所有文章 v1 */
export const getArticlesByType = (params) => axios.get(`${BASE_URL}/api/article/type`, { params })

/** 根据id获取文章信息 v1 */
export const getArticleById = (id) => axios.get(`${BASE_URL}/api/article/${id}`)

/** 获取某篇文章的评论 v1 */
export const getComments = (params) => axios.get(`${BASE_URL}/api/comment/`, { params })
 
/** 添加评论 v1 */
export const addComment = (articleId, data) => httptool.post(`/api/comment/${articleId}`, data)

/** 获取所有用户 v1 */
export const getUserList = (params) => httptool.get("/api/user/", { params })

/** 修改用户状态（启用或禁用）v1 */
export const updateUserStatus = (data) => httptool.put("/api/user/updateUserStatuts", data)

/** 删除用户 v1 */
export const deleteUser = (id) => httptool.delete(`/api/user/${id}`)

/** 更新用户信息 v1 */
export const updateUser = (id, data) => httptool.put(`/api/user/${id}`, data)

/** 获取类别信息 v1 */
export const getSortOperation = () => axios.get(`${BASE_URL}/api/sort/operation`)

/** 新增分类 v1 */
export const addSort = (data) => httptool.post("/api/sort/operation", data)

/** 删除类别  v1 */
export const deleteSort = (id) => httptool.delete(`/api/sort/${id}`)

/** 修改类别 v1 */
export const updateSort = (data) => httptool.put("/api/sort/operation", data)

/** 获取标签信息 v1 */
export const getLabels = () => httptool.get(`${BASE_URL}/api/sort/label`)

/** 添加标签 v1 */
export const addLabel = (data) => httptool.post("/api/sort/label", data)

/** 更新文章 v1 */
export const updateArticle = (id, data) => httptool.put(`/api/article/update/${id}`, data)

/** 添加文章 v1 */
export const addArticle = (data) => httptool.post("/api/article/add", data)

/** 删除文章 v1 */
export const deleteArticle = (id) => httptool.delete(`/api/article/delete/${id}`)

/** 刷新token v1 */
export const refreshToken = (refreshToken) => axios.post(`${BASE_URL}/api/authority/refreshToken`, { refresh: refreshToken })

/** 定时判断用户登录是否过期 */
export const verify = () => httptool.get(`${BASE_URL}/api/authority/verify`)

/** 上传资源 v1 */
export const uploadMedia = (formData) => httptool.post("/api/media/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  })

/** 删除资源 v1 */
export const deleteMedia = (fileUrl) => httptool.delete("/api/media/", { data: { fileUrl } })


