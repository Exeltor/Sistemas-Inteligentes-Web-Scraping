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
    categorias = [
        {'name': 'Salud', 'endpoint': 'ciencia-y-salud/salud.html'},
        {'name': 'Ciencia', 'endpoint': 'ciencia-y-salud/ciencia.html'},
        {'name': 'Tecnologia', 'endpoint': 'tecnologia.html'}
    ]

    for categoria in categorias:
        r = requests.get(f'https://www.elmundo.es/{categoria["endpoint"]}')
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
                
                dateTime = article.find('time')['datetime']
                doc = {
                    'title': header.text,
                    'categoria': categoria['name'],
                    'noticia': articleBody.text,
                    'fecha': dateTime
                }
                jsonDoc = json.dumps(doc)
                path = os.getcwd()
                f = open(path + f'/El Mundo/{categoria["name"]}/{categoria["name"]}.{dateTime}.txt', 'w+', encoding='utf-8')
                f.writelines(jsonDoc)
                f.close()



def scrapeElPais():
    print('el pais')
    noticiarios = [{'name': 'Sanidad', 'code': 'noticias/salud'}, {'name': 'Ciencia',
                                                                 'code': 'ciencia'}, {'name': 'Tecnologia', 'code': 'tecnologia'}]
    for noticiario in noticiarios:
        r = requests.get(f'https://elpais.com/{noticiario["code"]}/')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            title = article.find('h2').text
            try:
                link = 'https://elpais.com' + article.find('h2').find('a')['href']
                req = requests.get(link)
            except:
                print(link)
            try:
                link = article.find('h2').find('a')['href']
                req = requests.get(link)
            except:
                print(link)
            
            soupArt = BeautifulSoup(req.text, 'html.parser')
            try:
                fecha = soupArt.find('time')['datetime']
            except:
                print('no fecha time')
            try:
                fecha = soupArt.find('div', attrs={'class': 'place_and_time'}).find('a').text
            except:
                print('no fecha div')
            section = soupArt.find('section', attrs={'class': 'article_body'})
            if(section != None):
                everyP = section.find_all('p')
                noticia = ''
                for eachP in everyP:
                    noticia += eachP.text
            div = soupArt.find('div', attrs={'id': 'cuerpo_noticia'})
            if(div != None):
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
    categorias = [
        {'name': 'Salud', 'endpoint': 'salud/'},
        {'name': 'Ciencia', 'endpoint': 'ciencia/'},
        {'name': 'Tecnologia', 'endpoint': 'tecnologia/'}
    ]

    for categoria in categorias:
        r = requests.get(f'https://www.20minutos.es/{categoria["endpoint"]}')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            titleContainer = article.find('div', { 'class': 'media-content' })
            hyperLink = titleContainer.find('a')
            articleLink = hyperLink['href']
            articleTitle = hyperLink.text
            titleClean = articleTitle.strip()
            print(titleClean)
            articlePage = requests.get(articleLink)
            parsedPage = BeautifulSoup(articlePage.text, 'html.parser')
            dateTime = parsedPage.find('span', { 'class': 'article-date' })
            if dateTime is None:
                continue

            articleSection = parsedPage.find('article', { 'class': 'article-body' })
            if articleSection is None:
                continue

            articleContent = articleSection.find('div', { 'class': 'article-text' })
            if articleContent is None:
                continue

            noticia = articleContent.text

            doc = {
                'title': titleClean,
                'categoria': categoria['name'],
                'noticia': noticia,
                'fecha': dateTime.text
            }
            jsonDoc = json.dumps(doc)
            path = os.getcwd()
            f = open(path + f'/20 Minutos/{categoria["name"]}/{categoria["name"]}.{dateTime.text}.txt', 'w+')
            f.writelines(jsonDoc)
            f.close()



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
    #scrapeElMundo()
    #scrapeElPais()
    scrape20Minutos()


scrapeAll()
