import os
from datetime import datetime
from time import sleep

import pytz

from run_date_mgt import get_current_datetime, read_last_run_date, update_last_run_date
from retriever import InternationalOrganizationRetriever
from openai_wrapper import summarize_abstract
from sender import SlackSender


if __name__ == "__main__":
    model = 'gpt-3.5-turbo'
    openai_api_key = os.environ['OPENAI_API_KEY']
    slack_webhook_url = os.environ['SLACK_URL']
    run_date_file = 'last_run_date.json'

    now = get_current_datetime()
    last_run_date = read_last_run_date(run_date_file)

    retriever = InternationalOrganizationRetriever()
    recent_entries = retriever.fetch_recent_entries(now, last_run_date)

    sender = SlackSender(slack_webhook_url)

    had_updates = False

    for entry in recent_entries:
        abstract: str = retriever.extract_abstract(entry)

        if abstract == '':
            continue
        # summary = summarize_abstract(abstract, openai_api_key, model)
        summary = """## 要約
- 国際批判に対して、whataboutism（他の国の同様の過ちを指摘する）は公衆の意見を変える効果がある。
- 類似の過ちを引き合いに出すwhataboutismは、アメリカ合衆国の立場や処罰措置に対する公衆の支持を低下させる。
- アメリカの対立メッセージはwhataboutismの影響を減らすのに失敗することが多い。
## 解説
この研究は、国際批判に直面するとき、国家が他国の同様の欠点を指摘するwhataboutismがアメリカの公衆意見をどのように形成するかを調査している。whataboutismは批判の影響を軽減し、公衆の立場を変える効果があり、類似の最近の過ちを引用するwhataboutismが意見を形成する力を持つことが分かった。しかし、whataboutist国家のアイデンティティは効果に大きな影響を与えない。これらの結果から、whataboutismは国際関係における強力な修辞戦術であり、国際関係の研究者により多くの注意を必要とすることが示されている。"""

        # status = sender.send_summary(entry, summary, retriever.name)
        status = 200
        if status == 200:
            had_updates = True
        sleep(5)
    
    if had_updates:
        update_last_run_date(run_date_file, now)

