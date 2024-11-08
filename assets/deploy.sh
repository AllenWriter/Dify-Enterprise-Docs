#!/bin/bash

echo "开始部署流程..."

# 构建 Docker 镜像
echo "第一步：构建 Docker 镜像"
docker build -t dify-enterprise-docs-demo .

# 删除旧容器
echo "第二步：删除旧容器"
docker rm -f dify-docs-demo || true

# 运行新容器
echo "第三步：运行新容器"
docker run -d --restart unless-stopped --name dify-docs-demo -p 3005:3005 -e PORT=3005 dify-enterprise-docs-demo

echo "部署完成！"