from typing import Optional
from pydantic import BaseModel

class ScrapingConfig(BaseModel):
    max_pages: int = 10
    days_to_scrape: int = 7
    base_urls: list[str]
    retry_attempts: int = 3
    timeout: int = 30
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" 