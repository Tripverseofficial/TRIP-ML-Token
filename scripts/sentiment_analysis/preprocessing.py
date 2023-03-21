import re
import spacy
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from spacy.lang.en import English

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = nltk.WordNetLemmatizer()
parser = English()

def preprocess_text(text, language='english'):
    """
    Cleans and preprocesses the input text by removing unwanted characters, converting to lowercase,
    tokenizing, removing stop words, and lemmatizing or stemming based on the language.
    """
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    doc = parser(text)
    if language == 'english':
        tokens = [token.lemma_ if token.lemma_ != "-PRON-" else token.text for token in doc]
    else:
        tokens = [token.text for token in doc]
    tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    if language == 'english':
        tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]  # Lemmatization
    else:
        porter = nltk.PorterStemmer()
        tokens = [porter.stem(token) for token in tokens]  # Stemming using PorterStemmer
    return tokens

def get_wordnet_pos(word):
    """
    Maps POS tag to first character used by WordNetLemmatizer.
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def preprocess_dataframe(df, text_column, language='english'):
    """
    Preprocesses the text in the specified column of the input dataframe.
    """
    df[text_column] = df[text_column].apply(lambda x: preprocess_text(x, language))
    return df
