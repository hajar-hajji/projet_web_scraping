import spacy
#print(spacy.__path__)
from spacy.lang.en.stop_words import STOP_WORDS
import string

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):

  # Convert text to lowercase and remove punctuation
  text = text.lower()
  text = ''.join([char for char in text if char not in string.punctuation])

  doc = nlp(text)

  # lemmatize and remove stopwords
  tokens_lemmatized = [token.lemma_ for token in doc if token.is_alpha and token.lemma_ not in STOP_WORDS]

  return ' '.join(tokens_lemmatized)

