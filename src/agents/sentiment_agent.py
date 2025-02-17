from langchain.agents import Tool
from langchain_community.tools import BaseTool
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime
from typing import List, Dict, Any

class SentimentAnalysisTool(BaseTool):
    name: str = "sentiment_analyzer"
    description: str = "Analyzes market sentiment from scraped content"

    def __init__(self):
        super().__init__()
        self._llm = OllamaLLM(model="llama2")
        self._prompt = PromptTemplate(
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
        self._chain = LLMChain(llm=self._llm, prompt=self._prompt)

    def _run(self, content: List[Dict[str, str]]) -> Dict[str, Any]:
        combined_text = "\n".join([item['text'] for item in content])
        analysis = self._chain.run(content=combined_text)
        
        return {
            'sentiment_analysis': analysis,
            'analyzed_documents': len(content),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _arun(self, content: List[Dict[str, str]]) -> Dict[str, Any]:
        raise NotImplementedError("Async not implemented") 