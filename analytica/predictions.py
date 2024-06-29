from analytica import sess, roberta_tokenizer
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

from analytica.scraping import get_reviews
from analytica import stopwords


from sklearn.feature_extraction.text import CountVectorizer
from analytica.scraping import get_reviews

import re


def negation_handler(review):
    # Handle specific contractions first
    review = re.sub(r"won't", "will not", review)
    review = re.sub(r"can't", "can not", review)
    review = re.sub(r"don't", "do not", review)
    review = re.sub(r"shouldn't", "should not", review)
    review = re.sub(r"needn't", "need not", review)
    review = re.sub(r"hasn't", "has not", review)
    review = re.sub(r"haven't", "have not", review)
    review = re.sub(r"weren't", "were not", review)
    review = re.sub(r"mightn't", "might not", review)
    review = re.sub(r"didn't", "did not", review)
    review = re.sub(r"doesn't", "does not", review)
    # Handle general case of n't to not
    review = re.sub(r"n\'t", " not", review)
    return review

def clean_text(text):
    # Remove punctuation and convert to lowercase
    # text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def get_top_text_bysize(corpus, ngram=(3, 3), top_num=10, stop_words='english'):
    # Process the corpus with negation handler
    processed_corpus = [negation_handler(doc) for doc in corpus]
    
    # Clean the corpus
    cleaned_corpus = [clean_text(doc) for doc in processed_corpus]
    
    # Use predefined stop words if 'english' is specified
    stop_words = set(stopwords)
    stop_words.discard('not')
    stop_words = list(stop_words)  # Ensure 'not' is not in the stop words list

    vec = CountVectorizer(ngram_range=ngram, stop_words=stop_words)
    bag_of_words = vec.fit_transform(cleaned_corpus)
    word_counts = np.array(bag_of_words.sum(axis=0))[0]
    x = {word: count for word, count in zip(vec.get_feature_names_out(), word_counts)}
    top_ngrams = pd.Series(x).sort_values(ascending=False).head(top_num)
    return top_ngrams


# Initialize tokenizer and model session
input_names = ['input_ids', 'attention_mask']

def get_sentiments(sentences):
    inp = roberta_tokenizer(sentences,
                            padding="max_length", truncation=True,
                            return_tensors='np', max_length=200)
    
    input_feed = {input_name: inp[input_name].astype(np.int32) for input_name in input_names}
    
    result = sess.run(None, input_feed)
    result = np.argmax(result, axis=-1)
    result = list(zip(sentences, result[0]))
    return result























