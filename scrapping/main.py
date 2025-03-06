from fun import GoogleLLMService, Summarizer, Scrapper, Orchestrator
import json

from settings import api_key, rss_url_list, summary_prompt, generator_prompt, max_entries, sleep_time, model_name

if __name__=="__main__":
    llm_service = GoogleLLMService(api_key, model_name)
    summarizer = Summarizer(llm_service, summary_prompt)
    news_aggregator = Summarizer(llm_service, generator_prompt)
    scrapper = Scrapper(max_entries, sleep_time)

    orchestrator = Orchestrator(scrapper, summarizer, news_aggregator)
    news_summary_json = orchestrator.run(rss_url_list)

    with open('output/news_of_day.json', 'w', encoding="utf-8") as f:
        json.dump(news_summary_json, f, ensure_ascii=False, indent=4)