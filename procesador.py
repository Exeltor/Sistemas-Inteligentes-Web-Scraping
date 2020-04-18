from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os, json
from nltk.corpus import stopwords

sw = stopwords.words('spanish')
def extractor():
    noticias=[]
    for root, dirs, files in os.walk(os.getcwd()): #recorre todos los archivos
        for name in files:
            if name.endswith('.txt'):
                file = open(f'{root}/{name}', 'r', encoding="utf8", errors='ignore')
                text = json.loads(file.read().strip())
                file.close()

                noticias.append({"noticia": str(text['noticia']), "nombre": f'{root}/{name}'})
    return noticias

def procesado(query, noticias):
    vectorizer = TfidfVectorizer(stop_words=sw)
    query = vectorizer.fit_transform([str(query)])
    
    for i in range(len(noticias)):
        noticias[i]["noticia"] = vectorizer.transform([str(noticias[i]["noticia"])])
    return query, noticias
    
    
def calcDistancia(query, noticias):
    distancias = []
    for noticia in noticias:
        distancias.append({"distance": cosine_similarity(query, noticia["noticia"]), "name": noticia["nombre"]})
    return distancias

def distanceKey(distancia):
    return distancia['distance']

def search(textQuery, number=200):
    noticias = extractor()
    query, noticias = procesado(textQuery, noticias)
    distancias = calcDistancia(query, noticias)
    distancias.sort(key=distanceKey, reverse=True)
    return distancias[:int(number)]

    