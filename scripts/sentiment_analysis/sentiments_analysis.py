import pandas as pd
import nltk
from data.sentiments_analysis.news_scraper import scrape_news
from data.sentiments_analysis.twitter_scraper import scrape_tweets
from data.sentiments_analysis.telegram_scraper import scrape_messages
from data.sentiments_analysis.preprocessing import preprocess_dataframe
from data.sentiments_analysis.sentiment_analysis import analyze_sentiment
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def perform_sentiment_analysis(data):
    # Initialize VADER sentiment analyzer
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()

    # Preprocess data
    data = preprocess_dataframe(data, 'text')

    # Create new dataframe to store sentiment scores
    sentiment_scores = pd.DataFrame(columns=['date', 'text', 'compound'])

    # Loop through each row of data and calculate sentiment score using VADER
    for index, row in data.iterrows():
        text = row['text']
        date = row['date']
        compound = analyze_sentiment(sid, text)['compound']
        sentiment_scores = sentiment_scores.append({'date': date, 'text': text, 'compound': compound}, ignore_index=True)

    # Sort sentiment scores by date
    sentiment_scores = sentiment_scores.sort_values('date')

    return sentiment_scores

# Example usage
if __name__ == "__main__":
    # Scrape data from all sources
    news_data = scrape_news('https://www.bbc.com/news')
    tweet_data = scrape_tweets('Bitcoin', 100)
    telegram_data = scrape_messages('Bitcoin', 100)

    # Concatenate dataframes
    data = pd.concat([news_data, tweet_data, telegram_data])

    # Perform sentiment analysis
    sentiment_scores = perform_sentiment_analysis(data)

    # Print results
    print(sentiment_scores)
