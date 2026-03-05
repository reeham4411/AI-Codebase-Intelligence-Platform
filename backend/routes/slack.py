import os
import json
import hmac
import hashlib
import time

from fastapi import APIRouter, Request, HTTPException
from services.rag_service import answer_question

router = APIRouter(prefix="/api", tags=["Slack"])

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")


def verify_slack_signature(body: bytes, timestamp: str, signature: str) -> bool:
    """Verify that the request actually came from Slack."""
    if not SLACK_SIGNING_SECRET:
        return True  # Skip verification if no secret set (dev mode)

    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False  # Request too old

    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    computed = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed, signature)


@router.post("/slack/events")
async def slack_events(request: Request):
    """
    Handle Slack events (URL verification + message events).
    Configure this URL in your Slack App: https://your-domain/api/slack/events
    """
    body = await request.body()
    data = json.loads(body)

    # Slack URL verification challenge
    if data.get("type") == "url_verification":
        return {"challenge": data["challenge"]}

    # Verify Slack signature
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")

    if SLACK_SIGNING_SECRET and not verify_slack_signature(body, timestamp, signature):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")

    # Handle message events
    event = data.get("event", {})

    if event.get("type") == "app_mention":
        question = event.get("text", "").strip()
        # Remove bot mention from the question
        if "<@" in question:
            question = question.split(">", 1)[-1].strip()

        if question:
            answer, sources = answer_question(question)

            source_text = "\n".join([f"• `{s}`" for s in sources]) if sources else "No specific files referenced."

            response_text = f"*Answer:*\n{answer}\n\n*Sources:*\n{source_text}"
        else:
            response_text = "Please ask a question about the codebase! Example: `@bot how does authentication work?`"

        # Return response for Slack
        return {
            "response_type": "in_channel",
            "text": response_text
        }

    return {"status": "ok"}


@router.post("/slack/ask")
async def slack_slash_command(request: Request):
    """
    Handle Slack slash command: /ask <question>
    Configure in Slack App as a slash command pointing to: https://your-domain/api/slack/ask
    """
    form_data = await request.form()
    question = form_data.get("text", "").strip()

    if not question:
        return {
            "response_type": "ephemeral",
            "text": "Please provide a question. Usage: `/ask how does authentication work?`"
        }

    answer, sources = answer_question(question)

    source_text = "\n".join([f"• `{s}`" for s in sources]) if sources else "No specific files referenced."

    return {
        "response_type": "in_channel",
        "text": f"*Question:* {question}\n\n*Answer:*\n{answer}\n\n*Sources:*\n{source_text}"
    }
