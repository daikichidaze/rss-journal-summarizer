import openai
import json
import requests
import pytz
from datetime import datetime, timedelta, timezone

from retriever import InternationalOrganizationRetriever

# Indochina Timezone
ICT = timezone(timedelta(hours=+7))

# APIキーの設定
# openai.api_key = os.environ["OPENAI_API_KEY"]

# Slack Webhook URL
WEBHOOK_URL = "{通知先のWebhook URL}"

SYSTEM_PARAMETER = """```
与えられたフィードの情報を、以下の制約条件をもとに要約を出力してください。

制約条件:
・文章は簡潔にわかりやすく。
・箇条書きで3行で出力。
・要約した文章は日本語へ翻訳。
・最終的な結論を含めること。

期待する出力フォーマット:
1.
2.
3.
```"""


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
    # openai_api_key = os.environ['OPENAI_API_KEY']
    # discord_url = os.environ['DISCORD_URL']

    now = datetime.now(tz=pytz.timezone('Asia/Bangkok'))
    retriever = InternationalOrganizationRetriever()
    recent_entries = retriever.fetch_recent_entries(now, hours_ago=24*62)

    # sender = DiscordSender(discord_url)
    for entry in recent_entries:
        abstract: str = retriever.extract_abstract(entry)

        if abstract == '':
            continue
    #     summary = summarize_abstract(abstract, openai_api_key, model)
    #     sender.send_summary(entry, summary)
    #     sleep(5)
