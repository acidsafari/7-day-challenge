from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime

class SentimentAnalysisTool(BaseTool):
    name = "sentiment_analyzer"
    description = "Analyzes market sentiment from scraped content"

    def __init__(self):
        super().__init__()
        self.llm = Ollama(model="llama2")  # Or your preferred model
        self.prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            Analyze the following content and provide a market sentiment analysis report.
            Consider the following aspects:
            - Overall market sentiment (bullish/bearish/neutral)
            - Key trends and patterns
            - Notable market concerns or opportunities
            - Confidence level in the analysis

            Content: {content}
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def __call__(self, content: list[dict]) -> dict:
        combined_text = "\n".join([item['text'] for item in content])
        analysis = self.chain.run(content=combined_text)
        
        return {
            'sentiment_analysis': analysis,
            'analyzed_documents': len(content),
            'timestamp': datetime.now().isoformat()
        } 