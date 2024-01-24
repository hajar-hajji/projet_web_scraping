import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
from transformers import pipeline
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

nlp = spacy.load('en_core_web_sm')

def preprocess(text):
  # Convert text to lowercase and remove punctuation
  text = text.lower()
  text = ''.join([char for char in text if char not in string.punctuation])
  doc = nlp(text)
  # Lemmatize and remove stopwords
  tokens_lemmatized = [token.lemma_ for token in doc if token.is_alpha and token.lemma_ not in STOP_WORDS]
  return ' '.join(tokens_lemmatized)

def analyze_sentiment(text):
    # Load the sentiment analysis pipeline using a pre-trained BERT-based model
    classifier = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    # Get the sentiment analysis result for the input (preprocessed) text
    sentiment_result = classifier(preprocess(text))[0]
    n_stars = int(sentiment_result['label'].split(' ')[0])
    # Determine the sentiment label based on the number of stars
    sentiment_label = 'Positive' if n_stars >= 4 else ('Negative' if n_stars <= 2 else 'Neutral')
    return sentiment_label, n_stars

def get_polarity_scores(text):
    # Preprocess text
    text = preprocess(text)
    # Sentiment analysis with TextBlob
    analysis_blob = TextBlob(text)
    # Get polarity with TextBlob
    blob_score = analysis_blob.sentiment.polarity
    # Sentiment analysis with NLTK
    sia = SentimentIntensityAnalyzer()
    # Get compound score with NLTK
    vader_score = sia.polarity_scores(text)['compound']
    return blob_score, vader_score