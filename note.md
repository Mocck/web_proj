# 一、背景：为什么需要 middleware corsheaders

当你的 前端项目（例如 Vue） 在 http://localhost:8080 运行，
而 Django 后端 API 在 http://localhost:8000 运行时，
浏览器会因为 同源策略 (Same-Origin Policy) 阻止前端请求后端接口。

同源策略要求：协议、域名、端口必须完全相同，否则为跨域请求。
举例：

- ✅ 同源： http://localhost:8000
 → http://localhost:8000

- ❌ 跨域： http://localhost:8080
 → http://localhost:8000

#### 解决方法：在 Django 端允许来自特定来源的跨域请求 —— 就用到 django-cors-headers。

# 二、安装与配置步骤

1️⃣ 安装
```bash
pip install django-cors-headers
```

2️⃣ 在 **myproject.settings.py** 中注册 app
```pyhton
INSTALLED_APPS = [
    ...,
    'corsheaders',
]
```

3️⃣ 在中间件中添加（顺序非常重要）
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```

# 三、配置允许跨域的规则

- 只允许指定前端域名
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Vue 开发服务器
    "https://your-frontend-domain.com",  # 部署后的前端域名
]
```

- 允许特定 HTTP 方法
```python 
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
]
```


# 四、Django 中常用的中间件（Middleware）

中间件是 Django 在请求进入视图函数之前 和 响应返回浏览器之前 自动执行的钩子。可以把它看作一个 **全局拦截器链**。

🔹 请求生命周期简单图
```
Browser → Middleware → View → Middleware → Response → Browser
```

| 中间件                                                                          | 功能描述                             | 是否常用        |
| ---------------------------------------------------------------------------- | -------------------------------- | ----------- |
| `django.middleware.security.SecurityMiddleware`                              | 启用安全特性（如 HSTS、XSS 防护、内容类型限制等）    | ✅ 必用（生产）    |
| `django.contrib.sessions.middleware.SessionMiddleware`                       | 管理 session（基于 cookie 或数据库）       | ✅ 登录系统必用    |
| `django.middleware.common.CommonMiddleware`                                  | 实现常见 HTTP 功能（如 URL 规范化、ETag、缓存头） | ✅ 常用        |
| `django.middleware.csrf.CsrfViewMiddleware`                                  | 防止跨站请求伪造攻击 (CSRF)                | ✅ 表单/登录必用   |
| `django.contrib.auth.middleware.AuthenticationMiddleware`                    | 解析用户身份，绑定 `request.user`         | ✅ 登录系统必用    |
| `django.middleware.clickjacking.XFrameOptionsMiddleware`                     | 防止被 iframe 嵌套攻击                  | ✅ 推荐        |
| `corsheaders.middleware.CorsMiddleware`                                      | 支持跨域请求（第三方库 django-cors-headers） | ⚙️ 前后端分离时必用 |
| `django.middleware.cache.UpdateCacheMiddleware` / `FetchFromCacheMiddleware` | 页面级缓存支持                          | ⚙️ 性能优化可用   |


# 🧩 五、Redis 在 Django 中的使用

Redis 在 Django 里主要有三个用途：

| 用途           | 说明                              |
| ------------ | ------------------------------- |
| ✅ 缓存系统       | 加速数据库查询结果、API响应等                |
| ✅ Session 存储 | 代替默认的数据库 session                |
| ✅ Celery 后端  | 作为任务队列的 broker 和 result backend |


1️⃣ 安装 Redis 与 Python 依赖
```python
# 安装 Python 库
pip install redis django-redis
```

2️⃣ 配置缓存（Cache）

在 settings.py：
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

使用缓存 API：
```python
from django.core.cache import cache

# 设置缓存
cache.set('user_count', 100, timeout=60)  # 60秒过期

# 获取缓存
value = cache.get('user_count')
```

3️⃣ 将 Redis 用作 Session 存储
```python
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

# 六、遇到的一些问题


- 使用 异步视图 (async def) + DRF 的 Response 对象

Django REST Framework 的 Response 类是 同步环境专用的，
它内部最终会调用 Django 的 WSGI HttpResponse 流程。
```
在异步环境中（async def 视图），DRF 无法正确处理 Response 对象 → 导致 500 Internal Server Error。
```

- 在 Django REST Framework（DRF）中：
```python
serializer = AgentSerializer(rows, many=True)
serializer.data
```

返回的是一个 ReturnDict 或 ReturnList 对象，而不是普通 Python list。

它是只读属性，你不能直接修改。


- Vue 项目中 main.js 解析：

``createApp(App)``：创建一个 Vue 应用实例，把 App.vue 当作根组件。

``app.mount('#app')``：把 Vue 应用挂载到 HTML 页面中 id="app" 的元素上。

所以 app 就是你整个 Vue 应用的“核心实例”，之后所有插件、全局组件、路由、状态管理等都可以通过它来安装。


- router 是 Vue Router 实例。
  ``app.use(router)``:作用是把路由功能安装到 Vue 应用上，让整个应用都能识别 ``<router-view /> 和 <router-link>``


安装后，``<router-view />`` 可以自动显示当前路由对应的组件。

所以你的 App.vue 里虽然只有 ``<router-view />``，只要安装了路由插件，它就会渲染当前路由的组件。

- app.use() 是 Vue 提供的安装插件的方法。任何插件、库或者中间件都可以通过 app.use() 安装到整个应用实例。
```js
app.use(router)       // 安装路由
app.use(store)        // 安装 Vuex / Pinia
app.use(ElementPlus)  // 安装 UI 组件库
```

安装插件后，相关功能、组件、指令就可以在全局使用，不需要在每个单独的组件里重复引入。