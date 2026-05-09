<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/frontend/Header.vue'
import Footer from '@/components/frontend/Footer.vue'
import BackToTop from '@/components/frontend/BackToTop.vue'
import httptool from '@/utils/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import { showError, showSuccess, showWarning } from '@/utils/message.js'
import { getComments, addComment, uploadMedia, getArticleById } from '@/api/index.js'
import hljs from 'highlight.js'

const route = useRoute()
const authStore = useAuthStore()
const articleData = ref({})
const content = ref('')
const comments = ref(null)
const dialogVisible = ref(false)
const replyText = ref('')
const fatherid = ref(-1)
const floorcommentid = ref(-1)
const commentNum = ref(0)
const showEmoji = ref(false)
const showEmojiReply = ref(false)
const showUploadImage = ref(false)
const fileList = ref([])
const uploadRef = ref(null)
const previewVisible = ref(false)
const previewImageUrl = ref('')

const webInfo = JSON.parse(localStorage.getItem('webInfo'))

const FILE_NUMS = 1
const MAX_COMMENT_LENGTH = 10000
const EMOJI_MAP = {
  '[666]': 'http://codejourney.cn/emoji/666.jpg',
  '[喜欢]': 'http://codejourney.cn/emoji/喜欢.jpg',
  '[愣住]': 'http://codejourney.cn/emoji/愣住.jpg',
  '[无语]': 'http://codejourney.cn/emoji/无语.jpg',
  '[杀马特]': 'http://codejourney.cn/emoji/杀马特.jpg',
  '[点赞]': 'http://codejourney.cn/emoji/点赞.jpg',
  '[狗头]': 'http://codejourney.cn/emoji/狗头.jpg'
}



// 渲染消息（支持表情和图片）
function renderMessage(text) {
  if (!text) return ''
  return text.replace(/\[(.*?)\]/g, (match) => {
    const emojiPath = EMOJI_MAP[match]
    if (emojiPath) {
      const emojiName = match.slice(1, -1)
      return `<img src="${emojiPath}" title="${emojiName}" loading="lazy" style="vertical-align: middle; width: 32px; height: 32px" class="emoji">`
    }
    const imageMatch = match.match(/\[([^,]+),\s*(https?:\/\/[^\s\]\)]+\.(?:jpg|jpeg|png|gif|webp)[^\s\]\)]*)\]/i)
    if (imageMatch) {
      const userName = imageMatch[1]
      const imageUrl = imageMatch[2]
      return `<img src="${imageUrl}" class="pictureReg" title="${userName}" loading="lazy" onclick="window.__openImagePreview && window.__openImagePreview('${imageUrl}')" style="cursor:pointer">`
    }
    return match
  })
}

// 表情操作
function selectEmoji(name) {
  content.value += name
  showEmoji.value = false
}

function selectEmojiReply(name) {
  replyText.value += name
  showEmojiReply.value = false
}

function toggleEmoji() {
  showEmoji.value = !showEmoji.value
}

function toggleEmojiReply() {
  showEmojiReply.value = !showEmojiReply.value
}

function openPreview(url) {
  previewImageUrl.value = url
  previewVisible.value = true
}

// 回复操作
function openReplyDialog(commentId, floorCommentId) {
  dialogVisible.value = true
  fatherid.value = commentId
  floorcommentid.value = floorCommentId
  replyText.value = ''
}

function handleClose() {
  dialogVisible.value = false
}

// 提交回复
async function submitReply() {
  if (!replyText.value?.trim()) {
    showError('评论内容不能为空')
    return
  }

  if (!authStore.hasLogin()) {
    showError('用户未登录')
    return
  }

  const params = {
    authorid: authStore.user.userId,
    content: replyText.value,
    fatherid: fatherid.value,
    floorcommentid: floorcommentid.value
  }

  try {
    await addComment(route.params.id, params)
    showSuccess('评论成功')
    replyText.value = ''
    dialogVisible.value = false
    await fetchComments()
  } catch (error) {
    const serverMsg = error.response?.data?.message
    showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
  }
}

// 提交评论
async function submitComment() {
  if (!content.value?.trim()) {
    showError('评论内容不能为空')
    return
  }

  if (!authStore.hasLogin()) {
    showError('用户未登录')
    return
  }

  const params = {
    authorid: authStore.user.userId,
    content: content.value,
    fatherid: -1,
    floorcommentid: -1
  }

  try {
    await addComment(route.params.id, params)
    showSuccess('评论成功')
    content.value = ''
    dialogVisible.value = false
    await fetchComments()
  } catch (error) {
    const serverMsg = error.response?.data?.message
    showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
  }
}

// 获取评论
async function fetchComments() {
  try {
    const response = await getComments({ articleId: route.params.id })
    comments.value = response.data.records
    commentNum.value = response.data.recordNum
  } catch (error) {
    const serverMsg = error.response?.data?.message
    showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
  }
}

// 上传图片
function openUploadDialog() {
  showUploadImage.value = true
}

function cancelUpload() {
  showUploadImage.value = false
}

async function customUpload(file) {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  const maxSize = 2 * 1024 * 1024 // 2MB

  if (!allowedTypes.includes(file.file.type)) {
    showError('仅支持 JPG、PNG 或 GIF 格式')
    return
  }
  if (file.file.size > maxSize) {
    showError('单个文件不能超过 2MB')
    return
  }

  const url = await uploadCommentImage(file)
  content.value = `${content.value}[${authStore.user.userName},${url}]`
  showUploadImage.value = false
}

async function uploadCommentImage(file) {
  const formData = new FormData()
  const filename = `${authStore.user.userName}${Date.now()}.jpg`
  formData.append('originName', file.file.name)
  formData.append('fileName', filename)
  formData.append('type', 'comment')
  formData.append('storeType', 'qiniu')
  formData.append('file', file.file)

  try {
    const response = await uploadMedia(formData)
    return response.data.data.url
  } catch (error) {
    const serverMsg = error.response?.data?.message
    showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
  }
}

function handleExceed() {
  showWarning(`最多只能上传 ${FILE_NUMS} 个文件`)
}

async function handleUploadSubmit() {
  uploadRef.value?.submit()
  fileList.value = []
  showUploadImage.value = false
}

// 获取文章详情
async function fetchArticle() {
  try {
    const response = await getArticleById(route.params.id)
    articleData.value = response.data.article
    articleData.value.label = articleData.value.label.join(' · ')
  } catch (error) {
    const serverMsg = error.response?.data?.message
    showError(serverMsg || '网络请求失败，请检查网络或稍后重试')
  }
}

// 生命周期
onMounted(async () => {
  window.__openImagePreview = openPreview
  await fetchArticle()
  await fetchComments()
})

onUnmounted(() => {
  window.__openImagePreview = null
})
</script>

<template>
  <div class="home-container">
    <Header />
    <div id="main-container">
      <div class="article-head my-animation-slide-top">
        <el-image :src="articleData.cover" class="article-image" fit="cover" />
        <div class="article-info-container">
          <h1 class="article-title">{{ articleData.title }}</h1>
          <div class="article-info">
            <span class="info-item">
              <i style="vertical-align: -2px;"><svg viewBox="0 0 1024 1024" width="14" height="14">
                  <path
                    d="M510.4 65.5l259.69999999 0 1e-8 266.89999999c0 147.50000001-116.2 266.89999999-259.7 266.90000001-143.4 0-259.7-119.5-259.7-266.90000001 0.1-147.5 116.3-266.9 259.7-266.89999999z"
                    fill="#FF9FCF"></path>
                  <path
                    d="M698.4 525.2l-13 0c53-48.4 86.5-117.8 86.5-195.20000001 0-10.2-0.7-20.3-1.8-30.19999999C613.8 377.50000001 438.6 444.9 266 437.7c15 33.4 36.7 63.1 63.5 87.5l-5.3 0c-122.6 0-225.5 88.1-248.8 204.1C340 677.2 597.7 609.2 862.2 585.7c-44.3-37.6-101.5-60.5-163.8-60.5z"
                    fill="#FF83BB"></path>
                  <path
                    d="M862.2 585.7C597.7 609.2 340 677.2 75.4 729.3c-3.2 16.1-5 32.6-5 49.6 0 99.8 81.7 181.5 181.5 181.5l518.6 0c99.8 0 181.5-81.7 181.5-181.5 0.1-77.2-35-146.5-89.8-193.2z"
                    fill="#FF5390"></path>
                  <path
                    d="M770.1 299.8C755.1 168 643.3 65.5 507.4 65.5c-146.1 0-264.5 118.4-264.5 264.5 0 38.4 8.3 74.8 23.1 107.7 172.6 7.2 347.8-60.2 504.1-137.9z"
                    fill="#FF9FCF"></path>
                  <path
                    d="M436.4 282.1c0 24.1-19.6 43.7-43.7 43.7S349 306.2 349 282.1s19.6-43.7 43.7-43.7c24.19999999 0 43.7 19.6 43.7 43.7z"
                    fill="#FFFFFF"></path>
                  <path d="M625 282.1m-43.7 0a43.7 43.7 0 1 0 87.4 0 43.7 43.7 0 1 0-87.4 0Z" fill="#FFFFFF"></path>
                </svg></i>
              {{ articleData.author }}
            </span>
            <span class="separator">·</span>
            <span class="info-item">
              <i style="vertical-align: -2px;"><svg viewBox="0 0 1024 1024" width="14" height="14">
                  <path
                    d="M768 213.333333h-42.666667V170.666667c0-25.6-17.066667-42.666667-42.666666-42.666667s-42.666667 17.066667-42.666667 42.666667v42.666666H384V170.666667c0-25.6-17.066667-42.666667-42.666667-42.666667s-42.666667 17.066667-42.666666 42.666667v42.666666H256C183.466667 213.333333 128 268.8 128 341.333333v426.666667c0 72.533333 55.466667 128 128 128h512c72.533333 0 128-55.466667 128-128V341.333333c0-72.533333-55.466667-128-128-128z m42.666667 554.666667c0 25.6-17.066667 42.666667-42.666667 42.666667H256c-25.6 0-42.666667-17.066667-42.666667-42.666667v-256h597.333334v256zM213.333333 426.666667V341.333333c0-25.6 17.066667-42.666667 42.666667-42.666666h42.666667v42.666666c0 25.6 17.066667 42.666667 42.666666 42.666667s42.666667-17.066667 42.666667-42.666667V298.666667h256v42.666666c0 25.6 17.066667 42.666667 42.666667 42.666667s42.666667-17.066667 42.666666-42.666667V298.666667h42.666667c25.6 0 42.666667 17.066667 42.666667 42.666666v85.333334H213.333333z"
                    fill="#797979"></path>
                  <path
                    d="M341.333333 682.666667h341.333334c25.6 0 42.666667-17.066667 42.666666-42.666667s-17.066667-42.666667-42.666666-42.666667H341.333333c-25.6 0-42.666667 17.066667-42.666666 42.666667s17.066667 42.666667 42.666666 42.666667z"
                    fill="#797979"></path>
                </svg></i>
              {{ articleData.createtime }}
            </span>
            <span class="separator">·</span>
            <span class="info-item">
              <i style="vertical-align: -2px;"><svg viewBox="0 0 1024 1024" width="14" height="14">
                  <path d="M14.656 512a497.344 497.344 0 1 0 994.688 0 497.344 497.344 0 1 0-994.688 0z"
                    fill="var(--iconColor)"></path>
                  <path
                    d="M374.976 872.64c-48.299-100.032-22.592-157.44 14.421-211.37 40.448-58.966 51.115-117.611 51.115-117.611s31.659 41.386 19.115 106.005c56.149-62.72 66.816-162.133 58.325-200.405 127.317 88.746 181.59 281.002 108.181 423.381C1016 652.501 723.093 323.2 672.277 285.867c16.939 37.333 20.054 100.032-14.101 130.474-58.027-219.84-201.664-265.002-201.664-265.002 16.96 113.536-61.781 237.397-137.344 330.24-2.816-45.163-5.632-76.544-29.483-119.808-5.333 82.176-68.373 149.269-85.29 231.445-22.912 111.637 17.237 193.173 170.581 279.424z"
                    fill="#FFFFFF"></path>
                </svg></i>
              {{ articleData.pageviews }}
            </span>
            <span class="separator">·</span>
            <span class="info-item">
              <i style="vertical-align: -2px;"><svg viewBox="0 0 1024 1024" width="14" height="14">
                  <path
                    d="M113.834667 291.84v449.194667a29.013333 29.013333 0 0 0 28.842666 29.013333h252.928v90.453333l160.597334-90.453333h252.928a29.013333 29.013333 0 0 0 29.013333-29.013333V291.84a29.013333 29.013333 0 0 0-29.013333-29.013333h-665.6a29.013333 29.013333 0 0 0-29.696 29.013333z"
                    fill="#FFDEAD"></path>
                  <path
                    d="M809.130667 262.826667h-665.6a29.013333 29.013333 0 0 0-28.842667 29.013333v40.106667a29.013333 29.013333 0 0 1 28.842667-29.013334h665.6a29.013333 29.013333 0 0 1 29.013333 29.013334V291.84a29.013333 29.013333 0 0 0-29.013333-29.013333z"
                    fill="#FFF3DB"></path>
                  <path
                    d="M556.202667 770.048h252.928a29.013333 29.013333 0 0 0 29.013333-29.013333V362.837333s-59.733333 392.533333-724.309333 314.709334v63.488a29.013333 29.013333 0 0 0 28.842666 29.013333h253.098667v90.453333z"
                    fill="#F2C182"></path>
                  <path
                    d="M619.008 632.32l101.888-35.157333-131.754667-76.117334 29.866667 111.274667zM891.904 148.992a61.44 61.44 0 0 0-84.138667 22.528l-19.968 34.133333 106.666667 61.610667 19.968-34.133333a61.781333 61.781333 0 0 0-22.528-84.138667z"
                    fill="#69BAF9"></path>
                  <path d="M775.338667 198.775467l131.669333 76.032-186.026667 322.218666-131.6864-76.032z"
                    fill="#F7FBFF">
                  </path>
                  <path
                    d="M775.168 198.826667l-5.290667 9.216 59.221334 34.133333a34.133333 34.133333 0 0 1 12.458666 46.592l-139.946666 242.346667a34.133333 34.133333 0 0 1-46.762667 12.629333l-59.050667-34.133333-6.656 11.434666 88.746667 51.2L720.896 597.333333l186.026667-322.56z"
                    fill="#D8E3F0"></path>
                  <path
                    d="M616.448 622.592l2.56 9.728 101.888-35.157333-44.885333-25.941334-59.562667 51.370667zM891.904 148.992c-1.024 0-2.218667-0.853333-3.242667-1.536A61.610667 61.610667 0 0 1 887.466667 204.8l-19.968 34.133333-73.728-42.496-5.12 8.704 106.666666 61.610667 19.968-34.133333a61.781333 61.781333 0 0 0-23.381333-83.626667z"
                    fill="var(--iconColor)"></path>
                  <path
                    d="M265.898667 417.621333H494.933333a17.066667 17.066667 0 1 0 0-34.133333H265.898667a17.066667 17.066667 0 1 0 0 34.133333zM265.898667 533.504H494.933333a17.066667 17.066667 0 0 0 0-34.133333H265.898667a17.066667 17.066667 0 0 0 0 34.133333z"
                    fill="var(--iconColor)"></path>
                  <path
                    d="M959.488 354.645333a99.84 99.84 0 0 0-23.722667-127.488 78.677333 78.677333 0 0 0-142.848-64.170666l-11.605333 20.138666a17.066667 17.066667 0 0 0-20.821333 7.168l-32.085334 55.466667H142.677333a46.250667 46.250667 0 0 0-45.909333 46.08v449.194667a46.08 46.08 0 0 0 45.909333 46.08h236.032v73.386666a17.066667 17.066667 0 0 0 8.362667 14.848 17.066667 17.066667 0 0 0 8.704 2.218667 17.066667 17.066667 0 0 0 8.362667-2.218667l156.672-88.234666h248.32a46.08 46.08 0 0 0 46.08-46.08V398.677333L921.6 283.306667a17.066667 17.066667 0 0 0-4.266667-21.504l1.877334-3.413334a65.365333 65.365333 0 0 1 10.410666 79.189334l-53.077333 91.989333a56.832 56.832 0 0 0 20.821333 77.653333 17.066667 17.066667 0 0 0 24.234667-6.314666 17.066667 17.066667 0 0 0-6.997333-23.04 23.04 23.04 0 0 1-8.362667-31.061334z m-138.410667 386.389334a11.946667 11.946667 0 0 1-11.946666 11.946666H556.202667a17.066667 17.066667 0 0 0-8.362667 2.218667l-134.997333 76.117333v-61.269333a17.066667 17.066667 0 0 0-17.066667-17.066667H142.677333a11.946667 11.946667 0 0 1-11.776-11.946666V291.84a11.946667 11.946667 0 0 1 11.776-11.946667h565.930667L574.464 512a17.066667 17.066667 0 0 0-1.706667 12.970667L597.333333 615.253333H265.898667a17.066667 17.066667 0 1 0 0 34.133334h352.938666a17.066667 17.066667 0 0 0 5.802667 0l102.4-35.328a17.066667 17.066667 0 0 0 9.216-7.509334l85.333333-147.968z m-204.8-184.661334l63.829334 36.864-49.322667 17.066667z m206.848-170.666666v1.365333l-108.373333 186.709333-102.4-59.050666L781.482667 221.866667l102.4 59.050666z m76.458667-161.28L887.466667 244.224l-76.970667-44.373333 11.264-19.797334a44.544 44.544 0 1 1 77.141333 44.544z"
                    fill="var(--iconColor)"></path>
                </svg></i>
              {{ articleData.comments }}
            </span>
          </div>
        </div>

      </div>

      <div class="article-content-wrapper">
        <div class="article-container">
          <div class="entry-content">
            <MdPreview :id="'preview-only'" :modelValue="articleData.text" :editorExtensions="{ highlight: { instance: hljs } }" />
          </div>
          <div class="article-update-time">
            <span>文章最后更新于 {{ articleData.finalltime }}</span>
          </div>
          <div class="article-sort">
            <span>{{ articleData.type }} · {{ articleData.label }}</span>
          </div>

          <blockquote class="article-disclaimer">
            <div>作者：{{ articleData.author }}</div>
            <div>1. 本网站部分内容可能来源于网络，仅供大家学习与参考，如有侵权，请联系站长进行删除处理。</div>
            <div>2. 本网站一切内容不代表本站立场，并不代表本站转型升级和对其真实性负责。</div>
            <div>
              <span>3. 版权&amp;许可请详阅</span>
              <span class="copyright-link">版权声明</span>
            </div>
          </blockquote>

          <!-- 评论区 -->
          <div class="comment-section">
            <div class="comment-head">
              <el-icon :size="22">
                <Edit />
              </el-icon>
              留言
            </div>
            <div class="comment-form">
              <textarea v-model="content" placeholder="写下点什么..." :maxlength="MAX_COMMENT_LENGTH"
                class="comment-textarea" />
              <div class="comment-form-actions">
                <div class="comment-form-left">
                  <el-popover placement="top-start" :width="300" trigger="hover" :show-after="200">
                    <template #default>
                      <div class="emoji-panel">
                        <span v-for="(path, name) in EMOJI_MAP" :key="name" class="emoji-item" @click="selectEmoji(name)">
                          <img :src="path" :title="name" width="24" height="24" loading="lazy" />
                        </span>
                      </div>
                    </template>
                    <template #reference>
                      <span class="action-btn">
                        <el-icon :size="20">
                          <Orange />
                        </el-icon>
                      </span>
                    </template>
                  </el-popover>
                  <el-tooltip content="选择图片" placement="top" :show-after="200">
                    <span class="action-btn" @click="openUploadDialog">
                      <el-icon :size="20">
                        <PictureFilled />
                      </el-icon>
                    </span>
                  </el-tooltip>
                </div>
                <span class="submit-btn" @click="submitComment">提交</span>
              </div>
            </div>

            <!-- 评论列表 -->
            <div class="comment-list">
              <div class="commentInfo-title">
                <span style="font-size: 1.15rem;">Comments | </span>
                <span>{{ commentNum }} 条留言</span>
              </div>
              <div v-for="comment in comments" :key="comment.id" class="comment-item">
                <el-avatar shape="square" :size="36">
                  <img :src="comment.avatar" style="object-fit: cover;" />
                </el-avatar>
                <div class="comment-body">
                  <div class="comment-header">
                    <div>
                      <div class="commentInfo-username">{{ comment.username }}</div>
                      <div class="commentInfo-other">{{ comment.createtime }}</div>
                    </div>
                    <span class="reply-btn" @click="openReplyDialog(comment.id, comment.id)">回复</span>
                  </div>
                  <div class="commentInfo-content" v-html="renderMessage(comment.content)" />

                  <!-- 子评论 -->
                  <div v-for="child in (comment.childComments?.records || [])" :key="child.id" class="child-comment">
                    <el-avatar shape="square" :size="34">
                      <img :src="child.avatar" style="object-fit: cover;" />
                    </el-avatar>
                    <div class="comment-body">
                      <div class="comment-header">
                        <div>
                          <div class="commentInfo-username">{{ child.username }}</div>
                          <div class="commentInfo-other">{{ child.createtime }}</div>
                        </div>
                        <span class="reply-btn" @click="openReplyDialog(child.id, comment.id)">回复</span>
                      </div>
                      <div class="commentInfo-content" v-html="renderMessage(child.content)" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
    <Footer />
    <BackToTop />
    <el-image-viewer v-if="previewVisible" :url-list="[previewImageUrl]" @close="previewVisible = false" />
    <!-- 回复对话框 -->
    <el-dialog v-model="dialogVisible" center title="留言" width="500" :before-close="handleClose"
      style="margin-top: 15vh;">
      <div class="reply-dialog">
        <textarea v-model="replyText" placeholder="写下点什么..." :maxlength="MAX_COMMENT_LENGTH" class="comment-textarea" />
        <div class="comment-form-actions">
          <div class="comment-form-left">
            <el-popover placement="top-start" :width="300" trigger="hover" :show-after="200">
              <template #default>
                <div class="emoji-panel">
                  <span v-for="(path, name) in EMOJI_MAP" :key="name" class="emoji-item" @click="selectEmojiReply(name)">
                    <img :src="path" :title="name" width="24" height="24" loading="lazy" />
                  </span>
                </div>
              </template>
              <template #reference>
                <span class="action-btn">
                  <el-icon :size="20">
                    <Orange />
                  </el-icon>
                </span>
              </template>
            </el-popover>
            <el-tooltip content="选择图片" placement="top" :show-after="200">
              <span class="action-btn" @click="openUploadDialog">
                <el-icon :size="20">
                  <PictureFilled />
                </el-icon>
              </span>
            </el-tooltip>
          </div>
          <span class="submit-btn" @click="submitReply">提交</span>
        </div>
      </div>
    </el-dialog>

    <!-- 上传对话框 -->
    <el-dialog v-model="showUploadImage" center title="文件" width="500" :before-close="cancelUpload">
      <el-upload ref="uploadRef" :drag="true" :limit="FILE_NUMS" v-model:file-list="fileList" :on-exceed="handleExceed"
        :auto-upload="false" :http-request="customUpload">
        <el-icon>
          <UploadFilled />
        </el-icon>
        <div>拖拽上传或者<em>点击上传</em></div>
        <template #tip>
          <div class="upload-tip">单个文件不能超过2Mb，仅支持 JPG、PNG 或 GIF 格式</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button type="primary" @click="handleUploadSubmit">上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
:deep(.pictureReg) {
  border-radius: 5px;
  object-fit: cover;
  width: 100%;
  max-width: 200px;
  max-height: 200px;
  display: block;
}

.article-head {
  height: 40vh;
  position: relative;
}

.my-animation-slide-top {
  animation-name: slide-top;
  animation-duration: 1s;
  animation-timing-function: ease-out;
  animation-fill-mode: both;
}

.article-image {
  width: 100%;
  height: 100%;
}

.article-info-container {
  position: absolute;
  bottom: 15px;
  left: 20%;
  color: #fff;
}

.article-title {
  font-size: 28px;
  margin-bottom: 15px;
}

.article-info {
  font-size: 14px;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.info-icon {
  vertical-align: -2px;
}

.separator {
  margin: 0 4px;
}

.article-info-ui {
  position: absolute;
  bottom: 10px;
  right: 20%;
  display: flex;
  gap: 5px;
}

.article-info-ui-button {
  width: 50px;
  padding: 4px 0;
  font-size: 14px;
  text-align: center;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.article-content-wrapper {
  background: #fff;
}

.article-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.entry-content {
  position: relative;
}


.article-update-time {
  color: #797979;
  font-size: 12px;
  margin: 20px 0;
  user-select: none;
}

.article-sort {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.article-sort span {
  padding: 3px 10px;
  background-color: orange;
  border-radius: 5px;
  font-size: 14px;
  color: #fff;
  transition: all 0.3s;
  cursor: pointer;
  user-select: none;
}

.article-sort span:hover {
  background-color: red;
}

.article-disclaimer {
  line-height: 2;
  border-left: 0.2rem solid #03a9f4;
  padding: 10px 1rem;
  background-color: #ecf7fe;
  border-radius: 4px;
  margin: 0 0 40px 0;
  color: #000;
}

.copyright-link {
  color: rgb(51, 136, 255);
  cursor: pointer;
}

.comment-head {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 700;
  margin: 20px 0;
  color: orange;
  user-select: none;
}

.comment-form {
  margin-bottom: 40px;
}

.comment-textarea {
  border: 1px solid #ddd;
  width: 100%;
  font-size: 14px;
  padding: 15px;
  min-height: 180px;
  resize: none;
  outline: none;
  border-radius: 4px;
  background-image: url('https://niu.codejourney.cn/commentURL.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: 100%;
  margin-bottom: 10px;
  box-sizing: border-box;
}

.comment-form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.comment-form-left {
  display: flex;
  gap: 12px;
}

.action-btn {
  font-size: 18px;
  cursor: pointer;
}

.action-btn:hover {
  transform: none;
}

.submit-btn {
  width: 66px;
  height: 33px;
  line-height: 33px;
  text-align: center;
  background: rgb(131, 123, 199);
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  user-select: none;
}

.emoji-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.emoji-item {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.emoji-item:hover {
  background: #ddd;
}

:deep(.emoji) {
  margin: 0.25rem;
  vertical-align: middle;
}

.comment-list {
  margin-top: 20px;
}

.commentInfo-title {
  margin-bottom: 20px;
  color: #797979;
  user-select: none;
}

.comment-item {
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.child-comment {
  margin-top: 15px;
  padding-left: 12px;
}

.comment-body {
  flex: 1;
  padding-left: 12px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.commentInfo-username {
  color: #ef794f;
  font-size: 16px;
  font-weight: 600;
}

.commentInfo-other {
  color: #797979;
  font-size: 12px;
  margin-top: 2px;
  user-select: none;
}

.commentInfo-content {
  margin: 10px 0 15px;
  padding: 15px;
  background: #f7f9fe;
  border-radius: 10px;
  color: #000;
  word-break: break-word;
}

.reply-btn {
  cursor: pointer;
  height: 22px;
  line-height: 22px;
  color: #fff;
  background: orange;
  border-radius: 0.2rem;
  padding: 0 6px;
  font-size: 12px;
  user-select: none;
}

.reply-dialog {
  padding: 0 20px;
}

.upload-tip {
  color: #999;
  font-size: 12px;
}

@keyframes slide-top {
  0% {
    opacity: 0;
    transform: translateY(-20%);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
