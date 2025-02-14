import requests
from bs4 import BeautifulSoup
import time
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class CrawlerAgent:
    """
    CrawlerAgent: Handles HTTP requests with retries and SSL management
    """
    def __init__(self):
        # Set up session with retry configuration
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504, 429],
            allowed_methods=["GET", "POST"]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def fetch(self, url, user_agent=None, verify_ssl=True):
        """Fetch URL with error handling and retries
            Implementation handles:
                - SSL errors (with fallback)
                - HTTP status codes
                - Timeouts
                - Automatic retries
        """
        headers = {'User-Agent': user_agent or 'Mozilla/5.0'}

        try:
            response = self.session.get(
                url,
                headers=headers,
                allow_redirects=True,
                verify=verify_ssl,
                timeout=10
            )
            response.raise_for_status()
            return response

        except requests.exceptions.SSLError as e:
            logging.warning(f"SSL Error: {e}. Retrying without SSL verification...")
            return self.session.get(url, headers=headers, verify=False)

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error {e.response.status_code} for URL: {url}")
            if e.response.status_code == 404:
                raise PageNotFoundError(url)
            raise

        except requests.exceptions.RequestException as e:
            logging.error(f"Connection Error: {e}")
            raise


class ParserAgent:
    """
    ParserAgent: Manages HTML parsing with error detection
    """
    def __init__(self, parser="html.parser"):
        self.parser = parser

    def parse(self, content):
        """
        Parse HTML content with error handling
            - Wraps BeautifulSoup with error handling
            - Converts raw HTML to parseable DOM
        """
        try:
            return BeautifulSoup(content, self.parser)
        except Exception as e:
            logging.error(f"Parsing error: {e}")
            raise ParsingError("Failed to parse HTML content")


class ErrorHandlerAgent:
    """
    ErrorHandlerAgent: Detects redirects and error pages
    """
    @staticmethod
    def is_redirect(response, expected_url):
        """Check if redirect occurred to unexpected location"""
        if response.url != expected_url:
            logging.warning(f"Redirected to: {response.url}")
            return True
        return False

    @staticmethod
    def is_error_page(soup):
        """Detect common error pages in parsed content"""
        error_patterns = [
            '404', 'Not Found',
            '500', 'Server Error',
            'Access Denied', 'Unauthorized'
        ]
        text = soup.get_text().lower()
        return any(pattern.lower() in text for pattern in error_patterns)


class CookieManagerAgent:
    """
    CookieManagerAgent: Handles cookie consent popups
    """
    def __init__(self, crawler):
        self.crawler = crawler
        self.session = crawler.session

    def handle_cookie_consent(self, soup, url):
        """Detect and handle cookie consent popups

        Implements logic to:
            - Find consent forms
            - Submit form data
            - Maintain session state
        """
        consent_selectors = [
            ('form', {'id': 'cookie-consent'}),
            ('button', {'id': 'accept-cookies'}),
            ('div', {'class': 'cookie-banner'})
        ]

        for tag, attrs in consent_selectors:
            element = soup.find(tag, attrs)
            if element:
                logging.info("Found cookie consent form, attempting to accept...")
                consent_url = self._get_action_url(element, url)
                return self.submit_consent(consent_url)
        return False

    def _get_action_url(self, form_element, base_url):
        form_action = form_element.get('action', '')
        return requests.compat.urljoin(base_url, form_action)

    def submit_consent(self, consent_url):
        """Submit consent form"""
        try:
            response = self.crawler.fetch(
                consent_url,
                verify_ssl=False,
                user_agent="Mozilla/5.0"
            )
            return response.ok
        except Exception as e:
            logging.error(f"Failed to submit consent: {e}")
            return False


class WebScrapingWorkflow:
    """

    """
    def __init__(self):
        self.crawler = CrawlerAgent()
        self.parser = ParserAgent()
        self.error_handler = ErrorHandlerAgent()
        self.cookie_manager = CookieManagerAgent(self.crawler)

    def scrape(self, url):
        """
        Orchestrate the scraping process

        Coordinates:
            - Request handling
            - Error recovery
            - Cookie management
            - Retry logic
        """
        max_retries = 2
        attempt = 0

        while attempt <= max_retries:
            try:
                logging.info(f"Scraping attempt {attempt + 1}/{max_retries + 1}")
                response = self.crawler.fetch(url)

                if self.error_handler.is_redirect(response, url):
                    url = response.url  # Update URL to redirected location

                soup = self.parser.parse(response.text)

                if self.error_handler.is_error_page(soup):
                    raise ContentError("Error content detected in page")

                if self.cookie_manager.handle_cookie_consent(soup, url):
                    logging.info("Cookie consent handled - retrying original request")
                    attempt -= 1  # Reset attempt counter
                    time.sleep(1)
                    continue

                return soup

            except PageNotFoundError as e:
                logging.error(f"Page not found: {e.url}")
                raise

            except Exception as e:
                logging.error(f"Scraping failed: {str(e)}")
                attempt += 1
                if attempt > max_retries:
                    raise ScrapeError(f"Failed after {max_retries} attempts")
                time.sleep(2 ** attempt)  # Exponential backoff


# Custom Exceptions
class PageNotFoundError(Exception):
    pass


class ParsingError(Exception):
    pass


class ContentError(Exception):
    pass


class ScrapeError(Exception):
    pass


# Usage Example
if __name__ == "__main__":
    scraper = WebScrapingWorkflow()
    try:
        result = scraper.scrape("https://example.com")
        print("Scraping successful!")
        print(f"Page title: {result.title.string}")
    except ScrapeError as e:
        print(f"Scraping failed: {str(e)}")