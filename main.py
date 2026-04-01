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
    try:
        subprocess.run("git checkout main", shell=True)
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
        
        full_msg = f"{instruction}. Sau khi làm xong, hãy git add, commit 'fix: update' và push lên {branch_name}. {reporting_template}"
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

# --- SLACK: Xử lý Task chạy ngầm ---
def handle_task_in_background(event):
    channel_id = event.get("channel")
    raw_text = event.get("text")
    user_query = raw_text.split(">")[-1].strip()
    
    if not user_query: return

    # Gửi thông báo bắt đầu qua WebClient
    slack_web_client.chat_postMessage(channel=channel_id, text=f"🚀 *Socket Mode:* Đang xử lý yêu cầu: *{user_query}*...")
    
    res = run_opencode_workflow(user_query)

    if res.get("success"):
        try:
            jira_key = log_to_jira(user_query, res)
            slack_web_client.chat_postMessage(
                channel=channel_id, 
                text=f"✅ Hoàn tất! Đã tạo ticket *{jira_key}* và push lên nhánh *{res['branch']}*."
            )
        except Exception as e:
            slack_web_client.chat_postMessage(channel=channel_id, text=f"⚠️ Code đã sửa nhưng lỗi log Jira: {str(e)}")
    else:
        error_info = res.get("error") or res.get("stdout")
        slack_web_client.chat_postMessage(channel=channel_id, text=f"❌ OpenCode gặp lỗi: \n`{error_info[:500]}...`")

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
    # Khởi tạo SocketModeClient
    socket_client = SocketModeClient(
        app_token=slack_app_token,
        web_client=slack_web_client
    )

    # Đăng ký hàm xử lý sự kiện
    socket_client.socket_mode_request_listeners.append(process_slack_event)

    print("⚡️ AI Agent đang kết nối với Slack qua Socket Mode (WebSocket)...")
    
    # Kết nối và duy trì script (blocking)
    socket_client.connect()
    
    # Giữ script luôn chạy
    from threading import Event
    Event().wait()