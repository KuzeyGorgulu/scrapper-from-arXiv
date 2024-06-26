import requests
from bs4 import BeautifulSoup
import urllib.parse

# Function to show article titles from arXiv
def show_article_titles(query):
    base_url = "https://arxiv.org/search/"
    params = {
        'query': query,
        'searchtype': 'all',
        'abstracts': 'show',
        'order': '-announced_date_first',
        'size': '50'
    }

    # Download HTML content
    response = requests.get(base_url, params=params)
    html_content = response.content

    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find article titles
    papers = soup.find_all('li', class_='arxiv-result')

    # Show titles with numbering
    for index, paper in enumerate(papers, start=1):
        title = paper.find('p', class_='title').text.strip()
        print(f"{index}. {title}")

    # Ask user to select a paper
    selected_index = int(input("\nEnter the number of the article you want to open: ")) - 1

    # Find URL of the selected paper
    selected_paper = papers[selected_index]
    paper_href = selected_paper.find('p', class_='list-title').find('a')['href']
    paper_url = urllib.parse.urljoin(base_url, paper_href)

    # Display selected paper title and URL
    print(f"\nSelected Paper: {papers[selected_index].find('p', class_='title').text.strip()}")
    print(f"URL: {paper_url}")

    # Ask user if they want to open the full version of the paper
    open_paper = input("\nDo you want to open the full version of the paper? (Y/N): ")
    if open_paper.lower() == 'y':
        try:
            # Directly open the paper URL
            response_paper = requests.get(paper_url)
            html_paper = response_paper.content
            soup_paper = BeautifulSoup(html_paper, 'html.parser')

            # Find the full text of the paper or the abstract if full text is not found
            full_text_div = soup_paper.find('div', class_='article')
            if full_text_div:
                full_paper = full_text_div.text.strip()
                print(f"\n{full_paper}")
            else:
                abstract_text = soup_paper.find('blockquote', class_='abstract').text.strip()
                print(f"\nAbstract:\n{abstract_text}\n")
                print("Unable to find the full text of the paper.")

        except Exception as e:
            print(f"Error opening the paper: {e}")

# Get search query from the user and call the function
search_query = input("Enter the search term to look up on arXiv (e.g., 'machine learning'): ")
show_article_titles(search_query)
