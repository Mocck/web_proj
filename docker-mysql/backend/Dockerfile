# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y busybox \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    pkg-config \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*
    
# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目代码
COPY backend/ ./

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 端口
EXPOSE 8080

# 启动命令（开发模式）
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

