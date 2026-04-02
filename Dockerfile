FROM python:3.10-slim
WORKDIR /app

# 1. Cài đặt git và xóa cache để giảm dung lượng image
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 2. Cấu hình bảo mật Git cho Docker
RUN git config --global --add safe.directory /app

# 3. THÊM DÒNG NÀY: Cấu hình danh tính để Bot có thể thực hiện lệnh 'git commit'
RUN git config --global user.email "bot-agent@render.com" && \
    git config --global user.name "Tan-AI-Agent"

# 4. Cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ code (Bao gồm cả các folder app khác để OpenCode có thể sửa)
COPY . .

# 6. Mở cổng cho Flask Health Check
EXPOSE 10000

# 7. Chạy Bot
CMD ["python", "main.py"]