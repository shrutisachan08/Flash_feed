from newsapi import NewsApiClient
from rich.console import Console
from rich.markdown import Markdown
import requests
from bs4 import BeautifulSoup

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

# Extract article content from URL
def extract_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the article's title (usually in an <h1> tag)
        title = soup.find('h1').get_text()

        # Extract the main content (e.g., in <p> tags)
        paragraphs = soup.find_all('p')
        content = "\n".join([para.get_text() for para in paragraphs])

        return title, content
    except Exception as e:
        console.print(f"[bold red]An error occurred while fetching the article:[/bold red] {e}")
        return None, None

# Main program
def main():
    query = input("Enter your search query: ")
    articles = fetch_news(query=query, language='en')

    if articles:
        for i, article in enumerate(articles):
            title = article['title']
            url = article['url']
            markdown_link = Markdown(f"[{i+1}. {title}]({url})")
            console.print(markdown_link)
            console.print(f"Description: {article['description']}")
            console.print("-" * 80)
        
        try:
            choice = int(input("Enter the number of the article to read more about: ")) - 1
            if 0 <= choice < len(articles):
                article_url = articles[choice]['url']
                title, content = extract_article_content(article_url)
                if title and content:
                    console.print(f"\n[bold underline]{title}[/bold underline]")
                    console.print(f"\n{content}")
                else:
                    console.print("[bold red]Failed to extract the article content.[/bold red]")
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a valid number.[/bold red]")
    else:
        console.print("[bold red]No articles found.[/bold red]")

if __name__ == "__main__":
    main()
