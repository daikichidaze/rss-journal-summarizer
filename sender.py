import json

import requests


class SlackSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_summary(self, entry, summary, journal_title):
        authors = '; '.join([author.name for author in entry.authors])

        data = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{entry.link}|{entry.title}>",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'Journal: `{journal_title}`\n'
                                f'Authors: `{authors}`\n'
                                f'Date: `{entry.updated}`\n'
                    },
                },
                {"type": "divider"},
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_preformatted",
                            "elements": [
                                {
                                    "type": "text",
                                    "text": summary
                                }
                            ]
                        }
                    ]
                },
            ],
            "unfurl_links": False,
        }

        headers = {'Content-Type': 'application/json'}
        res = requests.post(
            self.webhook_url, data=json.dumps(data), headers=headers)

        res.raise_for_status()

        return res.status_code
