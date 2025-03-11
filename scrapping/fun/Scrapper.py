import feedparser
import time
import requests
import re
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, max_entries: int = 100, sleep_time: int = 5):
        self.max_entries = max_entries
        self.sleep_time = sleep_time

    def scrape_news(self, rss_url_list: list[str]) -> list[dict[str, str]]:
        news_url_list = self._get_urls_from_rss_list(rss_url_list)
        news_list = self._fetch_from_list(news_url_list)
        return news_list

    def _get_urls_from_rss_list(self, rss_url_list: list[str]) -> list[dict[str, str]]:
        url_news = []
        for rss_url in rss_url_list:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[: self.max_entries]:
                url_news.append(
                    {
                        "title": entry.title,
                        "url": entry.link,
                        "published": entry.published,
                    }
                )
        return url_news

    def _fetch_from_list(self, news_list: list[dict[str, str]]) -> list[dict[str, str]]:
        news_list_with_content = []
        for news in news_list:
            content = self._fetch(news["url"])
            if content:
                news_list_with_content.append({**news, "content": content})
            time.sleep(self.sleep_time)
        return news_list_with_content

    def _fetch(self, url: str) -> str:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = BeautifulSoup(response.text, "html.parser").get_text()
                clean_content = re.sub(r"[\s\n]+", " ", content)
                return clean_content
        except Exception as e:
            print(f"Error getting news from {url}: {e}")
        return ""