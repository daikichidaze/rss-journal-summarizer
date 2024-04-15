import json
import requests


class SlackSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_summary(self, property, summary):
        authors_text = f'Authors: `{property["authors"]}`\n' if property["authors"] else ""
        data = {
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'<{property["url"]}|{property["title"]}>',
                    },
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'Journal: `{property["journal_name"]}`\n'
                                f'{authors_text}'
                                f'Date: `{property["date"]}`\n'
                    },
                },
                {'type': 'divider'},
                {
                    'type': 'rich_text',
                    'elements': [
                        {
                            'type': 'rich_text_preformatted',
                            'elements': [
                                {
                                    'type': 'text',
                                    'text': summary
                                }
                            ]
                        }
                    ]
                },
            ],
            'unfurl_links': False,
        }

        headers = {'Content-Type': 'application/json'}
        res = requests.post(
            self.webhook_url, data=json.dumps(data), headers=headers)

        res.raise_for_status()

        return res.status_code
