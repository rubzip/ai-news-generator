from dotenv import load_dotenv
import os

rss_url_list = [
    # https://news.google.com/headlines/section/topic/NATION?hl=es&gl=ES&ceid=ES:es
    # "https://rss.app/feeds/pJtCWZLcLPUtlICC.xml",
    
    # https://news.google.com/headlines/section/topic/TECHNOLOGY?hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/LXWIy0QwhgozSYBT.xml",
    
    # https://news.google.com/headlines/section/topic/BUSINESS?hl=es&gl=ES&ceid=ES:es
    #"https://rss.app/feeds/wrafKnrRQmcvW9w7.xml",
    
    # https://news.google.com/headlines/section/topic/SCIENCE?hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/1pcG6ARQfeV8z63e.xml",

    # https://news.google.com/search?q=inteligencia+artificial&hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/LZRtqXzeyFlAnPep.xml",

    "https://news.ycombinator.com/rss",

    "https://www.reddit.com/r/technology/.rss",

    "https://www.reddit.com/r/science/.rss",

    "https://es.wired.com/feed/rss",

    "https://es.wired.com/feed/ciencia/rss",

    "https://feeds.bloomberg.com/technology/news.rss"
]

load_dotenv()
api_key = os.getenv("API_KEY")

summary_prompt_path = "prompt/summary_prompt.txt"
generator_prompt_path = "prompt/generator_prompt.txt"
model_name = "gemini-2.0-flash-lite"

max_entries = 5
sleep_time = 10

with open(summary_prompt_path, "r") as f:
    summary_prompt = f.read()

with open(generator_prompt_path, "r") as f:
    generator_prompt = f.read()