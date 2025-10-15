# 项目名称

实现一个前后端智能体创建平台，微信小程序的三端网页项目

## 目录

- [安装](#安装)
- [使用方法](#使用方法)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 安装

```bash
# 克隆仓库
git clone https://github.com/Mocck/web_proj.git
cd your-repo

# 安装依赖
npm install

# axios（HTTP 客户端）
npm i axios

# 样式与构建
npm i -D tailwindcss postcss autoprefixer @tailwindcss/postcss

# UI 组件库
npm i element-plus @element-plus/icons-vue

pip install django uvicorn
```

## 使用方法

启动vue前端
```bash
npm run dev

# 产出 dist/ 静态文件
npm run build
```


启动django后端
```bash
python manage.py runserver
```


微信小程序
```bash
```


e.g.

### 一、前端vue添加页面:

（1）/views 添加.vue文件；

（2）在/router/index.js中注册 

``{ path: '/ping', name: 'ping', component: PingView }``

### 二、后端Django异常处理流程:

浏览器请求 → Django URLConf

    （1）setting.py 中 INSTALLEDAPPS 注册DRF，匹配到 DRF 的路由 → DRF 视图(使用@api_view 装饰的函数)
           -a 抛出业务异常、数据库异常 … → DRF custom_exception_handler 统一 JSON
           -b 正常返回 DRF::Response
    （2）没有匹配到任何路由,注册在根目录urls.py → handler404 → 普通JsonResponse

### 三、asyncio
``见async.md``

### 四、Mysql

（1）备份数据：
```bash
docker exec mysql8-demo \
  mysqldump -u demo_user -p你的密码 demo_db > backup.sql
```

```bash
# 启动所有服务（后台运行）
docker compose up -d

# 查看服务状态
docker compose ps

# 查看服务日志
docker compose logs
docker compose logs mysql
docker compose logs phpmyadmin

```
(2)在django中使用Mysql：

在 settings.py 中，DATABASES 是一个字典，可以配置多个命名数据库。

Run ``python manage.py migrate`` to migrate newest database change

```python
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',   # 使用 MySQL
        'NAME': 'demo_db',                      # 你的数据库名
        'USER': 'demo_user',                    # 数据库用户名
        'PASSWORD': 'demo_pass_123',            # 数据库密码
        'HOST': 'localhost',                    # 本地就用这个
        'PORT': '3306',                         # MySQL 默认端口
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
```
### 五、在 phpMyAdmin 中创建数据库表

```SQL
-- 创建应用表
CREATE TABLE t_app (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
  name VARCHAR(100) NOT NULL COMMENT '应用名称',
  description VARCHAR(255) NOT NULL COMMENT '简短描述',
  full_description TEXT COMMENT '详细描述',
  avatar VARCHAR(255) COMMENT '应用头像URL',
  category VARCHAR(64) COMMENT '应用分类',
  price DECIMAL(10,2) DEFAULT 0.00 COMMENT '价格',
  rating DOUBLE COMMENT '评分',
  downloads INT COMMENT '下载量',
  reviews INT COMMENT '评论数',
  author VARCHAR(100) COMMENT '作者',
  published_at DATE COMMENT '发布日期',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='应用信息表';

-- 插入示例数据
INSERT INTO t_app(name, description, full_description, avatar, category, price, rating, downloads, reviews, author, published_at)
VALUES
('智能客服助手', '基于大语言模型的智能客服系统，支持多轮对话和知识库检索',
 '这是一个功能强大的智能客服系统，能够理解用户意图，提供准确回答。支持多轮对话、知识库检索、情感分析等功能。',
 'https://via.placeholder.com/80x80', 'customer-service', 0.00, 4.8, 1200, 156, 'AI团队', '2024-01-15'),
('内容创作大师', 'AI驱动的内容生成和优化工具，支持多种文体创作',
 '专业的内容创作工具，利用AI技术帮助用户快速生成高质量内容。支持文章、广告文案、社交媒体内容等多种文体的创作和优化。',
 'https://via.placeholder.com/80x80', 'content-creation', 0.00, 4.9, 980, 123, '创作工坊', '2024-01-10');

```
## 贡献指南

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细流程。

## 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。