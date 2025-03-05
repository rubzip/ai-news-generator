from fun import NewsSummarizer, NewsScrapper, ContentGenerator, NewsOfTheDay
import json

from settings import api_key, rss_url_list, summary_prompt, generator_prompt, max_entries, sleep_time, model_name

summarizer = NewsSummarizer(api_key=api_key, summary_prompt=summary_prompt)
scrapper = NewsScrapper(summarizer=summarizer, max_entries=max_entries, sleep_time=sleep_time)
generator = ContentGenerator(api_key=api_key, generator_prompt=generator_prompt, model_name=model_name)

news_of_the_day = NewsOfTheDay(scrapper=scrapper, generator=generator)
news_of_day_parsed = news_of_the_day.generate(rss_url_list)

with open('output/news_of_day.json', 'w', encoding="utf-8") as f:
    json.dump(news_of_day_parsed, f, ensure_ascii=False, indent=4)