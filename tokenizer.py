import os, json, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.metrics import edit_distance
import numpy as np
from nltk.internals import Counter

sw = stopwords.words('spanish')

def df():
    DF = {}
    for i in range(len(processed_text)):
        tokens = processed_text[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

def tfIDF():
    tf_idf = {}
    for i in range(N):
        tokens = processed_text[i]
        counter = Counter(tokens + processed_title[i])
        for token in np.unique(tokens):
            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log(N/(df+1))
            tf_idf[doc, token] = tf*idf

def recorrerTXT():
    articulos = []
    for root, dirs, files in os.walk(os.getcwd()): #recorre todos los archivos
        for name in files:
            if name.endswith('.txt'):
                articulos.append(f'{root}/{name}')

def tokenizador(query):
    metric_list = []
    for root, dirs, files in os.walk(os.getcwd()): #recorre todos los archivos
        for name in files:
            if name.endswith('.txt'): # entramos solo en los que son txt, los que hemos creado nosotros
                fjson = json.load(open(f'{root}/{name}')) # leemos los datos en formato json de los txt
                rawText = f'{fjson["title"]} \n {fjson["noticia"]}' # concatenando el titulo mas la noticia
                tokens = word_tokenize(rawText, "spanish",preserve_line=True)
                clean_tokens = tokens[:]
                for token in tokens:
                    if token in sw:
                        clean_tokens.remove(token) #quitamos las stopwords
                final_tokens = stem(clean_tokens)
                doc = {
                    'name': f'{root}/{name}',
                    'distance': edit_distance(query, final_tokens)
                }
                metric_list.append(doc)

    return metric_list


def stem(tokens):
    spanish_stemmer = SnowballStemmer('spanish')
    lista = tokens[:]
    for palabra in tokens:
        lista.append(spanish_stemmer.stem(palabra))

    return lista

# A function to do counting sort of arr[] according to 
# the digit represented by exp. 
def countingSort(arr, exp1): 
  
    n = len(arr) 
  
    # The output array elements that will have sorted arr 
    output = [0] * (n) 
  
    # initialize count array as 0 
    count = [0] * (10) 
  
    # Store count of occurrences in count[] 
    for i in range(0, n): 
        index = int(arr[i]['distance']/exp1) 
        count[ (index)%10 ] += 1
  
    # Change count[i] so that count[i] now contains actual 
    #  position of this digit in output array 
    for i in range(1,10): 
        count[i] += count[i-1] 
  
    # Build the output array 
    i = n-1
    while i>=0: 
        index = int(arr[i]['distance']/exp1) 
        output[ count[ (index)%10 ] - 1] = arr[i]
        count[ (index)%10 ] -= 1
        i -= 1
  
    # Copying the output array to arr[], 
    # so that arr now contains sorted numbers 
    i = 0
    for i in range(0,len(arr)): 
        arr[i] = output[i] 
  
# Method to do Radix Sort 
def radixSort(arr): 
    max1 = 0
    # Find the maximum number to know number of digits
    for index in arr:
        if(index['distance'] > max1):
            max1 = index['distance']
  
    # Do counting sort for every digit. Note that instead 
    # of passing digit number, exp is passed. exp is 10^i 
    # where i is current digit number 
    exp = 1
    while max1/exp > 0: 
        countingSort(arr,exp) 
        exp *= 10

def tokenizerQ(texto):
    print("pollon")
    
def search(texto):
    text = tokenizerQ(texto)
    lista = tokenizador(text)
    radixSort(lista)
    return lista

