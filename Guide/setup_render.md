Setup Render Markdown Template
# Render.com Deployment Guide

This document guides how to set up the **Web Service** on Render to
operate the AI Agent using Docker, ensuring the system runs stably 24/7.

## 1. Overview (Overview)
* **Render.com** is used to host the Python Bot running in
**Socket Mode**.
* We use **Docker** to create a &quot;Hybrid&quot; environment (combining both
Python for Bot and Node.js for OpenCode).
* **Default Port:** Render requires the application to listen on Port
`10000`.

---


## 2. Dockerfile Configuration (Heart of the system)
To avoid missing `npm` or `opencode` command errors, your `Dockerfile`
needs the following structure:

```dockerfile
# 1. Use Python as base
FROM python:3.10-slim

# 2. Install Node.js and Git (Mandatory)
RUN apt-get update && apt-get install -y \ curl \


# 3. Install OpenCode AI globally
RUN npm install -g opencode-ai

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# 4. Run application
CMD [python main.py]
```

&gt; **Syntax:** Pay attention to the `\` to concatenate commands in the Dockerfile.

---

## 3. Setup steps on Render Dashboard
1. Access [dashboard.render.com](https://dashboard.render.com/).
2. Click **New +** -&gt; Select **Web Service**.
3. Connect with your GitHub Repo `Web_Agent`.
4. **Runtime:** Select `Docker`.
5. **Plan:** Select `Free` (or Starter if more RAM is needed).

---

## 4. Environment Variables Configuration (Environment Variables)
Go to **Settings &gt; Environment**, add all the following Keys:

| Key | Value Example |
| :--- | :--- |
| `SLACK_BOT_TOKEN` | `xoxb-xxx...` |
| `SLACK_APP_TOKEN` | `xapp-xxx...` |
| `GITHUB_TOKEN` | `ghp_xxx...` |
| `GOOGLE_API_KEY` | `AIzaSy...` |
| `JIRA_SERVER` | `https://xxx.atlassian.net` |
| `JIRA_USER_EMAIL` | `email@gmail.com` |
| `JIRA_API_TOKEN` | `mã_token_jira` |
| `JIRA_PROJECT_KEY` | `SCRUM` |

---

## 5. Check Health Check
* In the Python code, we ran a parallel Flask app at
Port `10000`.
* Render will automatically ping your URL. If it sees the word **&quot;AI Agent
is Online!&quot;**, it means the Bot is ready to receive commands from Slack.

---

## 6. Troubleshooting (Troubleshooting)
* **Out of Memory Error (137):** The Free plan only has 512MB RAM. If
OpenCode scans too many files, Render will &quot;kill&quot; the process.
* **Port 10000 Error:** Ensure the Python code has the snippet
`app.run(host=0.0.0.0, port=10000)`.

* **Build Fail:** Carefully review all logs in the **Events** tab to know which step
in the Dockerfile failed.

---
*Developed by Tan - 2026*

[Back to Overall home page](../overall.md)