# User Management - Usage & Testing

此文档说明如何在本地环境中启用并测试 `user_management` 应用（包含 JWT 支持、Postman 示例以及如何运行单元测试）。

注意：本项目使用 `djangorestframework-simplejwt` 提供标准 JWT 功能，和 DRF 的 `APIClient` 进行测试。

1) 准备环境

- 创建并激活虚拟环境（Windows cmd 示例）：

```bat
python -m venv .venv
.venv\Scripts\activate
```

- 安装依赖：

```bat
pip install -r requirements.txt
# 如果项目没有 requirements.txt，请至少安装下面两个包：
pip install django djangorestframework djangorestframework-simplejwt
```

2) settings 要点

- REST framework 已配置使用 `rest_framework_simplejwt.authentication.JWTAuthentication`。

1) 常用 API（已挂载到 `/api/users/`）

- POST /api/users/register/  -> 注册，返回 user 和 token（包含 access/refresh）
- POST /api/users/login/     -> 登录，返回 user 和 token（access/refresh）
- POST /api/users/token/     -> standard token obtain endpoint (username/password)
- POST /api/users/token/refresh/ -> refresh access token
- GET  /api/users/me/        -> 当前用户信息（需 Authorization: Bearer <access>）
- GET  /api/users/           -> 用户列表（需认证），支持 q, page, page_size

4) Postman 快速测试（示例）

- 注册：
  - POST http://localhost:8000/api/users/register/
  - Body JSON: { "username": "alice", "email": "alice@example.com", "password":"pass123" }

- 登录：
  - POST http://localhost:8000/api/users/login/
  - Body JSON: { "username_or_email": "alice", "password": "pass123" }
  - 保存 response.token.access 到环境变量 `accessToken`

- 授权调用：
  - 在需要认证的请求中添加 Header: `Authorization: Bearer {{accessToken}}`

5) 运行单元测试（示例）

```bat
python manage.py test user_management
```

注意：你的环境需要安装 Django 和 DRF 以及 simplejwt，且数据库设置需可用（或使用 sqlite dev settings）。如果你遇到 `ModuleNotFoundError: No module named 'django'`，请先安装依赖并激活虚拟环境。

6) 如果需要我帮助

- 我可以：把 token 流程改为使用 refresh/access 的标准 endpoints（已经添加），或帮你修改为 cookie 存 token 的方案。也可以把 `managed=False` 的模型改为由 Django 管理并生成初始迁移（需要谨慎操作数据库）。

A. 注册（Register）

Method: POST
URL: http://localhost:8000/api/users/register/
Headers: Content-Type: application/json
Body (raw JSON):

{
"username": "alice",
"email": "alice@example.com",
"password": "pass123",
"nickname": "Alice",
"phone_number": "123456"
}

{
"username": "bob",
"email": "bob@example.com",
"password": "pass123",
"nickname": "Alice",
"phone_number": "2586669"
}

期望：201 返回 JSON 包含 user（不含 password）和 token 字符串。
注意：如果用户名或邮箱已存在会返回 400。

B. 登录（Login）

Method: POST
URL: http://localhost:8000/api/users/login/
Headers: Content-Type: application/json
Body:
{
"username_or_email": "alice",
"password": "pass123"
}
期望：200 返回 { "user": {...}, "token": "<token>" }

C. 带 token 的受保护接口（例如 /me/）

先从登录响应拿到 token。
Method: GET
URL: http://localhost:8000/api/users/me/
Headers:
Authorization: Bearer <token>
Accept: application/json
期望：200 返回当前用户信息；若 token 过期或无效返回 401。

D. 测试用户列表（分页 + 模糊搜索）

Method: GET
URL: http://localhost:8000/api/users/?q=ali&page=1&page_size=10
Headers: Authorization: Bearer <token>
响应示例：
{ "total": 12, "page": 1, "page_size": 10, "items": [ ... ] }
E. 用户详情/修改/删除

GET/PUT/DELETE 到 http://localhost:8000/api/users/<user_id>/
PUT body 仅包含允许更新的字段（nickname, email, phone_number, avatar, bio, is_active, is_locked）

F. 分配角色

POST http://localhost:8000/api/users/roles/assign/
Body:
{
"user_id": 6,
"role_id": 3
}
需要 Authorization: Bearer <token>

G. 在 Postman 中测试 token 过期或无效：

修改 token 的最后几个字符使签名无效，调用受保护接口应得到 401 invalid token；
若需要测试过期，可以在 settings 中把 USER_TOKEN_EXPIRE_SECONDS 暂设为很短（例如 5 秒），生成 token、等待 6 秒再访问，应该得到 "token expired"。