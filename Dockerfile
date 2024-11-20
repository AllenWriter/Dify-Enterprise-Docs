# 使用 Node.js 作为基础镜像
FROM node:22-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json（如果存在）
COPY package*.json ./

# 安装依赖
RUN npm install

# 全局安装 mintlify
RUN npm install -g mintlify

# 复制所有文件到容器中
COPY . .

# 设置默认端口为 3000，但允许在运行时覆盖
ENV PORT=3005

# 启动 Mintlify，使用环境变量中的端口
CMD mintlify dev --port $PORT