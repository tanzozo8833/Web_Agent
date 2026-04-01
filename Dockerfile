FROM python:3.10-slim
WORKDIR /app

# Quan trọng: Cài đặt git vì script của ông có dùng subprocess chạy lệnh git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN git config --global --add safe.directory /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ nhưng nhớ dùng .dockerignore (tí t nói ở dưới)
COPY . .

# Mở cổng 10000 (Render thích cổng này hơn 80 cho gói Free)
EXPOSE 10000

# SỬA ĐƯỜNG DẪN Ở ĐÂY:
CMD ["python", "main.py"]