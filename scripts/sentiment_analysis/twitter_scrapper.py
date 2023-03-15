import tweepy
import pandas as pd

# Twitter API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Function to scrape tweets
def scrape_tweets(query, count):
    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Scrape tweets
    tweets = api.search(q=query, lang="en", tweet_mode="extended", count=count)

    # Store tweets in a dataframe
    tweet_list = [[tweet.created_at, tweet.full_text, tweet.user.screen_name] for tweet in tweets]
    tweet_df = pd.DataFrame(tweet_list, columns=['date', 'text', 'user'])

    return tweet_df
