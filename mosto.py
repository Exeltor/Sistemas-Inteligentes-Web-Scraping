from bs4 import BeautifulSoup
import requests
import os
import json
"""
diario/
    categoria/
        categoria.fecha.001
            {
                title:
                categoria:
                noticia:
                fecha:
            }

"""
noticias = [{}]


def scrapeElMundo():
    print('el mundo')
    r = requests.get('https://www.elmundo.es/ciencia-y-salud/salud.html')
    webContent = r.text
    soup = BeautifulSoup(webContent)
    articles = soup.find_all('article')
    for article in articles:
        for header in article.find_all('header'):
            print(header.text)
            link = header.find('a')['href']
            result = requests.get(link)
            soup = BeautifulSoup(result.text)
            article = soup.find('article')
            articleBody = article.find(
                'div', {'class': 'ue-l-article__body ue-c-article__body'})

            if articleBody is None:
                continue
            # Unwanted tags
            unwantedDiv = articleBody.find(
                'div', {'class': 'ue-c-article__trust'})
            unwantedUl = articleBody.find('ul')
            unwantedPremium = articleBody.find(
                'div', {'class': 'ue-c-article__premium'})
            unwantedDivRelated = articleBody.find(
                'div', {'class': 'ue-c-article__related-news ue-l-article--top-separator'})
            unwantedDiv.extract()

            # try catch blocks no entiendo
            try:
                unwantedUl.extract()
            except:
                print('no ul')

            try:
                unwantedDiv.extract()
            except:
                print('no trust')

            try:
                unwantedPremium.extract()
            except:
                print('no premium')

            try:
                unwantedDivRelated.extract()
            except:
                print('no related')
            print(articleBody.text)


def scrapeElPais():
    print('el pais')
    noticiarios = [{'name': 'Sanidad', 'code': 'noticias/salud'}, {'name': 'Ciencia',
                                                                 'code': 'ciencia'}, {'name': 'Tecnologia', 'code': 'ciencia'}]
    for noticiario in noticiarios:
        r = requests.get(f'https://elpais.com/{noticiario["code"]}/')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            title = article.find('h2').text
            print(title)
            link = 'https://elpais.com' + article.find('h2').find('a')['href']
            fecha = article.find('time')['datetime']
            req = requests.get(link)
            soupArt = BeautifulSoup(req.text, 'html.parser')
            section = soupArt.find('section', attrs={'class': 'article_body'})
            if(section != None):
                print('section')
                everyP = section.find_all('p')
                noticia = ''
                for eachP in everyP:
                    noticia += eachP.text
            div = soupArt.find('div', attrs={'id': 'cuerpo_noticia'})
            if(div != None):
                print('div')
                everyP = div.find_all('p')
                noticia = ''
                for eachP in everyP:
                    noticia += eachP.text
            doc = {
                'title': title,
                'categoria': noticiario['name'],
                'noticia': noticia,
                'fecha': fecha
            }
            jsonDoc = json.dumps(doc)
            path = os.getcwd()
            f = open(path + f'/El Pais/{noticiario["name"]}/{noticiario["name"]}.{fecha}.txt', 'w+')
            f.writelines(jsonDoc)
            f.close()


def scrape20Minutos():
    print('20 minutos')


def createDirectories():
    directories = ['/El Mundo/Salud',
                   '/El Mundo/Tecnologia',
                   '/El Mundo/Ciencia',
                   '/El Pais/Sanidad',
                   '/El Pais/Tecnologia',
                   '/El Pais/Ciencia',
                   '/20 Minutos/Salud',
                   '/20 Minutos/Tecnologia',
                   '/20 Minutos/Ciencia']
    for directory in directories:
        if not os.path.exists(os.getcwd() + '' + directory):
            os.makedirs(os.getcwd() + '' + directory)


def scrapeAll():
    createDirectories()
    # scrapeElMundo()
    scrapeElPais()
    scrape20Minutos()


scrapeAll()
