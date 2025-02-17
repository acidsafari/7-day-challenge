from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from agents.scraping_agent import WebScrapingTool
from agents.sentiment_agent import SentimentAnalysisTool
from config import ScrapingConfig
import logging

class MarketAnalysisOrchestrator:
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.llm = OllamaLLM(model="llama2")
        self.scraping_tool = WebScrapingTool(config)
        self.sentiment_tool = SentimentAnalysisTool()
        
        self.agent = initialize_agent(
            tools=[self.scraping_tool, self.sentiment_tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def run_analysis(self) -> dict:
        try:
            # First, scrape the content
            scraped_data = self.scraping_tool._run(self.config.base_urls)
            
            if not scraped_data:
                raise ValueError("No data could be scraped from the provided URLs")

            # Then, analyze the sentiment
            sentiment_analysis = self.sentiment_tool._run(scraped_data)

            return {
                'status': 'success',
                'scraped_pages': len(scraped_data),
                'sentiment_analysis': sentiment_analysis
            }
        except Exception as e:
            logging.error(f"Error in market analysis: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }

# Usage example:
if __name__ == "__main__":
    config = ScrapingConfig(
        base_urls=[
            "https://example.com/markets",
            "https://example.com/finance",
        ],
        max_pages=5,
        days_to_scrape=3
    )
    
    orchestrator = MarketAnalysisOrchestrator(config)
    result = orchestrator.run_analysis()
    print(result) 