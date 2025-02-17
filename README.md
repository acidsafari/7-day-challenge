# Market Sentiment Analysis System

A multi-agent system that scrapes financial news websites and generates market sentiment analysis using LangChain and Ollama.

## Features

- Web scraping with robust error handling
  - 404 error handling
  - SSL certificate issues
  - Rate limiting with exponential backoff
  - Cookie management
  - Timeout handling
  - Connection error handling
- Sentiment analysis using Ollama LLM
- Configurable parameters for scraping scope
- Detailed logging system

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- The llama2 model installed in Ollama

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd market-sentiment-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and run Ollama:
```bash
# Install Ollama from: https://ollama.ai/
ollama pull llama2
```

## Project Structure

```
src/
├── agents/
│   ├── scraping_agent.py
│   └── sentiment_agent.py
├── config.py
├── main.py
└── test_market_analysis.py
```

## Configuration

You can configure the system by modifying the `ScrapingConfig` in `config.py`:

- `max_pages`: Maximum number of pages to scrape
- `days_to_scrape`: Time window for article collection
- `base_urls`: List of URLs to scrape
- `retry_attempts`: Number of retry attempts for failed requests
- `timeout`: Request timeout in seconds

## Usage

1. Ensure Ollama is running with the llama2 model:
```bash
ollama run llama2
```

2. Run the test script:
```bash
python src/test_market_analysis.py
```

## Error Handling

The system handles various common errors:
- Network connectivity issues
- Rate limiting
- SSL certificate errors
- Invalid URLs
- Timeout errors
- Cookie consent prompts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

