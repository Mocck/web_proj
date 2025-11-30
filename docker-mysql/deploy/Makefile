# ==================== Makefile for Health Agent Platform ====================
# 心理健康 Agent 平台 - 容器化部署命令接口

.PHONY: help deploy build build-backend build-frontend start stop restart logs logs-backend logs-frontend logs-mysql ps clean status backup

.DEFAULT_GOAL := help

# ==================== 帮助信息 ====================
help:
	@echo "========================================"
	@echo "Chat Agent 平台 - 部署命令"
	@echo "========================================"
	@echo ""
	@echo "部署命令："
	@echo "  make deploy         - 🚀 一键部署（构建+启动）"
	@echo "  make build          - 📦 构建所有镜像"
	@echo "  make build-backend  - 📦 只构建后端"
	@echo "  make build-frontend - 📦 只构建前端"
	@echo ""
	@echo "服务控制："
	@echo "  make start          - ▶️ 启动所有服务"
	@echo "  make stop           - ⏹️ 停止所有服务"
	@echo "  make restart        - 🔄 重启所有服务"
	@echo "  make ps             - 📋 查看服务状态"
	@echo ""
	@echo "日志查看："
	@echo "  make logs           - 📜 查看所有服务日志"
	@echo "  make logs-backend   - 📜 查看后端日志"
	@echo "  make logs-frontend  - 📜 查看前端日志"
	@echo "  make logs-mysql     - 📜 查看数据库日志"
	@echo ""
	@echo "运维管理："
	@echo "  make status         - ✅ 检查服务健康状态"
	@echo "  make backup         - 💾 备份数据库"
	@echo "  make clean          - 🗑️ 清理所有容器和镜像"
	@echo ""

# ==================== 部署命令 ====================
deploy:
	@echo "🚀 开始一键部署..."
	@./deploy.sh

# ==================== 构建命令 ====================
build:
	@echo "📦 构建所有服务镜像..."
	@docker-compose build

build-backend:
	@echo "📦 构建后端镜像..."
	@docker-compose build backend

build-frontend:
	@echo "📦 构建前端镜像..."
	@docker-compose build web-admin

# ==================== 服务控制 ====================
start:
	@echo "▶️ 启动所有服务..."
	@docker-compose up -d
	@echo "✅ 服务已启动！"
	@docker-compose ps

stop:
	@echo "⏹️ 停止所有服务..."
	@docker-compose down
	@echo "✅ 服务已停止！"

restart: stop
	@sleep 2
	@$(MAKE) start

ps:
	@docker-compose ps

# ==================== 日志查看 ====================
logs:
	@docker-compose logs -f

logs-backend:
	@docker-compose logs -f backend

logs-frontend:
	@docker-compose logs -f web-admin

logs-mysql:
	@docker-compose logs -f mysql

# ==================== 运维管理 ====================
status:
	@echo "========================================"
	@echo "服务健康状态检查"
	@echo "========================================"
	@docker-compose ps
	@echo ""
	@echo "容器资源使用："
	@docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" $$(docker-compose ps -q)

backup:
	@echo "💾 备份数据库..."
	@mkdir -p backups
	@docker-compose exec -T mysql sh -c 'exec mysqldump -uroot -p"$${MYSQL_ROOT_PASSWORD}" "$${MYSQL_DATABASE}"' > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ 备份完成！文件保存在 backups/ 目录"

clean:
	@echo "🗑️ 清理所有容器、镜像和数据卷..."
	@read -p "确认要清理吗？这将删除所有数据！(yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose down --rmi all --volumes --remove-orphans; \
		echo "✅ 清理完成！"; \
	else \
		echo "❌ 取消清理"; \
	fi
