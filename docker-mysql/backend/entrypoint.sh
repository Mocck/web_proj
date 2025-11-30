#!/bin/bash
set -e

# 等待 MySQL 启动
echo "Waiting for MySQL..."

until mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_ROOT_PASSWORD" --ssl=0 -e "SELECT 1;" &> /dev/null; do
  echo "Waiting for MySQL..."
  sleep 2
done

echo "MySQL is up."

# 执行 migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# 收集 static（可选）
# python manage.py collectstatic --noinput

# 启动服务
echo "Starting server..."
python manage.py runserver 0.0.0.0:8080

# 或者使用 Gunicorn 作为生产服务器
# gunicorn backend.wsgi:application --bind 0.0.0.0:8080
# uvicorn backend.asgi:application --host 0.0.0.0 --port 8080