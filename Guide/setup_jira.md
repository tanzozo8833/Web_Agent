# 📋 Jira API Setup Guide

This document guides how to connect AI Agent with **Jira Software** to automatically manage Tickets and log work reports.

## 1. Overview (Overview)
* **Jira Integration** helps the AI Agent automate reporting. Every time AI edits code successfully, it will automatically create a Task on Jira with detailed logs and a link to the GitHub Branch.
* This helps project management (PM/Lead) track what the AI is doing without reading the code.

---

## 2. Implementation Steps (Steps)

### Step 1: Get Jira API Token
1. Access the Atlassian security management page: [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Click **Create API token**.
3. Set a label for the token (for example: `AI-Agent-Token`).
4. Click **Create** and **Copy** that code immediately.

&gt; **Extremely important note:** This is **NOT** your Jira login password. Please use this code as `JIRA_API_TOKEN`.

### Step 2: Determine Jira Server URL
1. The main URL is the address you use to access Jira on a web browser.
2. The format is usually: `https://company-name.atlassian.net`.
&gt; Your example: `https://hoangductan.atlassian.net`

### Step 3: Find Project Key (The core issue)
1. Go to Jira, select your project.
2. Look at the left menu -&gt; **Project settings** (Project settings).
3. Find the **Key** section. It is usually 2-4 uppercase characters (Example: `SCRUM`, `WEB`, `PROJ`).

&gt; **Note:** If you enter this Key incorrectly, the Bot will report the error `404: No project found`.

### Step 4: Check Issue Type
1. Ensure your project has a work type named **Task**.
2. If your project uses a different name (for example: `Task`), please correct it in the Python code at `issuetype: {&#39;name&#39;: &#39;Task&#39;}`.

---

## 3. Environment Check
Please ensure the following variables have been configured on Render/Local:

```env
JIRA_SERVER=[https://hoangductan733.atlassian.net](https://hoangductan733.atlassian.net)
JIRA_USER_EMAIL=your-email@gmail.com
JIRA_API_TOKEN=your-newly-created-api-token
JIRA_PROJECT_KEY=SCRUM (please double check your jira project key for accuracy)

```

## 4. Troubleshooting
1. 401 Unauthorized Error: Due to incorrect JIRA_USER_EMAIL or JIRA_API_TOKEN. Let's try creating a new Token.

2. 404 Project Not Found Error: Double check the JIRA_PROJECT_KEY. This Key must be all uppercase and exist in your Jira.

3. 403 Forbidden Error: Check if your account has permission to create Tickets in that Project.

4. Issue Type Error: If the project requires mandatory fields (Fields) such as Priority or Assignee, you need to add them to the create_issue function in the Python code.

*Developed by Tan - 2026*


[Back to Overall home page](../overall.md)