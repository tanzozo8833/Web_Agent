# 1. Chọn hệ điều hành nhẹ nhàng (slim) có sẵn Python
FROM python:3.10-slim

# 2. Thiết lập thư mục làm việc bên trong Docker
WORKDIR /app

# 3. Copy file danh sách thư viện vào trước để tối ưu hóa việc build
COPY requirements.txt .

# 4. Cài đặt các thư viện
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ mã nguồn vào trong Docker
COPY . .

# 6. Mở cổng 80 (Render mặc định dùng cổng này hoặc bạn có thể tùy chỉnh)
EXPOSE 80

# 7. Lệnh để chạy ứng dụng
CMD ["python", "app/main.py"]