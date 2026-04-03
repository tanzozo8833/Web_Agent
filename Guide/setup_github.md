Setup GitHub Documentation Template
# GitHub Token Setup Guide

This document guides how to grant permissions for the AI Agent so it can automatically
create branches (Branch), push code (Push), and merge source code (Merge) into
your project.

## 1. Overview (Overview)
* By default, Render or Python Bot does not have permission to interfere with
your Repo.
* We use a **Personal Access Token (PAT)** as a &quot;master key&quot;
to identify the Bot as a member with Write access
in the Repo.

---


## 2. Implementation Steps (Steps)

### Step 1: Create Personal Access Token (Classic)
1. Access your GitHub -&gt; **Settings** (Personal settings).
2. Scroll to the bottom of the left menu, select **Developer settings**.
3. Select **Personal access tokens** -&gt; **Tokens (classic)**.
4. Click **Generate new token** -&gt; Select **Generate new token
(classic)**.

### Step 2: Select Scopes for Bot
For the Bot to run smoothly, you **MUST** check the following boxes:
* [x] **repo**: Full control of repositories (to Push code).

* [x] **workflow**: Allow Bot to update GitHub
Actions configuration files (if any).
* [x] **admin:repo_hook**: So the Bot can manage hook connections
if necessary.
* [x] **delete_repo**: (Optional) If you want the Bot to have permission to delete the branch
after Merging.

### Step 3: Storage and Security
1. Click **Generate token**.
2. **Immediately copy** the code starting with `ghp_...`.

&gt; **Note:** GitHub only displays this code once. If you forget,
you will have to create a new one.

---

## 3. Environment variable configuration (Environment Check)
Paste the copied code into the environment variable on Render or in the
`.env` file:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 4. How the Bot uses the Token in Code
In `main.py`, we embed the Token into the URL so Git won't ask for a password:

```python

repo_url = github.com/tanzozo8833/Web_Agent.git
remote_url = https://{github_token}@{repo_url}
# after that run this command:
# git remote set-url origin {remote_url}
```

---

## 5. Troubleshooting (Troubleshooting)
* **Error 403 Forbidden:** Because your Token didn't check the `repo` box (Write
permission). Please go back to Step 2 and add it.
* **Expired Token Error:** GitHub usually defaults the Token to expire after
30 days. Please select `No expiration` if you want the Bot to run forever
(but please be careful with security).
* **Main branch blocked:** If you enabled &quot;Branch Protection&quot; on
GitHub, the Bot may be blocked from Merging directly. Please add
this Token to the &quot;Allow force push&quot; or &quot;Bypass
protections&quot; list.

---
*Developed by Tan - 2026*

[Back to Overall home page](../overall.md)