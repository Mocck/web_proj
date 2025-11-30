import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 新增：引入 Tailwind 的入口样式文件（让所有 Tailwind 工具类在全局生效）
import './styles/tailwind.css'

/* 新增：引入 Element Plus 组件库（JS 逻辑） */
import ElementPlus from 'element-plus'
/* 新增：引入 Element Plus 的基础样式（必须与上面一行配合，否则组件无样式） */
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(router)

/* 新增：在应用实例上安装 Element Plus，使 <el-*> 组件可用 */
app.use(ElementPlus)

app.mount('#app')
