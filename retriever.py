from datetime import datetime, timedelta
from time import mktime

import feedparser
import requests
import pytz
from typing import List
from bs4 import BeautifulSoup


# Indochina Timezone
ICT = pytz.timezone('Asia/Bangkok')


class InternationalOrganizationRetriever:
    name = 'International Organization'
    rss_url = 'https://www.cambridge.org/core/rss/product/id/146C8B1E6606CE283EBC5B10B255F4C0'

    def fetch_recent_entries(self, now=None, hours_ago=24):
        feed = feedparser.parse(self.rss_url)
        entries = feed.entries
        recent_entries = retrieve_recent_entries(
            entries, now=now, hours_ago=hours_ago)
        return recent_entries

    def extract_abstract(self, entry) -> str:
        # Get page contents
        response = requests.get(entry.link)

        # Parse page contents
        soup = BeautifulSoup(response.text, 'html.parser')

        abstract_class = soup.find(class_='abstract')

        if abstract_class is None:
            return ''

        abstract_contents = abstract_class.find_all('p', recursive=False)[0]
        abstract_text = abstract_contents.contents[0]

        return abstract_text

    def get_property(self, entry) -> dict:
        journal = entry['prism_publicationtitle']
        date = entry['prism_publicationdate']
        url = entry['link']
        title = entry['title']
        authors = ';'.join([item.name for item in entry['authors']])

        return {
            'journal': journal,
            'date': date,
            'url': url,
            'title': title,
            'authors': authors
        }


def check_entry_recent(entry, now=None, hours_ago=24):
    if now is None:
        now = datetime.now(tz=ICT)

    entry_time = datetime.fromtimestamp(
        mktime(entry.updated_parsed), tz=ICT)
    start_time = now - timedelta(hours=hours_ago)

    if (start_time <= entry_time < now):
        return True

    return False


def retrieve_recent_entries(entries, now=None, hours_ago=24) -> List:
    if now is None:
        now = datetime.now(tz=ICT)

    return [entry for entry in entries if check_entry_recent(entry, now, hours_ago)]
