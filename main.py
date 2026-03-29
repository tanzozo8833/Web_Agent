import os
import uuid
import subprocess
import threading
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from jira import JIRA
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()

app = Flask(__name__)

# --- Cấu hình Clients ---
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(os.getenv("SLACK_SIGNING_SECRET"))

jira = JIRA(
    server=os.getenv("JIRA_SERVER"),
    basic_auth=(os.getenv("JIRA_USER_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)

def run_opencode_workflow(instruction):
    branch_name = f"ai-task-{uuid.uuid4().hex[:6]}"
    try:
        # 1. Chuyển nhánh
        subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)
        
        # 2. Chuẩn bị instruction cực kỳ rõ ràng
        # Ép OpenCode phải làm xong các bước git cuối cùng
        full_msg = f"{instruction}. Sau đó hãy chạy 'git add .', 'git commit -m \"fix: {instruction[:30]}\"' và 'git push origin {branch_name}'."
        
        # SỬA LẠI CÁCH GỌI: Dùng list để tránh lỗi dấu ngoặc kép trên Windows/Linux
        # Lệnh: opencode run "nội dung"
        command = ["opencode", "run", full_msg]
        
        print(f"🛠 Đang gọi: {' '.join(command)}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            env=os.environ,
            encoding="utf-8", # THÊM DÒNG NÀY ĐỂ FIX LỖI UNICODE
            errors="ignore"    # THÊM DÒNG NÀY ĐỂ BỎ QUA KÝ TỰ LỖI
        )
        
        # Nếu vẫn hiện Help (có chữ "Options:"), nghĩa là lệnh chưa vào được thread xử lý
        if "Options:" in result.stdout and result.returncode == 0:
            return {"success": False, "error": "OpenCode không nhận diện được tin nhắn. Hãy kiểm tra lại cú pháp lệnh 'run'.", "branch": branch_name}

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout if result.stdout else result.stderr,
            "branch": branch_name
        }
    except Exception as e:
        return {"success": False, "error": str(e), "branch": branch_name}

def log_to_jira(instruction, res):
    """Tạo ticket Jira và ghi log"""
    project_key = os.getenv("JIRA_PROJECT_KEY")
    # Thay link repo thật của bạn ở đây
    repo_url = "https://github.com/tanzozo8833/web_agent" 
    branch_url = f"{repo_url}/tree/{res['branch']}"

    issue_dict = {
        'project': project_key,
        'summary': f'[AI-Agent] {instruction[:50]}',
        'description': f'Yêu cầu: {instruction}\nGitHub Branch: {branch_url}',
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    
    comment = (
        f"✅ *AI đã sửa code xong!*\n"
        f"* *Nhánh:* `{res['branch']}`\n"
        f"* *Link:* {branch_url}\n"
        f"* *Log:* \n{{code}}{res.get('stdout', '')[:800]}{{code}}"
    )
    jira.add_comment(new_issue, comment)
    return new_issue.key

def handle_task_in_background(event):
    """Hàm xử lý chính chạy ngầm để không làm Slack bị Timeout"""
    channel_id = event.get("channel")
    raw_text = event.get("text")
    # Lấy toàn bộ nội dung sau khi mention bot
    user_query = raw_text.split(">")[-1].strip()
    
    if not user_query:
        return

    # Thông báo cho người dùng
    slack_client.chat_postMessage(channel=channel_id, text=f"🚀 Đang bắt đầu xử lý: *{user_query}*...")

    # Chạy OpenCode
    res = run_opencode_workflow(user_query)

    if res.get("success"):
        # Log Jira
        try:
            jira_key = log_to_jira(user_query, res)
            slack_client.chat_postMessage(
                channel=channel_id, 
                text=f"✅ Hoàn tất! Đã tạo ticket *{jira_key}* và push lên nhánh *{res['branch']}*."
            )
        except Exception as e:
            slack_client.chat_postMessage(channel=channel_id, text=f"⚠️ Code đã sửa nhưng lỗi log Jira: {str(e)}")
    else:
        error_info = res.get("error") or res.get("stdout")
        slack_client.chat_postMessage(channel=channel_id, text=f"❌ OpenCode gặp lỗi: \n`{error_info}`")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    # Xác thực request
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return jsonify({"status": "invalid"}), 403

    data = request.json
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    # Kiểm tra nếu là mention và KHÔNG phải là tin nhắn từ chính bot (tránh loop)
    if event.get("type") == "app_mention" and event.get("bot_id") is None:
        # CHẠY NGẦM: Trả lời Slack 200 ngay lập tức, xử lý tính sau
        thread = threading.Thread(target=handle_task_in_background, args=(event,))
        thread.start()
        
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5001)