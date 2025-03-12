from .LLM import JsonGenerator
from .Scrapper import Scrapper
import random
import time
import json
from datetime import date

class Orchestrator:
    def __init__(self, scrapper: Scrapper, news_processor: JsonGenerator, news_aggregator: JsonGenerator, attributes: list = ["title", "url", "summary", "score"], summary_time=10, number_of_news=8):
        self.scrapper = scrapper
        self.news_processor = news_processor
        self.news_aggregator = news_aggregator

        self.attributes = attributes
        self.summary_time = summary_time
        self.number_of_news = number_of_news

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
        
        # Summarizing news and getting score
        news_processed = []
        for news in news_list:
            content = news.get("content")
            output = self.news_processor.get_json_response({"content": content}) if content else None
            time.sleep(self.summary_time)
            if output:
                news_processed.append({**news, **output})

        with open("output/news_list.json", "w", encoding="utf-8") as f:  # delete in production
            json.dump(news_processed, f, ensure_ascii=False, indent=4)   # delete in production

        # Avoiding to consider all the atributes in every news dictionary
        news_list_to_ingest = [
            {att: news.get(att, "") for att in self.attributes}
            for news in news_processed
        ]
        
        # Filtering the n with highest score
        news_list_to_ingest = sorted(news_list_to_ingest, key=lambda x: x.get("score", 0), reverse=True)[:self.number_of_news]
        news_list_to_ingest_str = "\n".join(map(str, news_list_to_ingest))

        # Aggregating all the news
        daily_summary = self.news_aggregator.get_json_response(
            {"content": news_list_to_ingest_str}
        )

        return {
            **daily_summary,
            "date": date.today().isoformat()
            }