import os
import requests
from dotenv import load_dotenv

# 1. Load .env
load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

if not API_KEY or not ENDPOINT:
    print("❌ Thiếu AZURE_OPENAI_API_KEY hoặc AZURE_OPENAI_ENDPOINT")
    exit()

# 2. Gọi API lấy danh sách deployments
url = f"{ENDPOINT}/openai/deployments?api-version={API_VERSION}"

headers = {
    "api-key": API_KEY
}

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Lỗi gọi API: {response.status_code}")
        print(response.text)
        exit()

    data = response.json()

    deployments = data.get("data", [])

    if not deployments:
        print("⚠️ Không có deployment nào → Bạn chưa deploy model nào.")
        exit()

    print("✅ Danh sách deployments:\n")

    found_gpt4o_mini = False

    for d in deployments:
        name = d.get("id")
        model = d.get("model")

        print(f"- Deployment name: {name}")
        print(f"  Model: {model}")
        print()

        if name == "gpt-4o-mini":
            found_gpt4o_mini = True

    # 3. Check lỗi của bạn
    print("🔎 Kiểm tra cấu hình hiện tại:\n")

    if found_gpt4o_mini:
        print("✅ Bạn CÓ deployment tên 'gpt-4o-mini' → dùng được trực tiếp.")
    else:
        print("❌ KHÔNG có deployment tên 'gpt-4o-mini'")
        print("👉 Bạn đang dùng sai model name trong OpenClaw!")
        print("👉 Hãy dùng 1 trong các deployment name ở trên.")

except Exception as e:
    print("❌ Exception:", str(e))