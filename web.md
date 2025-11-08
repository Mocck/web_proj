# 用户管理系统构建

## 流程

- 注册

填写相关信息，注册表单  -> 后端对应接口校验 -> if valid: 写入数据库

- 登录
  
{user:password} -> 后端对应接口校验 -> if success: return token

- 访问页面

Http + token -> 后端对应接口接收 Http request -> 判断token合法性 -> 返回对应 Http Reponse 

注：

1) 前后端都应确保的传入的数据安全性:校验
2) token 存在有效期，当 token 过期时，通过 refesh_token 得到新的{token， refresh_token}

- 返回页面

获取用户权限 -> Home菜单页面 -> 返回前端


# Django SimpleJWT 只允许 access token 用于访问受保护接口。

| 名称                | 有效期           | 用途                                    | 存放位置（前端）                         | 说明                                                |
| ----------------- | ------------- | ------------------------------------- | -------------------------------- | ------------------------------------------------- |
| **access token**  | 短（一般 5~15 分钟） | 用来访问需要身份验证的 API，比如 `/me`、`/profile` 等 | 通常放在内存或请求头中                      | 每次请求都要携带它（`Authorization: Bearer <access_token>`） |
| **refresh token** | 长（一般 7~30 天）  | 用来在 access 过期后，**获取新的 access**        | 一般安全地保存在 localStorage 或 cookie 中 | 不能直接访问 API，只能换取新 access                           |


| 接口类型       | 是否加装饰器            | 原因          |
| ---------- | ----------------- | ----------- |
| 登录、注册、验证码等 | ✅ 加上              | 因为用户还没登录    |
| 用户资料、个人中心等 | ❌ 不加              | 需要 token 验证 |
| 全局默认权限     | `IsAuthenticated` | 保证安全        |

- 前端（浏览器/移动端）关于 token 的存储建议

最佳安全实践：把 token （尤其 access token）放在 HttpOnly、Secure 的 cookie 中由后端设置（更安全，防 XSS）。如果

必须在 JS 里保存，优先使用内存或短期 localStorage（有 XSS 风险）。

refresh token 存放在 HttpOnly cookie 或更受限的存储，并实现刷新/黑名单策略以便登出/撤销。

强制 HTTPS。不要把 token 放在 URL（会被日志/Referer 泄露）。

- 服务器端注意点
  
登录/注册只是“颁发 token”。如果你希望“可撤销 token”，需要引入 token 黑名单或在后端维护会话（simplejwt support 

blacklist app）。

切换到 cookie-based token（HttpOnly）需要后端在登录时使用 Set-Cookie 写入，前端不直接保存 token。


- CSRF 的作用：防止攻击者利用用户已登录（凭证存在浏览器 cookie）的状态，在用户不知情的情况下发起对受信任站点的“写操

作”请求（如 POST/PUT/DELETE），导致未授权的状态改变。

什么时候生效：由服务端的 CSRF 检查（Django 的 CsrfViewMiddleware 或相应机制）在“非安全方法”（通常指 POST、PUT、

PATCH、DELETE 等会改变状态的 HTTP 方法）时执行。GET/HEAD/OPTIONS 被视为“安全/只读”方法，通常不会触发 CSRF 校验。

与 Authorization header（Bearer token）对比：如果客户端每次都在 Authorization 头里显式发送 token（不是依赖浏览器

自动带的 cookie），CSRF 风险大幅降低，通常服务器不会对这种请求做 CSRF 校验；但当认证依赖 cookie（浏览器自动发送的凭

证）时，就必须做 CSRF 校验。

# 在我们项目（cookie-based JWT）中的具体建议与流程

场景：我们把 JWT 放在 HttpOnly 的 access / refresh cookie 中（浏览器自动随请求发送）。因为凭证是 cookie，所以必须同时启用 CSRF 保护以防 CSRF 攻击。

推荐前后端交互流程（我们已添加的 /api/users/csrf/ 端点正是为此设计）：
用户登录：POST /api/users/login/，服务端在响应中设置 Set-Cookie: access=...; HttpOnly 和 Set-Cookie: refresh=...; HttpOnly。
前端获取 CSRF token：
方法 A（推荐）：向 GET /api/users/csrf/ 发请求（带 credentials），服务端返回 JSON 包含 csrfToken，并同时设置 csrftoken cookie。前端把这个 token 存在内存或直接在后续请求 header 中使用。
方法 B：如果 CSRF_COOKIE_HTTPONLY=False，前端可直接从 document.cookie 读取 csrftoken cookie（注意安全考虑）。
发起写请求（POST/PUT/DELETE）时：
设置请求头 X-CSRFToken: <csrfToken>（从步骤 2 得到的值）。
确保请求发送时带上 cookie：fetch/axios 需设置 credentials: 'include' 或 withCredentials: true。
服务端（Django）在 CsrfViewMiddleware 中验证 header 中的 token 与 cookie/session 中的 token 是否匹配。
重要：因为 access 是 HttpOnly，前端不能从 JS 读取它——这正是安全点。前端只需负责获取 CSRF token 并在 header 里传回去，cookie 会由浏览器自动发送

# 配置和部署注意（常见坑）

跨域（前后端不同域或端口）时：
需要 CSRF_TRUSTED_ORIGINS = ['https://your.frontend.domain']（Django >=4.0 格式）。
如果使用 django-cors-headers，需要 CORS_ALLOW_CREDENTIALS = True 并允许该前端域。
Cookie 的 SameSite：若跨站点发起请求并希望浏览器发送 cookie，需要 SameSite=None 且 Secure=True（必须 HTTPS）。否则浏览器可能不会发送 cookie，从而导致认证或 CSRF 校验失败。
CSRF_COOKIE_HTTPONLY：
默认是 False（允许 JS 读取 csrftoken cookie）。如果你把它设置为 True，JS 无法读到 cookie，这时必须通过专门的 endpoint（如我们加的 /csrf/）把 token 返回给前端。
Middleware：确保 CsrfViewMiddleware 在 MIDDLEWARE 中启用。
Blacklist/logout：即便你黑名单了 refresh token，仍需确保前端在 logout 时清除 cookie（服务端 Set-Cookie 清空或前端发请求后收到 Set-Cookie 删除）。

# 开启了 JWT 黑名单/刷新 token 功能，Simple JWT 需要在 OutstandingToken 表中写一条记录。

而 OutstandingToken.user 外键指向 settings.AUTH_USER_MODEL（默认 'auth.User'）。

你传入的是自定义 User，类型不匹配 → 报错。

# 🔹 前端说明

meta: { requiresAuth: true } 用来标记哪些页面需要验证 token

beforeEach 是全局守卫，每次路由跳转都会执行

如果用户没登录（token 为空），就重定向到 /login


💡 原因解释

在 <script setup> 语法下，router 不是全局变量；

需要用 Vue Router 的组合式函数：

import { useRouter } from 'vue-router'
const router = useRouter()


否则在执行 router.push() 时就会抛出 router is not defined。

✅ 小提示

router.push() 是 Vue 内部跳转（SPA 内跳转）


# DRF Serializer 两种属性：

## 输入数据（反序列化）

### 来自 request.data

- 由 serializer.validated_data 提供

- 包含你在 fields 中定义的字段，只要在 write_only=True 的字段也在这里可访问

### 输出数据（序列化）

- serializer.data

- 用于返回给客户端

- 默认会忽略 write_only=True 的字段, 所以 password 不会出现在这里

```python
serializer.validated_data:
{'username': 'alice', 'email': 'alice@example.com', 'password': '123456', 'nickname': 'Alice'}

serializer.data:
{'username': 'alice', 'email': 'alice@example.com', 'nickname': 'Alice'}
```

# DRF 的 Response 类的签名如下：

``Response(data=None, status=None, template_name=None, headers=None, content_type=None)``


- 它要求第一个参数 data 是：

- 一个可被 JSON 序列化（serializable） 的对象。


### ImageField 是专门为图片文件设计的字段，它继承自 FileField。
Django 会自动帮你处理上传、存储、路径管理。

MySQL 中不会存二进制数据，而是只存储文件的相对路径，比如：

```avatars/user_123.jpg
```

前端访问 时，可以通过：

```user.avatar.url
```

获取图片的可访问 URL。





# django 中数据库操作

- Q 对象用于在 ORM 查询中实现 逻辑运算（AND / OR / NOT） 的组合查询

- 普通 filter 只能用 AND

User.objects.filter(username='tony', email='t@example.com') => WHERE username='tony' AND email='t@example.com'

如果你想做 OR 或 NOT，就必须用 Q：

User.objects.filter(Q(username='tony') | Q(email='t@example.com'))

# ✅ 与 exclude() 配合

你也可以这样写：

User.objects.exclude(Q(is_active=False) | Q(is_deleted=True))


→ 过滤掉非活跃或已删除的用户。

# ForeignKey：用于表达关系、保证引用完整性并方便 ORM 操作。已正确使用。注意设置合适的 on_delete 策略（你用的 RESTRICT 是保护性更强的选择）。
# models.Index：用来加速常用的 filter/order/join。但要基于查询模式、基数和写入频率进行权衡。对 owner、created_at、deleted_at 等字段建立索引通常是合理的；对低选择性字段单列索引需谨慎，考虑复合索引替代。