Run Project Markdown Template
# Project Operation Guide (Run Project)

This document guides how to start and maintain the AI Agent from a personal
computer (Local) to coordinate the entire Workflow.

## 1. Local Environment Preparation
Before running, please ensure your computer has installed:
* **Python 3.10+**: To run the main script `main.py`.
* **Git**: To execute code synchronization commands.
* **Node.js & npm**: (If you want to try OpenCode commands directly
on your machine).

---

## 2. Startup Steps (Running)

### Step 1: Install libraries
Open Terminal at the root directory of the project and run:
```bash
pip install -r requirements.txt
```

### Step 2: Configure .env file
Ensure the `.env` file on your Local has all the Keys (similar to the ones on
Render):
```env

SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
GITHUB_TOKEN=ghp_...
GOOGLE_API_KEY=AIza...
JIRA_SERVER=https://...
```

### Step 3: Execute Bot
Run the following command to activate the "control station":
```bash
python main.py
```
&gt; **Success indicator:** Terminal displays the text `⚡️ AI Agent is
connecting to Slack via Socket Mode...` and ` Health Check serve
is running...`.

---

## 3. Verification Process (Verification)

1. **Check connection:** Go to Slack, mention Bot: `@PyBot hello`.
If Bot responds, it means Socket Mode at Local is smooth.
2. **Test code editing:** Try commanding: `@PyBot change background color
of Sidebar to blue`.
3. **Monitor Terminal:** * See Bot create Git branch.
* See OpenCode execute file editing.
* See Push command and Merge to Main.

---

## 4. Important Notes when running Local
* **Maintain connection:** Do not close the Terminal running `main.py`.
If closed, the Bot will stop receiving commands from Slack.
* **Internet:** Local machine needs a stable network connection to maintain
WebSocket with Slack and push code to GitHub.
* **Conflict:** Avoid running `main.py` on multiple machines at the same time (e.g.,
running on Laptop and PC simultaneously) to prevent duplicate Jira Tickets
or Git branches.

---

## 5. Check results on Cloud
After the Bot reports &quot;Completed&quot; on Slack, please check:
1. **GitHub:** See if the `main` branch has a new Commit.
2. **Render:** See if your Web App automatically Deploys a new version
(Auto-deploy trigger).
3. **Jira:** See if a new Ticket has been created with full logs.

---

*Developed by Tan - 2026*

[Back to Overall home page](../overall.md)