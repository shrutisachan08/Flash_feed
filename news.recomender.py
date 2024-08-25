from newsapi import NewsApiClient
from rich.console import Console
from rich.markdown import Markdown

# Initialize the NewsApiClient with your API key
api_key = 'b8a03c825ab64da3bbf460c920f0b492'
newsapi = NewsApiClient(api_key=api_key)

console = Console()

# Fetch news articles based on a query
def fetch_news(query, language='en', from_date=None, to_date=None, page_size=10):
    try:
        response = newsapi.get_everything(
            q=query,  # Search query (e.g., a topic, keyword, or phrase)
            language=language,  # e.g., 'en' for English
            from_param=from_date,  # Start date (format: YYYY-MM-DD)
            to=to_date,  # End date (format: YYYY-MM-DD)
            page_size=page_size  # Number of articles to fetch
        )
        return response['articles']
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
        return []

# Example usage
query = input("Enter your search query: ")
articles = fetch_news(query=query, language='en')

# Print the fetched news articles with clickable titles
if articles:
    for article in articles:
        title = article['title']
        url = article['url']
        # Create a clickable hyperlink in the terminal
        markdown_link = Markdown(f"[{title}]({url})")
        console.print(markdown_link)
        console.print(f"Description: {article['description']}")
        console.print("-" * 80)
else:
    console.print("[bold red]No articles found.[/bold red]")
from newsapi import NewsApiClient
from rich.console import Console
from rich.markdown import Markdown

# Initialize the NewsApiClient with your API key
api_key = 'b8a03c825ab64da3bbf460c920f0b492'
newsapi = NewsApiClient(api_key=api_key)

console = Console()

# Fetch news articles based on a query
def fetch_news(query, language='en', from_date=None, to_date=None, page_size=10):
    try:
        response = newsapi.get_everything(
            q=query,  # Search query (e.g., a topic, keyword, or phrase)
            language=language,  # e.g., 'en' for English
            from_param=from_date,  # Start date (format: YYYY-MM-DD)
            to=to_date,  # End date (format: YYYY-MM-DD)
            page_size=page_size  # Number of articles to fetch
        )
        return response['articles']
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")
        return []


query = input("Enter your search query: ")
articles = fetch_news(query=query, language='en')


if articles:
    for article in articles:
        title = article['title']
        url = article['url']
        markdown_link = Markdown(f"[{title}]({url})")
        console.print(markdown_link)
        console.print(f"Description: {article['description']}")
        console.print("-" * 80)
else:
    console.print("[bold red]No articles found.[/bold red]")
