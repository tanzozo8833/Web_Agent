# Stage 1: Build React Frontend
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files và cài đặt dependencies
COPY package*.json ./
RUN npm ci 

# Copy mã nguồn và Build React thành các file tĩnh (folder build/)
COPY . .
ENV CI=true NODE_ENV=production
RUN npm run build

# Stage 2: Production Runner (Chạy Express Server)
FROM node:20-alpine AS runner
WORKDIR /app

# Bảo mật: Không chạy bằng quyền root
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nodejs

# Copy kết quả build từ Stage 1
COPY --from=builder --chown=nodejs:nodejs /app/build ./build
# Copy server.js và package.json để chạy Express
COPY --from=builder --chown=nodejs:nodejs /app/server.js ./
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./

# Chỉ cài đặt các thư viện cần thiết cho production
RUN npm install --production

USER nodejs

# Render mặc định ưu tiên cổng 10000 cho gói Free
ENV PORT=10000
ENV NODE_ENV=production
EXPOSE 10000

# Chạy server.js (Express sẽ serve folder build/)
CMD ["node", "server.js"]