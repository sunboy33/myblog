import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import path from "path"


export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"), // 关键配置：将 @/ 指向 src 目录
    }
  },
  server: {
    host: '0.0.0.0',  // 允许外部访问
    port: 5173,       // 指定端口
    strictPort: true, // 如果端口被占用则退出
     allowedHosts: [
      "codejourney.cn",
      "www.codejourney.cn"
    ]

  }
  
})
