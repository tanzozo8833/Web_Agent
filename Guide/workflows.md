Workflows Markdown Template
# Workflows 

This document details how components (Slack, AI, GitHub,
Jira) coordinate with each other to automate a code editing request.

## 1. High-Level Diagram
Below is the data flow going through the system:

```
[User] --( Slack Mention )--&gt; [Python Bot]
                                          |
                                   ( Call OpenCode AI )
                                          |
(Trigger Render) &lt;-- [GitHub Repo] &lt;--( Push/Merge )--- [OpenCode (Gemini 3)]
(Auto-Deploy)            |                                   |
    |               ( Link Branch )                    ( Return Log )
[Web App Live]           |                                   |
                         +------&gt; [Jira Software] &lt;----------+
                                        |
                                ( Create Task Ticket )
```

---

## 2. Detailed 7 Operational Steps

### Step 1: Trigger
* The user types: `@PyBot change Sidebar button color
to black`.
* Slack sends the event via **Socket Mode** (WebSocket) to the Python Bot
running on Render.

### Step 2: Initialization
* The Python Bot extracts the request content (`instruction`).
* The Bot automatically creates a new Git branch with a random name: `ai-task-
xxxxxx`.

### Step 3: AI Action
* The Bot calls the `opencode run` command alongside the user&#39;s request.
* **Gemini 3 Flash** scans the entire project directory to find the right CSS/JS file
to edit.
* AI directly applies source code edits inside the Render Container.

### Step 4: Git Version Flow
* AI executes commands: `git add`, `git commit`, and `git push` to branch
`ai-task-xxxxxx`.
* **GitHub Token** is used to authenticate Write permission.

### Step 5: Auto Merge
* After AI reports success, Python Bot executes a sequence of commands:
1. `git checkout main`
2. `git pull origin main`
3. `git merge ai-task-xxxxxx`
4. `git push origin main`
* The official code is updated on the Main branch of the project.

### Step 6: Jira Logging
* The Bot gets results (Stdout/Stderr) from OpenCode.
* Uses **Jira API** to create a new Issue (Task) in the Project.
* Attaches the GitHub branch link and the entire Terminal Log into the Comment of
the Ticket.

### Step 7: Notification
* The Bot sends a confirmation message to Slack: `✅ Completed! Created ticket
SCRUM-XX and pushed to Main`.

---

## 3. Processing Status Table

| Status | System Action | Slack Return Result |
| :--- | :--- | :--- |
| **Start** | Receive Socket Event | "⏳ Processing: [Request]..." |
| **Running** | AI edit file & Git push | (Silently waiting) |
| **Success** | Merge Main & Create Jira | "✅ Completed! Created ticket..." |
| **Failure** | Catch Exception / Error Log | "❌ OpenCode failed: [Error code]" |

---

## 4. Safety Mechanism
* **Sub-branch:** AI always works on the `ai-task-` branch first to
avoid breaking Main code if there&#39;s an error.

* **Safe Directory:** Docker is configured with `safe.directory` so Git
does not block actions from unknown Users.
* **Merge Logic:** Python only executes Merge if and only if
OpenCode returns `exit code 0`.

---

*Developed by Tan - 2026*

[Back to Overall home page](../overall.md)