import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from data.sentiments_analysis.news_scraper import scrape_news
from data.sentiments_analysis.twitter_scraper import scrape_tweets
from data.sentiments_analysis.telegram_scraper import scrape_messages
from data.sentiments_analysis.preprocessing import preprocess_dataframe
from data.sentiments_analysis.sentiment_analysis import analyze_sentiment

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def perform_sentiment_analysis(data):
    data = preprocess_dataframe(data, 'text')
    sentiment_scores = pd.DataFrame(columns=['date', 'text', 'compound'])
    for index, row in data.iterrows():
        text = row['text']
        date = row['date']
        compound = analyze_sentiment(sid, text)['compound']
        sentiment_scores = sentiment_scores.append({'date': date, 'text': text, 'compound': compound}, ignore_index=True)
    sentiment_scores = sentiment_scores.sort_values('date')
    return sentiment_scores

if __name__ == "__main__":
    news_data = scrape_news('https://www.bbc.com/news')
    tweet_data = scrape_tweets('Bitcoin', 100)
    telegram_data = scrape_messages('Bitcoin', 100)
    data = pd.concat([news_data, tweet_data, telegram_data])
    sentiment_scores = perform_sentiment_analysis(data)
    print(sentiment_scores)
