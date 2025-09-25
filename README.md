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
pip install django
```

## 使用方法

启动vue前端
```bash
npm run dev
```


启动django后端
```bash
python manage.py runserver
```


微信小程序
```bash
```


e.g.:
一、前端vue添加页面:
（1）/views 添加.vue文件；
（2）在/router/index.js中注册 { path: '/ping', name: 'ping', component: PingView }。

二、后端Django异常处理流程:
浏览器请求 → Django URLConf
    （1）setting.py 中 INSTALLEDAPPS 注册DRF，匹配到 DRF 的路由 → DRF 视图(使用@api_view 装饰的函数)
           -a 抛出业务异常、数据库异常 … → DRF custom_exception_handler 统一 JSON
           -b 正常返回 DRF::Response
    （2）没有匹配到任何路由,注册在根目录urls.py → handler404 → 普通JsonResponse
四、Mysql
（1）备份数据：docker exec mysql8-demo \
  mysqldump -u demo_user -p你的密码 demo_db > backup.sql

## 贡献指南

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细流程。

## 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。