import numpy as np
from nltk.corpus import stopwords
import num2words
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

sw = stopwords.words('spanish')
symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in sw and len(w) > 1:
            new_text = new_text + " " + w
    return new_text
    
def remove_punctuation(data):
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data
    
def remove_apostrophe(data):
    return np.char.replace(data, "'", "")
    
def stemming(data):
    spanish_stemmer = SnowballStemmer('spanish')
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + spanish_stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text


def remove_single_characters(data):
    new_text = ""
    for w in data:
        if len(w) > 1:
            new_text = new_text + " " + w
    return new_text
  
def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
   # data = remove_single_characters(data)
    data = convert_numbers(data)
    data = remove_stop_words(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)

    return data