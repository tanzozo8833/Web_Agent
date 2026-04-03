# 💬 Slack Socket Mode Setup Guide

This document guides how to create and configure a Slack App to connect with the AI Agent via **Socket Mode**.

## 1. Overview (Overview)
* **Socket Mode** allows the Bot to receive events from Slack via WebSocket without configuring a Public URL (Webhook).
* This is extremely useful when running on **Render.com** or **Local** because there is no need to open a Port for incoming requests.

---

## 2. Implementation Steps (Steps)

### Step 1: Create Slack App
1. Access [Slack API: Applications](https://api.slack.com/apps).
2. Click **Create New App** -&gt; Select **From scratch**.
3. Name the App (for example: `PyBot-AI`) and select your Workspace.

### Step 2: Enable Socket Mode &amp; Get App Token
1. In the left menu, find **Settings &gt; Socket Mode**.
2. Toggle the switch to **Enable Socket Mode**.
3. A panel appears asking you to name the Token (e.g., `SocketToken`).
4. Click **Generate** -&gt; Copy the string starting with `xapp-...`.

&gt; **Note:** This is your `SLACK_APP_TOKEN` variable.

### Step 3: Configure Scopes (Permissions)
1. Go to **Features &gt; OAuth &amp; Permissions**.
2. Scroll down to **Scopes &gt; Bot Token Scopes**.
3. Click **Add an OAuth Scope** and add the following permissions:
    * `app_mentions:read`: So the Bot can hear when you `@mention`.
    * `chat:write`: So the Bot has permission to send reply messages.
    * `files:write`: (Optional) If you want the Bot to send log files.

### Step 4: Enable Event Subscriptions
1. Go to **Features &gt; Event Subscriptions**.
2. Toggle the switch to **On**.
3. Scroll down to **Subscribe to bot events**, click **Add Bot User Event**.
4. Select event: `app_mention`.
5. Click **Save Changes**.

### Step 5: Install App &amp; Get Bot Token
1. Go to **Settings &gt; Install App**.
2. Click **Install to Workspace** and select **Allow**.
3. After installation is complete, you will see exactly the **Bot User OAuth Token** (starting with `xoxb-...`).

&gt; **Note:** This is your `SLACK_BOT_TOKEN` variable.

---

## 3. Environment Check
After completing, you must have both of the following Tokens in your `.env` file or Render:

```env
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-1-xxxxxxxxxxxx-xxxxxxxxxxxxx
```
## 4. Troubleshooting
1. Bot does not reply: Check if you have invited the Bot to the Channel (Type /invite @bot_name in Slack).

2. Ratelimited error: Ensure you do not send too many consecutive requests in a short time.

3. Socket Mode disconnect: Verify if SLACK_APP_TOKEN is exactly the xapp type (many people confuse it with the Bot&#39;s Token).

4. Each Socket API can only be used for 1 service.

*Developed by Tan - 2026*


[Back to Overall home page](../overall.md)