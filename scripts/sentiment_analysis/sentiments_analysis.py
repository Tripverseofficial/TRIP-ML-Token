import pandas as pd
from data.sentiments_analysis.news_scraper import scrape_news
from data.sentiments_analysis.twitter_scraper import scrape_tweets
from data.sentiments_analysis.telegram_scraper import scrape_messages
from data.sentiments_analysis.preprocessing import preprocess_text
from data.sentiments_analysis.sentiment_analysis import calculate_sentiment_scores
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def perform_sentiment_analysis(news_url, twitter_keyword, twitter_limit, telegram_keyword, telegram_limit):
    # Initialize VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Scrape data from all sources
    news_data = scrape_news(news_url)
    tweet_data = scrape_tweets(twitter_keyword, twitter_limit)
    telegram_data = scrape_messages(telegram_keyword, telegram_limit)

    # Concatenate dataframes
    data = pd.concat([news_data, tweet_data, telegram_data])

    # Preprocess data
    data['text'] = data['text'].apply(preprocess_text)

    # Calculate sentiment scores
    sentiment_scores = calculate_sentiment_scores(data, sid)

    # Sort sentiment scores by date
    sentiment_scores = sentiment_scores.sort_values('date')

    return sentiment_scores

def main():
    # Example usage
    news_url = 'https://www.bbc.com/news'
    twitter_keyword = 'Bitcoin'
    twitter_limit = 100
    telegram_keyword = 'Bitcoin'
    telegram_limit = 100

    sentiment_scores = perform_sentiment_analysis(news_url, twitter_keyword, twitter_limit, telegram_keyword, telegram_limit)

    # Print results
    print(sentiment_scores)

if __name__ == "__main__":
    main()
