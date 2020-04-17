from nltk.tokenize import word_tokenize
import preprocess as prep
import os
import json
import numpy as np
import math
from collections import Counter

alpha = 0.3
processed_text = []
processed_title = []
DF = {}
doc = 0
N = 0
tf_idf = {}
tf_idf_title = {}
total_vocab_size = 0
total_vocab = []

def extractor():
    global N
    for root, dirs, files in os.walk(os.getcwd()): #recorre todos los archivos
        for name in files:
            if name.endswith('.txt'):
                file = open(f'{root}/{name}', 'r', encoding="utf8", errors='ignore')
                text = json.loads(file.read().strip())
                file.close()

                processed_text.append(word_tokenize(str(prep.preprocess(text['noticia']))))
                processed_title.append(word_tokenize(str(prep.preprocess(text['title']))))
    N = len(processed_text)
    print(N)
    print('extractor')

def calculateDF():
    global total_vocab, total_vocab_size, DF
    print(N)
    for i in range(N):
        tokens = processed_text[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

        tokens = processed_title[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
    for i in DF:
        DF[i] = len(DF[i])

    total_vocab_size = len(DF)
    total_vocab = [x for x in DF]
        

def doc_freq(word):
    global doc
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

    for i in range(N):
    
        tokens = processed_text[i]
        
        counter = Counter(tokens + processed_title[i])
        words_count = len(tokens + processed_title[i])
        
        for token in np.unique(tokens):
            
            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log((N+1)/(df+1))
            
            tf_idf[doc, token] = tf*idf

        doc += 1

def calculateTFIDFTitle():
    global tf_idf_title, doc
    for i in range(N):
    
        tokens = processed_title[i]
        counter = Counter(tokens + processed_text[i])
        words_count = len(tokens + processed_text[i])

        for token in np.unique(tokens):
            
            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log((N+1)/(df+1)) #numerator is added 1 to avoid negative values
            
            tf_idf_title[doc, token] = tf*idf

        doc += 1

def merginWeights():
    global tf_idf
    for i in tf_idf:
        tf_idf[i] *= alpha
    for i in tf_idf_title:
        tf_idf[i] = tf_idf_title[i]

def callAll():
    global D
    extractor()
    calculateDF()
    calculateTFIDFTitle()
    merginWeights()
    D = np.zeros((N, total_vocab_size))
    for i in tf_idf:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = tf_idf[i]
        except:
            pass
    print(D)


def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def gen_vector(tokens):
    Q = np.zeros((len(total_vocab)))
    
    counter = Counter(tokens)
    words_count = len(tokens)

    query_weights = {}
    
    for token in np.unique(tokens):
        
        tf = counter[token]/words_count
        df = doc_freq(token)
        idf = math.log((N+1)/(df+1))

        try:
            ind = total_vocab.index(token)
            Q[ind] = tf*idf
        except:
            pass
    return Q

def cosine_similarity(k, query):
    #global D
    callAll()

    preprocessed_query = prep.preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
        
    d_cosines = []
    
    query_vector = gen_vector(tokens)
    print(query_vector)
    print(D)
    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))
        
    out = np.array(d_cosines).argsort()[-k:][::-1]
    
    print("")
    
    return out








print(cosine_similarity(20,"Coronao te lo meto por el"))