const express = require("express");
const cors = require("cors");
const path = require("path"); // Cần thiết để xử lý đường dẫn file

const app = express();
app.use(cors());

// 1. Phục vụ các file tĩnh (CSS, JS, Image) từ thư mục 'build'
app.use(express.static(path.join(__dirname, 'build')));

// 2. API test (giữ lại nếu bạn muốn)
app.get("/api/health", (req, res) => {
  res.send("Backend is running smoothly");
});

// 3. QUAN TRỌNG: Mọi request không phải API sẽ trả về file index.html của React
app.get("/*", (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// 4. Sử dụng cổng từ biến môi trường (Render dùng 10000)
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Horizontal App running on port ${PORT}`);
});