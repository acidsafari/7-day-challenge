# 7-day-challenge

Here we share the results of AICamp's 7-day-challenge, where we created a RAG application for financial analysis.

## web-scrapper-NO-FRAMEWORK

To use this workflow:
    1. Initialize the WebScrapingWorkflow
    2. Call the scrape() method with your target URL
    3. Handle potential exceptions appropriately

The workflow will automatically:
    - Handle temporary network errors
    - Manage cookies and sessions
    - Follow redirects while maintaining context
    - Detect and handle common error states
    - Attempt to manage cookie consent popups

Example usage pattern:

    scraper = WebScrapingWorkflow()
    try:
        result = scraper.scrape("https://target-website.com")
        # Process the BeautifulSoup object...
    except ScrapeError:
        # Handle final failure...


## web-scrapper-hugging-face

