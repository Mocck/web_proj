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

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看服务日志
docker compose logs -f mysql
docker compose logs -f phpmyadmin


Compose 里的 networks 是一个虚拟私有网络（bridge 网络）。

在同一个 network 下的容器可以通过“服务名”互相访问，比如：

phpmyadmin 访问数据库主机名：mysql

django 容器访问数据库主机名：mysql

redis 容器访问主机名：redis

不需要用 IP 地址，也不能用 localhost。

```bash
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'demo_db',
    'USER': 'demo_user',
    'PASSWORD': 'demo_pass_123',
    'HOST': 'mysql',  # <== 就是 compose 里定义的服务名
    'PORT': '3306',
  }
}
```

```
(2)在django中使用Mysql：

在 settings.py 中，DATABASES 是一个字典，可以配置多个命名数据库。

Run ``python manage.py migrate`` to migrate newest database change

```python
DATABASES = {
     'default': { # 主数据库
        'ENGINE': 'django.db.backends.mysql',   # 使用 MySQL
        'NAME': 'demo_db',                      # 你的数据库名
        'USER': 'demo_user',                    # 数据库用户名
        'PASSWORD': 'demo_pass_123',            # 数据库密码
        'HOST': 'localhost',                    # 本地就用这个
        'PORT': '3306',                         # MySQL 默认端口
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    },
    'analytics': {  # 第二个数据库，用于日志或统计
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'analytics_db',
        'USER': 'analytics_user',
        'PASSWORD': 'analytics_pass_123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    },
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

### 六、Celery

| 运行方式                             | 正确的 `CELERY_BROKER_URL`                 |
| -------------------------------- | --------------------------------------- |
| Django、Celery、Redis 都在 Docker 里  | `redis://:redis123456@redis:6379/0`     |
| Redis 在 Docker，Django/Celery 在本地 | `redis://:redis123456@localhost:6379/0` |
| Redis 本地安装（无密码）                  | `redis://localhost:6379/0`              |


# 启动 worker
celery -A backend worker -l info

# 启动 beat
celery -A backend beat -l info



🧩 一、Celery 架构概念快速回顾

Celery 是一个分布式任务队列系统，它主要分为三部分：

组件	作用
Producer（生产者）	比如你的 Django 代码，用 task.delay() 发任务
Broker（消息中间件）	比如 Redis 或 RabbitMQ，用来暂存任务消息
Worker（消费者）	负责真正执行任务的进程
Beat（调度器）	负责定时发送任务（例如每隔 30 分钟解锁用户）
⚙️ 二、两条命令的区别与作用
✅ 1️⃣ celery -A backend worker -l info

👉 启动 Celery Worker（任务执行者）

这是 Celery 的“工人”，会一直监听 Redis 队列。

当你的 Django 代码调用：

unlock_locked_users.delay()


这个任务就会被丢进 Redis，然后由 worker 执行。

简单说：

Worker 是“执行任务”的后台进程。

📘 参数解释：

-A backend：指定 Celery 应用名（对应项目 backend/celery.py）

-l info：显示日志等级（info 表示输出一般日志）

✅ 2️⃣ celery -A backend beat -l info

👉 启动 Celery Beat（任务调度器）

这是 Celery 的“闹钟”，负责周期性调度任务。

例如你的项目里：

@shared_task
def unlock_locked_users():
    ...


你可能在 celery.py 或 settings.py 里定义了：

CELERY_BEAT_SCHEDULE = {
    'unlock-users-every-30-mins': {
        'task': 'app.tasks.unlock_locked_users',
        'schedule': timedelta(minutes=30),
    },
}


Beat 就会每 30 分钟“发布”这个任务到 Redis 队列，
然后 Worker 发现有任务，就去执行它。

简单说：

Beat 是“定时发布任务”的后台进程。

🧠 三、为什么要分开运行？

原因在于：

Worker 是执行任务

Beat 是触发任务

二者职责完全不同，如果混在一个进程里可能会阻塞或出错。
尤其当任务很多或耗时较长时，Beat 无法正常调度。

💡 四、也可以合并（仅开发阶段）

如果你只是开发调试，可以用 一个命令同时启动二者：

celery -A backend worker -B -l info


参数 -B 就是让 worker 内部自带一个 beat 调度器。

不过生产环境不推荐这么做，因为：

Beat 和 Worker 会共用同一个进程；

Beat 调度可能被任务执行阻塞；

无法独立重启、扩容。

✅ 五、总结对比表

| 命令                                    | 作用       | 是否执行任务 | 是否定时调度 | 建议部署方式 |
| ------------------------------------- | -------- | ------ | ------ | ------ |
| `celery -A backend worker -l info`    | 执行任务     | ✅ 是    | ❌ 否    | 独立进程   |
| `celery -A backend beat -l info`      | 触发定时任务   | ❌ 否    | ✅ 是    | 独立进程   |
| `celery -A backend worker -B -l info` | 二合一（调试用） | ✅      | ✅      | 仅开发使用  |


## 贡献指南

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细流程。

## 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。