const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());

// Phục vụ giao diện React
app.use(express.static(path.join(__dirname, 'build')));

app.get("/api/status", (req, res) => {
  res.json({ status: "Sidebar Backend is active" });
});

// Trả về index.html cho các route của React (phù hợp với React Router)
app.get("/*", (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Sidebar App running on port ${PORT}`);
});