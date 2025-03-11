import os
from dotenv import load_dotenv

rss_url_list = [
    # Science
    "https://www.sciencedaily.com/rss/all.xml",
    "https://news.mit.edu/rss",
    "https://www.quantamagazine.org/feed/",
    "https://www.reddit.com/r/science/.rss",
    "https://es.wired.com/feed/ciencia/rss",
    # Technology
    "https://www.xataka.com/feedburner.xml",
    "https://news.ycombinator.com/rss",
    "https://www.technologyreview.com/feed/",
    "https://www.reddit.com/r/technology/.rss",
    "https://es.wired.com/feed/rss",
    "https://feeds.bloomberg.com/technology/news.rss",
    # AI
    "https://techcrunch.com/tag/artificial-intelligence/feed/"
    # Math
    "http://mathworld.wolfram.com/feeds/rss.xml"
    # Spain
    "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "https://www.abc.es/rss/feeds/abcPortada.xml",
    "https://www.elmundo.es/rss/portada.xml",
]

load_dotenv()
api_key = os.getenv("API_KEY")

processor_prompt_path = "prompts/news_processor.txt"
aggregator_prompt_path = "prompts/news_aggregator.txt"
model_name = "gemini-2.0-flash-lite"

max_entries = 4
sleep_time = 10

with open(processor_prompt_path, "r", encoding="utf-8") as f:
    processor_prompt = f.read()

with open(aggregator_prompt_path, "r", encoding="utf-8") as f:
    aggregator_prompt = f.read()
