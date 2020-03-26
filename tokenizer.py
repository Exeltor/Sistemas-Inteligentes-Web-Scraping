import os, json
from nltk.corpus import stopwords


def tokenizeAll():
    sw = stopwords.words('spanish')
    tk = {}
    articlesTK = []
    for root, dirs, files in os.walk(os.getcwd()): #recorre todos los archivos
        for name in files:
            if name.endswith('.txt'): #entramos solo en los que son txt, los que hemos creado nosotros
                fjson = json.load(open(f'{root}/{name}')) #leemos los datos en formato json de los txt
                tokens = [i for i in fjson['title'].split()] + [t for t in fjson['noticia'].split()] #separamos en una lista cada palabra 
                clean_tokens = tokens[:] #duplicamos el array
                for token in tokens:
                    if token in sw:
                        clean_tokens.remove(token) #quitamos las stopwords
                tk['filename'] = f'{root}/{name}'
                tk['tokens'] = clean_tokens[:]
                articlesTK.append(tk) #añadimos todo a la lista que contiene todos los datos

    print(articlesTK)
    print(len(articlesTK))

tokenizeAll()