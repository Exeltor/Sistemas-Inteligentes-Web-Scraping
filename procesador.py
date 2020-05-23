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
        distancias.append({"distance": cosine_similarity(query, noticia["noticia"])[0][0], "name": noticia["nombre"]})
    return distancias

def distanceKey(distancia):
    return distancia['distance']

def search(textQuery, number=500):
    noticias = extractor()
    query, noticias = procesado(textQuery, noticias)
    distancias = calcDistancia(query, noticias)
    distancias.sort(key=distanceKey, reverse=True)
    return distancias[:int(number)]

def extractorTAGS():
    noticias=[]
    for root, dirs, files in os.walk(os.getcwd()): #recorre todos los archivos
        for name in files:
            if name.endswith('.txt'):
                file = open(f'{root}/{name}', 'r', encoding="utf8", errors='ignore')
                text = json.loads(file.read().strip())
                file.close()

                noticias.append({"tags": text['tags'], "nombre": f'{root}/{name}'})
    return noticias

def procesadoTAGS(tagsQuery, noticias):
    for i in range(len(tagsQuery)):
        tagsQuery[i] = tagsQuery[i].lower()
        tagsQuery[i] = tagsQuery[i].strip()
        tagsQuery[i] = tagsQuery[i].replace(" ", "-")
    for i in range(len(noticias)):
        for j in range(len(noticias[i]["tags"])):
            noticias[i]["tags"][j] = noticias[i]["tags"][j].lower()
            noticias[i]["tags"][j] = noticias[i]["tags"][j].strip()
            noticias[i]["tags"][j] = noticias[i]["tags"][j].replace(" ", "-")
    return tagsQuery, noticias

def calcDistanciaTAGS(query, noticia):
    print(query)
    print(noticia)
    coincidencias = len(set(query).intersection(noticia))
    return (2 * coincidencias) / (len(query) + len(noticia))

def forDistanciaTAGS(query, noticias):
    distancias = []
    for noticia in noticias:
        distancias.append({"distance": calcDistanciaTAGS(query, noticia["tags"]), "name": noticia["nombre"]})
    print(distancias)
    return distancias

def similaritiesTAGS(tagsQuery, number=500):
    noticias = extractorTAGS()
    tagsQuery = eval(tagsQuery)
    query, noticias = procesadoTAGS(tagsQuery, noticias)
    distancias = forDistanciaTAGS(query, noticias)
    distancias.sort(key=distanceKey, reverse=True)
    return distancias[:int(number)]