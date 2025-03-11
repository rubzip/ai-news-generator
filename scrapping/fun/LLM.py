from google import genai
from pydantic import BaseModel
from string import Template
import abc

class LLMService(abc.ABC):
    @classmethod
    def generate_json(self, prompt: str) -> dict: ...

class GoogleLLMService(LLMService):
    def __init__(self, api_key: str, response_schema: BaseModel, model_name: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.response_schema = response_schema
        self.model_name = model_name
    
    def generate_json(self, prompt: str) -> dict:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": self.response_schema
                }
            )
            return response.parsed.model_dump()
        except:
            return {}

class JsonGenerator:
    def __init__(self, llm_service: LLMService, prompt_template: str):
        self.llm_service = llm_service
        self.prompt_template = Template(prompt_template)
    
    def get_json_response(self, mapping: dict):
        return self.llm_service.generate_json(self.prompt_template.safe_substitute(mapping))