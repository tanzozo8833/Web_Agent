# 1. Gốc là Python
FROM python:3.10-slim

# 2. Cài đặt các công cụ hệ thống và NODE.JS (Phải làm bước này TRƯỚC)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Giờ mới có NPM để cài OpenCode
RUN npm install -g opencode-ai

# 4. Cấu hình Git
RUN git config --global user.email "bot-agent@render.com" && \
    git config --global user.name "Tan-AI-Agent" && \
    git config --global --add safe.directory /app

# 5. Cài đặt thư viện Python (requirements.txt đã bỏ opencode-ai)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy code và chạy
COPY . .
EXPOSE 10000

CMD ["python", "main.py"]