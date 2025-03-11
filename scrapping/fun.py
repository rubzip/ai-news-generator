import re
import abc
import time
import json
import random
from string import Template


import requests
import feedparser
from bs4 import BeautifulSoup
import google.generativeai as genai
from langchain_core.output_parsers import JsonOutputParser


class LLMService(abc.ABC):
    @classmethod
    def generate_text(self, prompt: str) -> str: ...


class GoogleLLMService(LLMService):
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""


class Summarizer:
    def __init__(self, llm_service: LLMService, prompt_template: str):
        self.llm_service = llm_service
        self.prompt_template = Template(prompt_template)

    def summarize(self, insert: dict[str, str]) -> str:
        prompt = self.prompt_template.safe_substitute(insert)
        return self.llm_service.generate_text(prompt)


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


class Orchestrator:
    def __init__(self, scrapper: Scrapper, summarizer: Summarizer, news_aggregator: Summarizer, attributes: list = ["title", "url", "summary"], summary_time=10):
        self.scrapper = scrapper
        self.summarizer = summarizer
        self.news_aggregator = news_aggregator

        self.attributes = attributes
        self.summary_time = summary_time
        self.parser = JsonOutputParser()

    def run(self, rss_url_list: list[str], shuffle_news: bool = True) -> dict|None:
        """
        Executes the complete news summarization pipeline:
        1. Scrapes news from RSS feeds (titles, URLs, and full HTML content)
        2. Generates AI-powered summaries for each article
        3. Creates a structured daily digest using an AI model

        Args:
            rss_url_list (list[str]): List of RSS feed URLs
            shuffle_news (bool): Whether to randomize news order. Defaults to True

        Returns:
            dict: JSON-structured daily summary with keywords, content sections, and sources
        """

        # Scrapping news
        news_list = self.scrapper.scrape_news(rss_url_list)
        if shuffle_news:
            random.shuffle(news_list)
        # Summarizing every news
        news_summarized = []
        for news in news_list:
            content = news.get("content")
            summary = self.summarizer.summarize({"content": content}) if content else ""
            time.sleep(self.summary_time)
            if summary:
                news_summarized.append({**news, "summary": summary})

        with open("output/news_list.json", "w", encoding="utf-8") as f:  # delete in production
            json.dump(news_summarized, f, ensure_ascii=False, indent=4)  # delete in production
        # Avoiding to consider all the atributes in every news dictionary
        news_list_to_ingest = [
            {att: news.get(att, "") for att in self.attributes}
            for news in news_summarized
        ]
        news_list_to_ingest_str = "\n".join(map(str, news_list_to_ingest))
        # Aggregating all the news
        daily_summary = self.news_aggregator.summarize(
            {"content": news_list_to_ingest_str}
        )

        try:
            daily_summary_json = self.parser.parse(daily_summary)
            return daily_summary_json
        except:
            return None
