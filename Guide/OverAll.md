AI Agent Overall Markdown Template
# AI AGENT WORKFLOW - SLACK, JIRA, OPENCODE INTEGRATION

## 1. Purpose
* This project builds an **AI DevOps Agent** that helps automate the
code editing and task management process.
* Instead of doing it manually, the system will receive requests from Slack, use
AI (OpenCode/Gemini) to edit the source code, then automatically
Push/Merge to GitHub and log reports to Jira.

---


## 2. Contents
### 2.1 Setup
* [2.1 Slack Socket Mode Configuration](.././Guide/setup_slack.md) - How
to create an App and get Bot/App Tokens.
* [2.2 Jira API Configuration](.././Guide/setup_jira.md) - Guide to get
API Token and determine Project Key.
* [2.3 OpenCode Agent Configuration](.././Guide/setup_opencode.md) - Install
OpenCode-AI and configure the Gemini model.
* [2.4 Render.com Configuration](.././Guide/setup_render.md) - Setup
Docker Web Service and environment variables.
* [2.5 GitHub Token Configuration](.././Guide/setup_github.md) - Grant
Write permission for Bot to Push and Merge code.


### 2.2 Workflows

* [Workflows](.././Guide/workflows.md) - Detailed data flow diagram
from Slack to Merging into the Main branch.

### 2.3 Operation Guide
* [How to run](.././Guide/run_project.md) - How to run Local and check
Logs on Production.

---

## 3. Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Logic Bot** | Python 3.10 | Coordinate Socket Mode and handle Git/Jira |
| **AI Agent** | OpenCode (Gemini 3 Flash) | Understand context and directly edit files |
| **Infrastructure** | Docker | Package stable runtime environment
|
| **Hosting** | Render.com | Maintain 24/7 Service and Health Check
|
| **Task Tracking** | Jira Software | Retain history logs and manage tickets automatically |


---

## 4. Environment Variables

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
GITHUB_TOKEN=ghp_your_github_token
GOOGLE_API_KEY=your_gemini_api_key
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_USER_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=YOUR_KEY
```

---

*Project developed by Tan - HUST &amp; FPT Corporation - 2026*