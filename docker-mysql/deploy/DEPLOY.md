# 知识库系统

# 工作流

# 插件

# 多模型支持

# 智能体管理

用 nginx 80 端口 提供静态文件了，Vite 代理根本不起作用，因为 Vite 代理只在开发环境（npm run dev / vite dev server）生效。

这就是为什么 /api/users/login/ 返回 404 的原因：

浏览器请求 http://localhost/api/users/login/ → nginx 接管 → nginx 没有转发 → 返回 404

Django 容器监听 0.0.0.0:8080，nginx 没有代理到这个端口