from datetime import datetime, timedelta
from time import mktime

import feedparser
import pytz
import requests
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver


class InternationalOrganizationRetriever:
    rss_url = 'https://www.cambridge.org/core/rss/product/id/146C8B1E6606CE283EBC5B10B255F4C0'
    timezone = pytz.timezone('Asia/Bangkok')

    def fetch_recent_entries(self, now=None, hours_ago=24):
        feed = feedparser.parse(self.rss_url)
        entries = feed.entries
        recent_entries = retrieve_recent_entries(
            entries, timezone=self.timezone, now=now, hours_ago=hours_ago)
        return recent_entries

    def extract_abstract(self, entry) -> str:
        # Get page contents
        response = requests.get(entry.link)

        # Parse page contents
        soup = BeautifulSoup(response.text, 'html.parser')

        abstract_class = soup.find(class_='abstract')

        if abstract_class is None:
            return ''
        
        abstract_contents =  abstract_class.find_all('p', recursive=False)[0]
        abstract_text = abstract_contents.contents[0]

        return abstract_text


def check_entry_recent(entry, timezone, now=None, hours_ago=24):
    if now is None:
        now = datetime.now(tz=timezone)

    entry_time = datetime.fromtimestamp(
        mktime(entry.updated_parsed), tz=timezone)
    start_time = now - timedelta(hours=hours_ago)

    if (start_time <= entry_time < now):
        return True

    return False


def retrieve_recent_entries(entries, timezone, now=None, hours_ago=24) -> List:
    if now is None:
        now = datetime.now(tz=timezone)

    return [entry for entry in entries if check_entry_recent(entry, timezone, now, hours_ago)]
