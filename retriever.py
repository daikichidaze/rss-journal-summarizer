from datetime import datetime, timedelta
from time import mktime

import feedparser
import requests
import pytz
from typing import List
from bs4 import BeautifulSoup

from run_date_mgt import get_current_datetime, ICT


class InternationalOrganizationRetriever:
    name = 'International Organization'
    rss_url = 'https://www.cambridge.org/core/rss/product/id/146C8B1E6606CE283EBC5B10B255F4C0'

    def fetch_recent_entries(self, current_datetime=None, start_datetime=None):
        feed = feedparser.parse(self.rss_url)
        entries = feed.entries
        recent_entries = retrieve_recent_entries(
            entries, current_datetime=current_datetime, start_datetime=start_datetime)
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


def check_entry_recent(entry, current_datetime=None, start_datetime=None):
    if current_datetime is None:
        current_datetime = get_current_datetime()
    if start_datetime is None:
        start_datetime = current_datetime - timedelta(days=1)

    entry_time = datetime.fromtimestamp(
        mktime(entry.updated_parsed), tz=ICT)

    if (start_datetime <= entry_time < current_datetime):
        return True

    return False


def retrieve_recent_entries(entries, current_datetime=None, start_datetime=None) -> List:
    if current_datetime is None:
        current_datetime = get_current_datetime()
    if start_datetime is None:
        start_datetime = current_datetime - timedelta(days=1)

    return [entry for entry in entries if check_entry_recent(entry, current_datetime, start_datetime)]
