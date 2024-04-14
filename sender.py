import json

import requests


class SlackSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_summary(self, propertiy, summary):
        data = {
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'<{propertiy["url"]}|{propertiy["title"]}>',
                    },
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'Journal: `{propertiy["journal_name"]}`\n'
                                f'Authors: `{propertiy["authors"]}`\n'
                                f'Date: `{propertiy["date"]}`\n'
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
