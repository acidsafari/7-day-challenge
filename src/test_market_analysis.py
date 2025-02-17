import logging
from config import ScrapingConfig
from main import MarketAnalysisOrchestrator
import sys
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_market_analysis():
    # Test configuration with more reliable financial news URLs
    test_config = ScrapingConfig(
        base_urls=[
            "https://www.marketwatch.com/investing",
            "https://www.investing.com/news/stock-market-news",
            "https://finance.yahoo.com/topic/stock-market-news",
        ],
        max_pages=2,  # Limited for testing
        days_to_scrape=1,  # Just today's news
        retry_attempts=2,
        timeout=20
    )

    try:
        # Initialize the orchestrator
        logging.info("Initializing Market Analysis Orchestrator...")
        orchestrator = MarketAnalysisOrchestrator(test_config)

        # Run the analysis
        logging.info("Starting market analysis...")
        result = orchestrator.run_analysis()

        # Print results
        if result['status'] == 'success':
            print("\n=== Analysis Results ===")
            print(f"Status: {result['status']}")
            print(f"Pages Scraped: {result['scraped_pages']}")
            
            sentiment_data = result['sentiment_analysis']
            print("\nSentiment Analysis Report:")
            print("-" * 50)
            print(sentiment_data['sentiment_analysis'])
            print("-" * 50)
            print(f"\nAnalyzed Documents: {sentiment_data['analyzed_documents']}")
            print(f"Analysis Timestamp: {sentiment_data['timestamp']}")
            
        else:
            print("\n=== Error in Analysis ===")
            print(f"Status: {result['status']}")
            print(f"Error: {result.get('error', 'Unknown error')}")

    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Test failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    print("Starting Market Analysis Test...")
    print("Make sure Ollama is running with the llama2 model installed")
    print("Press Ctrl+C to stop the test at any time")
    print("-" * 50)
    
    try:
        # Small delay to read the instructions
        time.sleep(2)
        test_market_analysis()
    except KeyboardInterrupt:
        print("\nTest stopped by user")
        sys.exit(1) 