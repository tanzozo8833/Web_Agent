import os
import uuid
import subprocess
import threading
from dotenv import load_dotenv

# Slack SDK cho Socket Mode
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

# Jira SDK
from jira import JIRA
from flask import Flask # Nhớ import thêm Flask

flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "AI Agent is Online!", 200

def run_flask():
    # Render yêu cầu lắng nghe port 10000
    flask_app.run(host='0.0.0.0', port=10000)

# Tải biến môi trường
load_dotenv()

# --- Cấu hình Clients ---
# Token xoxb-... dùng để gửi tin nhắn
slack_web_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
# Token xapp-... dùng để duy trì kết nối WebSocket
slack_app_token = os.getenv("SLACK_APP_TOKEN")

jira = JIRA(
    server=os.getenv("JIRA_SERVER"),
    basic_auth=(os.getenv("JIRA_USER_EMAIL"), os.getenv("JIRA_API_TOKEN"))
)

# --- WORKFLOW: Chạy OpenCode ---
def run_opencode_workflow(instruction):
    branch_name = f"ai-task-{uuid.uuid4().hex[:6]}"
    github_token = os.getenv("GITHUB_TOKEN")
    repo_url = "github.com/tanzozo8833/Web_Agent.git" # Sửa đúng repo của ông
    remote_url = f"https://{github_token}@{repo_url}"

    try:
        # Kiểm tra xem folder .git có tồn tại không, nếu không thì init mới
        if not os.path.exists(".git"):
            print("🚀 Đang khởi tạo Repo Git mới trong Container...")
            subprocess.run("git init", shell=True)
            subprocess.run(f"git remote add origin {remote_url}", shell=True)
        else:
            subprocess.run(f"git remote set-url origin {remote_url}", shell=True)

        # Cấu hình lại danh tính cho chắc chắn
        subprocess.run('git config user.email "bot-agent@render.com"', shell=True)
        subprocess.run('git config user.name "Tan-AI-Agent"', shell=True)
        subprocess.run("git config --global --add safe.directory /app", shell=True)

        # Kéo code mới nhất về để đồng bộ
        print("📡 Đang kéo code từ GitHub...")
        subprocess.run("git fetch origin main --depth=1", shell=True)
        subprocess.run("git reset --hard origin/main", shell=True) # Ép local giống hệt GitHub
        subprocess.run("git checkout main", shell=True)
        
        # Bây giờ mới tạo nhánh mới để sửa code
        print(f"🌿 Tạo nhánh mới: {branch_name}")
        subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)
        # Thêm yêu cầu OpenCode báo cáo chi tiết ở cuối
        reporting_template = (
            "\n\nSau khi hoàn thành, hãy in một đoạn tóm tắt cuối cùng theo đúng định dạng sau:\n"
            "[REPORT]\n"
            "App: <tên app bị ảnh hưởng>\n"
            "Action: <hành động chính ví dụ: Thêm giao diện, Sửa màu...>\n"
            "Details: <chi tiết các file đã sửa hoặc tạo mới>\n"
            "Status: <Trạng thái hoàn thành>\n"
            "[/REPORT]"
        )
        
        full_msg = f"{instruction}. Sau khi làm xong, hãy git add, commit 'fix: update' và và git push origin {branch_name}. {reporting_template}"
        model_id = "google/gemini-3-flash-preview" 

        command = f'opencode run -m {model_id} "{full_msg}"'
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, shell=True, 
            encoding="utf-8", 
            errors="replace")
        
        # Trích xuất thông tin từ [REPORT] ... [/REPORT]
        stdout_content = result.stdout
        print("STDOUT của OpenCode:", result.stdout)
        print("STDERR của OpenCode:", result.stderr)
        report_data = {}
        if "[REPORT]" in stdout_content:
            report_section = stdout_content.split("[REPORT]")[1].split("[/REPORT]")[0].strip()
            for line in report_section.split('\n'):
                if ":" in line:
                    key, value = line.split(":", 1)
                    report_data[key.strip().lower()] = value.strip()

        return {
            "success": result.returncode == 0 and "Options:" not in stdout_content,
            "stdout": stdout_content,
            "branch": branch_name,
            "report": report_data # Chứa thông tin Agent tự phân tích
        }
    except Exception as e:
        return {"success": False, "error": str(e), "branch": branch_name}

# --- JIRA: Ghi Log Ticket ---
def log_to_jira(instruction, res):
    project_key = os.getenv("JIRA_PROJECT_KEY")
    repo_url = "https://github.com/tanzozo8833/web_agent" 
    branch_url = f"{repo_url}/tree/{res['branch']}"
    
    # Lấy dữ liệu từ báo cáo của Agent, nếu không có thì để mặc định
    report = res.get('report', {})
    app_name = report.get('app', 'N/A').upper()
    action = report.get('action', 'Update Code')
    details = report.get('details', 'No details provided')
    status = report.get('status', 'Completed')

    # 1. Tạo Issue chính
    issue_dict = {
        'project': project_key,
        'summary': f'[AI-AGENT][{app_name}] {action}',
        'description': (
            f"h1. 🤖 AI Agent Report\n"
            f"* *Yêu cầu ban đầu:* {instruction}\n"
            f"* *App:* {app_name}\n"
            f"* *Hành động:* {action}\n"
            f"* *Trạng thái:* {status}\n"
            f"* *GitHub Branch:* [{res['branch']}|{branch_url}]"
        ),
        'issuetype': {'name': 'Task'},
        'labels': ['ai-agent', f'app-{app_name.lower()}']
    }
    
    new_issue = jira.create_issue(fields=issue_dict)
    
    # 2. Tạo Comment log chi tiết hơn
    log_content = (
        f"h3. 📝 Chi tiết thay đổi\n"
        f"{details}\n\n"
        f"h3. 💻 Terminal Full Log\n"
        f"{{code:bash}}\n{res.get('stdout', '')[-1500:]}\n{{code}}" # Lấy 1500 ký tự cuối của log (thường chứa kết quả)
    )
    
    jira.add_comment(new_issue, log_content)
    return new_issue.key

def handle_task_in_background(event):
    channel_id = event.get("channel")
    raw_text = event.get("text")
    
    try:
        user_query = raw_text.split(">")[-1].strip()
    except:
        user_query = raw_text.strip()
    
    if not user_query: return

    slack_web_client.chat_postMessage(channel=channel_id, text=f"🚀 *Socket Mode:* Đang xử lý: *{user_query}*...")
    
    try:
        # Chạy logic chính
        res = run_opencode_workflow(user_query)
        
        print(f"--- DEBUG RESULT ---")
        print(res)
        print(f"--------------------")

        if res.get("success"):
            try:
                jira_key = log_to_jira(user_query, res)
                msg = f"✅ Hoàn tất! Đã tạo ticket *{jira_key}* và push lên nhánh *{res.get('branch')}*."
                slack_web_client.chat_postMessage(channel=channel_id, text=msg)
            except Exception as e_jira:
                slack_web_client.chat_postMessage(channel=channel_id, text=f"⚠️ Sửa code OK nhưng lỗi Jira: `{str(e_jira)}`")
        else:
            # Báo lỗi chi tiết lên Slack
            stderr = res.get("stderr", "")
            error_msg = res.get("error", "")
            stdout = res.get("stdout", "")
            
            full_error = "❌ *OpenCode thất bại:*\n"
            if error_msg: full_error += f"*Lỗi:* `{error_msg}`\n"
            if stderr: full_error += f"*Stderr:*\n{stderr}\n"
            if stdout: full_error += f"*Stdout:*\n{stdout}\n"
            slack_web_client.chat_postMessage(channel=channel_id, text=full_error)
    except Exception as e:
        slack_web_client.chat_postMessage(channel=channel_id, text=f"❌ *Lỗi hệ thống:* `{str(e)}`")

# --- SOCKET MODE LISTENER ---
def process_slack_event(client: SocketModeClient, req: SocketModeRequest):
    # Xác nhận với Slack đã nhận được request (để Slack không gửi lại)
    response = SocketModeResponse(envelope_id=req.envelope_id)
    client.send_socket_mode_response(response)

    # Nếu là sự kiện Events API (như app_mention)
    if req.type == "events_api":
        event = req.payload.get("event", {})
        # Lọc đúng sự kiện mention và không phải bot tự chat với chính mình
        if event.get("type") == "app_mention" and event.get("bot_id") is None:
            # Tạo thread mới để không làm tắc nghẽn WebSocket
            thread = threading.Thread(target=handle_task_in_background, args=(event,))
            thread.start()

# --- MAIN ---
if __name__ == "__main__":
    # 1. Chạy Flask Health Check ở một luồng riêng
    threading.Thread(target=run_flask, daemon=True).start()

    # 2. Khởi tạo và chạy Socket Mode Client
    socket_client = SocketModeClient(
        app_token=slack_app_token,
        web_client=slack_web_client
    )
    socket_client.socket_mode_request_listeners.append(process_slack_event)

    print("⚡️ AI Agent đang kết nối với Slack qua Socket Mode (WebSocket)...")
    print("🏥 Health Check server đang chạy tại port 10000...")
    
    socket_client.connect()
    
    from threading import Event
    Event().wait()