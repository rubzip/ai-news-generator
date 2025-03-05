import re
import requests
import feedparser
import time
from bs4 import BeautifulSoup
import google.generativeai as genai

from langchain_core.output_parsers import JsonOutputParser
import json
import random


class GoogleLLMAPI:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def __call__(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""

class NewsSummarizer:
    def __init__(self, api_key: str, summary_prompt: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        self.summary_prompt = summary_prompt
    
    def summarize(self, new: str) -> str:
        try:
            prompt = self.summary_prompt.replace("{{insert}}", new)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""

class NewsSummarizer2:
    def __init__(self, api_caller, summary_prompt: str):
        self.api_caller = api_caller
        self.summary_prompt = summary_prompt
    
    def summarize(self, new: str) -> str:
        prompt = self.summary_prompt.replace("{{insert}}", new)
        return self.api_caller(prompt)

class NewsScrapper:
    def __init__(self, summarizer: NewsSummarizer, max_entries: int=100, sleep_time: int=5):
        self.summarizer = summarizer
        self.max_entries = max_entries
        self.sleep_time = sleep_time

    def scrape_news(self, rss_url_list: list[str]) -> list[dict[str, str]]:
        news_list = self._get_list_of_news_from_list(rss_url_list)
        news_list_with_content = self._fetch_news_content_from_list(news_list)
        return news_list_with_content
    
    def _get_list_of_news_from_list(self, rss_url_list: list[str]) -> list[dict[str, str]]:
        news = []
        for rss_url in rss_url_list:
            news.extend(self._get_list_of_news(rss_url))
        return news
    
    def _get_list_of_news(self, rss_url: str) -> list[dict[str, str]]:
        feed = feedparser.parse(rss_url)
        news = []
        for entry in feed.entries[:self.max_entries]:
            news.append({
                "title": entry.title,
                "url": entry.link,
                "published": entry.published
            })
        return news
    
    def _fetch_news_content_from_list(self, news_list: list[dict[str, str]]) -> list[dict[str, str]]:
        news_list_with_content = []
        for news in news_list:
            content = self._fetch_news_content(news["url"])
            if content=="":
                continue
            summary = self.summarizer.summarize(content)
            if summary:
                news_list_with_content.append({**news, "content": content, "summary": summary})
            time.sleep(self.sleep_time)

        return news_list_with_content

    def _fetch_news_content(self, url: str) -> str:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = BeautifulSoup(response.text, 'html.parser').get_text()
                clean_content = re.sub(r'[\s\n]+', ' ', content)
                return clean_content
        except Exception as e:
            print(f"Error getting news from {url}: {e}")
        return ""
    
    
class ContentGenerator:
    def __init__(self, api_key: str, generator_prompt: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        self.generator_prompt = generator_prompt
        self.attributes = ["title", "url", "summary"]
    
    def generate_content(self, news: list[dict[str, str]]) -> str:
        try:
            filtered_news = [{att: new.get(att, "") for att in self.attributes} for new in news]
            news_string = "\n".join(map(str, filtered_news))

            prompt = self.generator_prompt.replace("{{insert}}", news_string)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""

class ContentGenerator2:
    def __init__(self, api_caller, generator_prompt: str, attributes: list = ["title", "url", "summary"]):
        self.api_caller = api_caller
        self.generator_prompt = generator_prompt
        self.attributes = attributes
    
    def generate_content(self, news: list[dict[str, str]]) -> str:
        filtered_news = [{att: new.get(att, "") for att in self.attributes} for new in news]
        news_string = "\n".join(map(str, filtered_news))
        prompt = self.generator_prompt.replace("{{insert}}", news_string)
        return self.api_caller(prompt)

class NewsOfTheDay:
    def __init__(self, scrapper: NewsScrapper, generator: ContentGenerator):
        self.scrapper = scrapper
        self.generator = generator
        
        self.parser = JsonOutputParser()
        
    def generate(self, rss_url_list: list[str], shuffle_news: bool=True) -> dict:
        news_list = self.scrapper.scrape_news(rss_url_list)
        if shuffle_news:
            random.shuffle(news_list)

        with open('output/news_list.json', 'w', encoding="utf-8") as f: # delete in production
            json.dump(news_list, f, ensure_ascii=False, indent=4)       # delete in production

        news_of_day = self.generator.generate_content(news_list)
        news_of_day_parsed = self.parser.parse(news_of_day)

        return news_of_day_parsed