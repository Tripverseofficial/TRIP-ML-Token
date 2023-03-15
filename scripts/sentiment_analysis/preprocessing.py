import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from data.sentiments_analysis.preprocessing import preprocess_data

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

def preprocess_text(text):
    """
    Cleans and preprocesses the input text by removing unwanted characters, converting to lowercase, 
    tokenizing, removing stop words, and stemming.
    """
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize using NLTK's word_tokenize function
    tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    stemmed_tokens = [porter.stem(token) for token in tokens]  # Stemming using PorterStemmer
    return stemmed_tokens

def preprocess_dataframe(df, text_column):
    """
    Preprocesses the text in the specified column of the input dataframe.
    """
    df[text_column] = df[text_column].apply(lambda x: preprocess_text(x))
    return df
