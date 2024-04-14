from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import mktime
import feedparser
import requests
from typing import List
from bs4 import BeautifulSoup

from run_date_mgt import get_current_datetime, ICT


class Retriever(ABC):
    name: str
    rss_url: str

    def fetch_recent_entries(self, current_datetime=None, start_datetime=None):
        feed = feedparser.parse(self.rss_url)
        entries = feed.entries
        return retrieve_recent_entries(entries, current_datetime=current_datetime, start_datetime=start_datetime)

    def extract_abstract(self, entry) -> str:
        """Common page retrieval and parsing process"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(
            'https://academic.oup.com/ia/advance-article/doi/10.1093/ia/iiae069/7641065', headers=headers)
        # response = requests.get(entry.link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.parse_abstract(soup)

    @abstractmethod
    def parse_abstract(self, soup) -> str:
        """Abstract method to define the specific abstract parsing method in subclasses"""
        pass

    @abstractmethod
    def get_entry_property(self, entry) -> dict:
        pass


class InternationalAffairsLatestIssueRetriever(Retriever):
    name = 'International Affairs'
    rss_url = 'https://academic.oup.com/rss/site_5569/3425.xml'

    def parse_abstract(self, soup) -> str:
        abstract_class = soup.find(class_='abstract')
        if abstract_class is None:  # In case not a article page
            return ''
        abstract_contents = abstract_class.find_all('p', recursive=False)[0]
        abstract_text = abstract_contents.contents[0]  # first contents
        return abstract_text

    def get_entry_property(self, entry) -> dict:
        date = entry['updated']
        url = entry['link']
        title = entry['title']
        authors = ''
        return {
            'journal_name': self.name,
            'date': date,
            'url': url,
            'title': title,
            'authors': authors
        }


class InternationalAffairsAdvanceArticlesRetriever(Retriever):
    name = 'International Affairs'
    rss_url = 'https://academic.oup.com/rss/site_5569/advanceAccess_3425.xml'

    def parse_abstract(self, soup) -> str:
        abstract_class = soup.find(class_='chapter-para')
        if abstract_class is None:  # In case not a article page
            return ''
        abstract_contents = abstract_class.find_all('p', recursive=False)[0]
        abstract_text = abstract_contents.contents[0]  # first contents
        return abstract_text

    def get_entry_property(self, entry) -> dict:
        date = entry['updated']
        url = entry['link']
        title = entry['title']
        authors = ''
        return {
            'journal_name': self.name,
            'date': date,
            'url': url,
            'title': title,
            'authors': authors
        }


class InternationalOrganizationRetriever(Retriever):
    name = 'International Organization'
    rss_url = 'https://www.cambridge.org/core/rss/product/id/146C8B1E6606CE283EBC5B10B255F4C0'

    def parse_abstract(self, soup) -> str:
        abstract_class = soup.find(class_='abstract')
        if abstract_class is None:  # In case not a article page
            return ''
        abstract_contents = abstract_class.find_all('p', recursive=False)[0]
        abstract_text = abstract_contents.contents[0]
        return abstract_text

    def get_entry_property(self, entry) -> dict:
        date = entry['updated']
        url = entry['link']
        title = entry['title']
        authors = ';'.join([item.name for item in entry['authors']])
        return {
            'journal_name': self.name,
            'date': date,
            'url': url,
            'title': title,
            'authors': authors
        }


class WorldPoliticsRetriever(Retriever):
    name = 'World Politics'
    rss_url = 'https://muse.jhu.edu/feeds/latest_articles?jid=208'

    def parse_abstract(self, soup) -> str:
        abstract_class = soup.find(class_='abstract')
        if abstract_class is None:  # In case not a article page
            return ''
        abstract_contents = abstract_class.find_all('p', recursive=False)[0]
        abstract_paragraph = abstract_contents.contents[1]  # second <p>
        abstract_text = abstract_paragraph.contents[0]  # first contents
        return abstract_text

    def get_entry_property(self, entry) -> dict:
        date = entry['updated']
        url = entry['link']
        title = entry['title']
        authors = ''
        return {
            'journal_name': self.name,
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
    entry_time = datetime.fromtimestamp(mktime(entry.updated_parsed), tz=ICT)
    return start_datetime <= entry_time < current_datetime


def retrieve_recent_entries(entries, current_datetime=None, start_datetime=None) -> List:
    if current_datetime is None:
        current_datetime = get_current_datetime()
    if start_datetime is None:
        start_datetime = current_datetime - timedelta(days=1)
    return [entry for entry in entries if check_entry_recent(entry, current_datetime, start_datetime)]

def get_all_retrievers():
    return Retriever.__subclasses__()