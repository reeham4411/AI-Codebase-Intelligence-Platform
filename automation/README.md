# Automation Workflows (n8n)

This folder contains n8n workflow configurations for automating the AI Codebase Intelligence Platform.

## Workflows

### 1. `github_auto_index.json` — Auto-Index on GitHub Push

Automatically re-indexes a repository whenever code is pushed to the main branch.

**Flow:**

```
GitHub Push Webhook → Check if Main Branch → Clone & Re-Index → Notify Slack
```

**Setup:**

1. Import `github_auto_index.json` into your n8n instance
2. Activate the workflow — it creates a webhook URL
3. Go to your GitHub repo → Settings → Webhooks → Add webhook
4. Set the Payload URL to: `https://your-n8n-domain/webhook/github-webhook`
5. Set Content type to `application/json`
6. Select "Just the push event"
7. (Optional) Configure Slack credentials in n8n for notifications

---

### 2. `slack_ai_assistant.json` — Slack Code Assistant

Lets developers ask questions about the codebase directly from Slack using a slash command.

**Flow:**

```
/ask <question> → n8n Webhook → AI Backend → Formatted Slack Response
```

**Setup:**

1. Import `slack_ai_assistant.json` into your n8n instance
2. Activate the workflow — it creates a webhook URL
3. Go to [api.slack.com/apps](https://api.slack.com/apps) → Create New App
4. Add a Slash Command:
   - Command: `/ask`
   - Request URL: `https://your-n8n-domain/webhook/slack-command`
   - Description: "Ask AI about the codebase"
5. Install the app to your Slack workspace

---

## Requirements

- **n8n** — Self-hosted or cloud ([n8n.io](https://n8n.io))
- **Backend API** running at `http://localhost:8000` (or update the URLs in the workflows)
- **GitHub** webhooks (for auto-indexing)
- **Slack** app (for the assistant)

## Alternative: Direct Slack Integration

If you don't want to use n8n, the backend also has built-in Slack endpoints:

- `POST /api/slack/events` — For Slack Event Subscriptions (app mentions)
- `POST /api/slack/ask` — For Slack Slash Commands

Set `SLACK_SIGNING_SECRET` in your `.env` file for request verification.
