rss_url_list = [
    # https://news.google.com/headlines/section/topic/NATION?hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/pJtCWZLcLPUtlICC.xml",
    
    # https://news.google.com/headlines/section/topic/TECHNOLOGY?hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/LXWIy0QwhgozSYBT.xml",
    
    # https://news.google.com/headlines/section/topic/BUSINESS?hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/wrafKnrRQmcvW9w7.xml",
    
    # https://news.google.com/headlines/section/topic/SCIENCE?hl=es&gl=ES&ceid=ES:es
    "https://rss.app/feeds/1pcG6ARQfeV8z63e.xml"
]

api_key = ""
summary_prompt_path = "prompt/summary_prompt.txt"
generator_prompt_path = "prompt/generator_prompt.txt"
model_name = "gemini-1.5-flash"

max_entries = 10
sleep_time = 10

with open(summary_prompt_path, "r") as f:
    summary_prompt = f.read()

with open(generator_prompt_path, "r") as f:
    generator_prompt = f.read()