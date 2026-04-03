Setup OpenCode Markdown Template
# OpenCode AI Agent Setup Guide

This document guides how to install and configure **OpenCode-AI**,
a tool that uses the Gemini model to automatically analyze and edit source
code.

## 1. Overview (Overview)
* **OpenCode-AI** is a powerful CLI tool that allows AI to access
the Project Context, understand the file structure and execute
changes (Edit/Create/Delete) based on requests from Slack.
* In this project, OpenCode acts as the &quot;executor arm&quot; of
the AI Agent.

---


## 2. Implementation Steps (Steps)

### Step 1: Install Node.js (Prerequisite)
* OpenCode runs on the Node.js platform. Ensure the environment (Local
or Docker) has Node.js version 18 or higher.
* Check with the command: `node -v` and `npm -v`.

### Step 2: Install OpenCode CLI
Open Terminal and run the Global installation command:
```bash

npm install -g opencode-ai
```
&gt; **Note for Render/Docker:** You must install Node.js into the Dockerfile BEFORE
running the `npm install` command.

### Step 3: Get Google API Key (Gemini)
1. Access [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key**.
3. Create a new API Key and copy this string code.

&gt; **Note:** This API Key is the `GOOGLE_API_KEY` environment variable.

### Step 4: Configure Model in Project
In the Python code (`main.py`), we use the model:
* `google/gemini-3-flash-preview`
* OpenCode will use the Key from the environment to automatically authenticate with Google.

---

## 3. How AI Agent calls OpenCode (Workflow)
The `run_opencode_workflow` function in `main.py` executes the following command via
`subprocess`:

```python
command = opencode run -m {model_id} {full_msg}
```

---

## 4. Environment Check
Please make sure the following variable has been configured:

```env
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxx
```

---

## 5. Troubleshooting (Troubleshooting)
* **Error `npm: not found`:** Occurs when the Dockerfile hasn&#39;t installed Node.js.
* **Error `Invalid API Key`:** Check if `GOOGLE_API_KEY` has
extra whitespace.
* **Quota Error (429):** If using the Free tier of Gemini, you might be
limited by the number of requests per minute (RPM).

---
*Project implemented by Tan - 2026*
[Back to Overall home page](../overall.md)