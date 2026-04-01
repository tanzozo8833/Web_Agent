# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY src/ ./src/
COPY public/ ./public/

ENV CI=true NODE_ENV=production
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS runner
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nodejs
RUN npm install -g serve

COPY --from=builder --chown=nodejs:nodejs /app/build ./build
COPY --chown=nodejs:nodejs server.js ./

USER nodejs
ENV PORT=3000 NODE_ENV=production
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["serve", "-s", "build", "-l", "3000"]
