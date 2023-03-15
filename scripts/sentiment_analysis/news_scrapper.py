import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_news(url):
    # Send a request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the news article containers on the page
    articles = soup.find_all('article')

    # Create an empty list to store the data
    news_data = []

    # Loop through each article container and extract the relevant information
    for article in articles:
        # Extract the date
        date = article.find('time')['datetime']

        # Extract the title
        title = article.find('h2').text.strip()

        # Extract the text
        text = article.find('div', {'class': 'description'}).text.strip()

        # Append the data to the list
        news_data.append([date, title, text])

    # Convert the list into a pandas DataFrame
    df = pd.DataFrame(news_data, columns=['date', 'title', 'text'])

    return df
