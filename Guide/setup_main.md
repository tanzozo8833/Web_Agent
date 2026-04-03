Setup Main Checklist Template
# Setup Checklist (Setup Checklist)

This document provides an overview of all necessary requirements for the AI
Agent system to operate smoothly. Please make sure you have completed this list before
running the project.

## 1. Environment Variable List (Required Keys)
This is the &quot;circulatory system&quot; of the project. Please prepare these values and fill them in the `.env` file at
Local.

| Component | Environment Variable (Key) | Source |
| :--- | :--- | :--- |
| **Slack** | `SLACK_BOT_TOKEN` | [Slack API Settings](./docs/setup_slack.md) |
| **Slack** | `SLACK_APP_TOKEN` | [Slack API Settings](./docs/setup_slack.md) |
| **GitHub** | `GITHUB_TOKEN` | [GitHub Settings](./docs/setup_github.md) |
| **Google AI**| `GOOGLE_API_KEY` | [Google AI Studio](./docs/setup_opencode.md) |
| **Jira** | `JIRA_SERVER` | [Atlassian Cloud](./docs/setup_jira.md) |
| **Jira** | `JIRA_USER_EMAIL` | Jira registration email |
| **Jira** | `JIRA_API_TOKEN` | [Atlassian Security](./docs/setup_jira.md) |
| **Jira** | `JIRA_PROJECT_KEY` | [Jira Project Settings](./docs/setup_jira.md) |

---



## 2. Software Requirements
To run the project at Local, your computer needs to have pre-installed:
1. **Python 3.10+**: Main logic runner (`main.py`).
2. **Node.js (v18+)**: To install and run OpenCode CLI.
3. **Git**: To perform source code management operations.
4. **Docker**: (Optional) To test the environment just like on Cloud.

---

## 3. Setup Roadmap
Please follow this order to avoid conflicts:
1. **[Step 1: Slack](./docs/setup_slack.md)** - Communication channel setup.
2. **[Step 2: GitHub](./docs/setup_github.md)** - Grant source code access.
3. **[Step 3: OpenCode](./docs/setup_opencode.md)** - Install AI &quot;brain&quot;.
4. **[Step 4: Jira](./docs/setup_jira.md)** - Reporting system setup.
5. **[Step 5: Render](./docs/setup_render.md)** - Cloud infrastructure configuration.

---

## 4. Final Check before launch (Final Check)
* [ ] The `.env` file is located at the root directory of the project.

* [ ] Bot has been Invited into the corresponding Slack channel.
* [ ] GitHub Token has enough `repo` and `workflow` permissions.
* [ ] Project Key on Jira exactly matches the `JIRA_PROJECT_KEY` variable.

---

*Developed by Tan - 2026*

[Back to Overall home page](../overall.md)