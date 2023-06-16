import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import current_app
import sqlite3
from requests.exceptions import SSLError
from .summarizer import summarize
# from .db import get_db

# URL to scrape
BASE_URL = "https://lite.cnn.com"

# number of articles to be scraped
NUM_SCRAPED = 20

summary = "summary"

# Get the current date in the required format
current_year_month = datetime.now().strftime("/%Y/%m")

def get_db():
    if 'db' not in current_app.extensions:
        current_app.extensions['db'] = sqlite3.connect(current_app.config['DATABASE'])

    return current_app.extensions['db']

def get_soup(url):
    # Send HTTP request
    print(f'scraping: {url}')
    # response = requests.get(url, verify=False)
    response = requests.get(url)
    # If successful, response status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        webpage = response.text

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(webpage, "html.parser")

        return soup

def get_article_content(soup):
    # Find the main content of the page - look specifically for elements with class "paragraph--lite"
    content = soup.find_all(class_='paragraph--lite')

    # Join together the text from each of these elements, separating them by two newlines
    text = "\n\n".join([p.get_text() for p in content[:-1]]) # filter out the last line
    return text

def get_article_headline(soup):
    title = soup.find(class_ = 'headline')
    text = title.get_text()
    return text
    
# # Get the soup for the base url
# soup = get_soup(base_url)

# # Find all 'a' HTML elements (or links)
# a_elements = soup.find_all('a')
# # for a in a_elements:
#     # Get the string contained in this HTML element
#     text = a.string

# Use content to store article content
# content = ""

def get_articles():
    soup = get_soup(BASE_URL)
    a_elements = soup.find_all('a')[:NUM_SCRAPED]
    
    with current_app.app_context():
        db = get_db()
    # Loop through all 'a' elements
        for a in a_elements:
            # Get the string contained in this HTML element
            link = a.get('href')
            if link and link.startswith(current_year_month):  # Filtering the news articles links by current date
            # print(f"Scraping {link}")
            # Construct full URL if it is a relative link
                link = BASE_URL + link
            # Get the BeautifulSoup object for this link
                try:
                    link_soup = get_soup(link)
                except SSLError as e:
                    print(f"Skipping URL: {link} due to SSLError: {str(e)}")
                    continue
                except requests.exceptions.ConnectionError as e:
                    print("Connection error occurred:", e)
                    continue
            # Get the article content for this link
                article_content = get_article_content(link_soup)
                article_title = get_article_headline(link_soup)
                article_summary = summarize(article_content)
                print(f'Saving Summary: {article_summary}')
                # print(f'about to save news with title{article_title}')
                try:
                    db.execute(
                        'INSERT INTO article (title, body, summary)'
                        'VALUES (?,?,?)',
                        (article_title, article_content, article_summary)
                    )
                    db.commit()
                    print('Article saved successfully!')
                except sqlite3.IntegrityError:
                    print('Article already exists. Skipping...')
                    
            # Sleep to avoid making too many requests in a short period of time
            # time.sleep(1)
        db.close()