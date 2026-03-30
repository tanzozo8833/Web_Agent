import os
import uuid
import subprocess
import threading
import shlex  # Thêm thư viện này
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(os.getenv("SLACK_SIGNING_SECRET"))

jira = JIRA(
    server=os.getenv("JIRA_SERVER"),
    basic_auth=(os.getenv("JIRA_USER_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)

def run_opencode_workflow(instruction):
    branch_name = f"ai-task-{uuid.uuid4().hex[:6]}"
    try:
        # 1. Reset và tạo nhánh mới
        subprocess.run("git checkout main", shell=True)
        subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)
        
        # 2. Làm sạch instruction (Xóa dấu ngoặc kép nếu user nhập vào)
        clean_instruction = instruction.replace('"', '').replace("'", "")
        
        # 3. Cấu hình lệnh Git bên trong (Dùng dấu ngoặc đơn cho commit message)
        git_steps = f"git add . && git commit -m 'fix: update' && git push origin {branch_name}"
        
        # 4. Gom lại thành instruction hoàn chỉnh
        full_msg = f"{clean_instruction}. Sau đó chạy: {git_steps}"
        
        # 5. SỬA LẠI CÁCH BỌC CÂU LỆNH (Dùng f-string với dấu ngoặc đơn bên ngoài)
        # Ép dùng model gemini-2.0-flash (hoặc tên model bạn đã check)
        model_name = "google/gemini-2.5-flash"
        
        # Cách này an toàn nhất trên Windows: bọc tin nhắn trong dấu ngoặc kép " "
        command = f'opencode run "{full_msg}" -m {model_name} --yes'
        
        print(f"🛠 Đang gọi lệnh: {command}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            env=os.environ,
            encoding="utf-8",
            errors="replace"
        )
        
        # Kiểm tra thực tế xem có chữ "Options:" (Help menu) không
        if "Options:" in result.stdout and "run" in result.stdout:
             # Nếu lỗi, thử in ra stdout để debug
             print(f"DEBUG OUTPUT: {result.stdout}")
             return {"success": False, "error": "Cấu pháp lệnh vẫn bị sai. Hãy thử ra lệnh bằng tiếng Anh không dấu.", "branch": branch_name}

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout if result.stdout else result.stderr,
            "branch": branch_name
        }
    except Exception as e:
        return {"success": False, "error": str(e), "branch": branch_name}

# Các hàm log_to_jira, handle_task_in_background giữ nguyên như cũ
# ... (Phần còn lại của code bạn giữ nguyên)

def log_to_jira(instruction, res):
    project_key = os.getenv("JIRA_PROJECT_KEY")
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
    channel_id = event.get("channel")
    raw_text = event.get("text")
    user_query = raw_text.split(">")[-1].strip()
    
    if not user_query: return

    slack_client.chat_postMessage(channel=channel_id, text=f"🚀 Đang bắt đầu xử lý: *{user_query}*...")
    res = run_opencode_workflow(user_query)

    if res.get("success"):
        try:
            jira_key = log_to_jira(user_query, res)
            slack_client.chat_postMessage(channel=channel_id, text=f"✅ Hoàn tất! Ticket: *{jira_key}*, Nhánh: *{res['branch']}*.")
        except Exception as e:
            slack_client.chat_postMessage(channel=channel_id, text=f"⚠️ Lỗi log Jira: {str(e)}")
    else:
        slack_client.chat_postMessage(channel=channel_id, text=f"❌ OpenCode gặp lỗi: \n`{res.get('error') or res.get('stdout')}`")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return jsonify({"status": "invalid"}), 403
    data = request.json
    if "challenge" in data: return jsonify({"challenge": data["challenge"]})
    event = data.get("event", {})
    if event.get("type") == "app_mention" and event.get("bot_id") is None:
        thread = threading.Thread(target=handle_task_in_background, args=(event,))
        thread.start()
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5001)