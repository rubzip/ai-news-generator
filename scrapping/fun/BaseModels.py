from pydantic import BaseModel


class ProcessNews(BaseModel):
    summary: str
    score: float

class ContentItem(BaseModel):
    category: str
    text: str

class Source(BaseModel):
    title: str
    url: str

class GenerateNews(BaseModel):
    keywords: list[str]
    content: list[ContentItem]
    sources: list[Source]