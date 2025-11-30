#!/bin/bash

# ==================== 容器化自动化部署脚本（Django 后端） ====================
# 特点：完全在容器内构建，无需安装 Python/Django
# 适用于：生产服务器、CI/CD 流水线

set -e  # 遇到错误立即退出

# ==================== 颜色定义 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # 无颜色

# ==================== 日志函数 ====================
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_step() {
    echo -e "\n${BLUE}==================== $1 ====================${NC}\n"
}

# ==================== 检查命令是否存在 ====================
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# ==================== 开始部署 ====================
log_step "开始部署"
log_info "时间: $(date '+%Y-%m-%d %H:%M:%S')"

# ==================== 1. 环境检查 ====================
log_step "1. 环境检查"

log_info "检查 Docker..."
check_command docker
docker --version

log_info "检查 Docker Compose..."
check_command docker-compose
docker-compose --version

log_info "检查 .env 文件..."
if [ ! -f .env ]; then
    log_error ".env 文件不存在，请先创建配置文件"
    exit 1
fi
log_info ".env 文件存在 ✓"

# ==================== 2. 停止旧服务 ====================
log_step "2. 停止旧服务"

if docker-compose ps | grep -q "Up"; then
    log_warn "检测到正在运行的服务，停止中..."
    docker-compose down
    log_info "旧服务已停止 ✓"
else
    log_info "没有正在运行的服务"
fi

# ==================== 3. 构建 Docker 镜像 ====================
log_step "3. 构建 Docker 镜像"

log_info "开始构建所有服务的 Docker 镜像..."
log_warn "首次构建可能需要 3-5 分钟（下载依赖）"

# 构建时不使用缓存，确保获取最新代码
docker-compose build --no-cache

log_info "所有镜像构建完成 ✓"

# ==================== 4. 启动服务 ====================
log_step "4. 启动服务"

log_info "启动所有服务..."
docker-compose up -d

# 等待服务启动
log_info "等待服务启动 5 秒..."
sleep 5

# ==================== 5. 运行 Django 数据库迁移 ====================
log_step "5. Django 数据库迁移"

log_info "应用数据库迁移..."
docker exec -it backend python manage.py migrate

log_info "收集静态文件..."
docker exec -it backend python manage.py collectstatic --noinput

# ==================== 6. 验证部署 ====================
log_step "6. 验证部署"

log_info "检查服务状态..."
docker-compose ps

# ==================== 7. 部署完成 ====================
log_step "部署完成！"

echo -e "${GREEN}"
echo "========================================"
echo "✓ 部署成功！服务访问地址："
echo "========================================"
echo "前端管理端:  http://localhost"
echo "前端移动端:  http://localhost:81"
echo "Django 后端 API:  http://localhost:8080"
echo "PHPMyAdmin:  http://localhost:8081"
echo
