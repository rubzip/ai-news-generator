import json
from fun.LLM import GoogleLLMService, JsonGenerator
from fun.BaseModels import ProcessNews, GenerateNews
from fun.Scrapper import Scrapper
from fun.Orchestrator import Orchestrator

from settings import api_key, rss_url_list, processor_prompt, aggregator_prompt, max_entries, sleep_time, model_name, num_of_articles_considered

if __name__ == "__main__":
    llm_service_processor = GoogleLLMService(api_key, ProcessNews, model_name)
    llm_service_aggregator = GoogleLLMService(api_key, GenerateNews, model_name)
    
    processor = JsonGenerator(llm_service_processor, processor_prompt)
    aggregator = JsonGenerator(llm_service_aggregator, aggregator_prompt)

    scrapper = Scrapper(max_entries, sleep_time)

    orchestrator = Orchestrator(scrapper, processor, aggregator, number_of_news=num_of_articles_considered)
    news_summary_json = orchestrator.run(rss_url_list)

    with open('output/news_of_day.json', 'w', encoding="utf-8") as f:
        json.dump(news_summary_json, f, ensure_ascii=False, indent=4)
