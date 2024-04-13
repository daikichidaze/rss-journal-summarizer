import json
import os
import requests
from datetime import datetime, timedelta, timezone
from time import sleep

import pytz

from retriever import InternationalOrganizationRetriever
from openai_wrapper import summarize_abstract

# Indochina Timezone
ICT = pytz.timezone('Asia/Bangkok')

# Slack Webhook URL
WEBHOOK_URL = "{通知先のWebhook URL}"


def post_to_slack(message: str, link_url: str, title: str) -> None:
    """
    RSSフィードとOpenAIの要約SlackのWebhookURLへPOST
    """
    data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{link_url}|{title}>",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message,
                },
            },
            {"type": "divider"},
        ],
        "unfurl_links": False,
    }
    requests.post(WEBHOOK_URL, data=json.dumps(data))


if __name__ == "__main__":
    model = 'gpt-3.5-turbo'
    openai_api_key = os.environ['OPENAI_API_KEY']

    now = datetime.now(tz=ICT)
    retriever = InternationalOrganizationRetriever()
    recent_entries = retriever.fetch_recent_entries(now, hours_ago=24*62)

    # sender = DiscordSender(discord_url)
    for entry in recent_entries:
        abstract: str = retriever.extract_abstract(entry)

        if abstract == '':
            continue
        # summary = summarize_abstract(abstract, openai_api_key, model)
        summary = abstract[:10]
    #     sender.send_summary(entry, summary)
        sleep(5)
