import os
from time import sleep

from run_date_mgt import get_current_datetime, read_last_run_date, update_last_run_date
from retriever import get_all_retrievers
from openai_wrapper import summarize_abstract
from sender import SlackSender


def post_summary(retriever) -> bool:
    recent_entries = retriever.fetch_recent_entries(now, last_run_date)

    had_updates = False
    entry_count = 0

    for entry in recent_entries:
        abstract: str = retriever.extract_abstract(entry)
        entry_property: dict = retriever.get_entry_property(entry)

        if abstract != '':
            summary = summarize_abstract(abstract, openai_api_key, model)
        else:
            summary = 'Abstract not found'

        status = sender.send_summary(entry_property, summary)
        # status = 200
        if status == 200:
            had_updates = True
            entry_count += 1
        sleep(5)

    print(f'Posted {entry_count} entries from {retriever.name}')
    return had_updates


if __name__ == "__main__":
    model = 'gpt-4o-mini'
    openai_api_key = os.environ['OPENAI_API_KEY']
    slack_webhook_url = os.environ['SLACK_URL']
    run_date_file = 'last_run_date.json'

    sender = SlackSender(slack_webhook_url)

    now = get_current_datetime()
    last_run_date = read_last_run_date(run_date_file)

    update_result = False

    for retriever_class in get_all_retrievers():
        retriever = retriever_class()
        update_result = post_summary(retriever) or update_result

    if update_result:
        update_last_run_date(run_date_file, now)
