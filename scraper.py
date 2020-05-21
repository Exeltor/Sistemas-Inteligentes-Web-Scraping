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
                link = header.find('a')['href']
                result = requests.get(link)
                soup = BeautifulSoup(result.text)
                article = soup.find('article')
                articleBody = article.find(
                    'div', {'class': 'ue-l-article__body ue-c-article__body'})

                articleTagContainer = article.find(
                    'ul', {'class': 'ue-c-article__tags'}
                )
                if articleTagContainer is None:
                    continue

                tags = []
                for tag in articleTagContainer.find_all('a'):
                    tags.append(tag.text)

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
                    pass

                try:
                    unwantedDiv.extract()
                except:
                    pass

                try:
                    unwantedPremium.extract()
                    continue
                except:
                    pass

                try:
                    unwantedDivRelated.extract()
                except:
                    pass
                
                if not articleBody.text:
                    continue
            
                dateTime = article.find('time')['datetime']
                doc = {
                    'title': header.text,
                    'categoria': categoria['name'],
                    'tags': tags,
                    'noticia': articleBody.text,
                    'fecha': dateTime
                }
                jsonDoc = json.dumps(doc)
                path = os.getcwd()
                f = open(path + f'/El Mundo/{categoria["name"]}/{categoria["name"]}.{dateTime}.txt', 'w+', encoding='utf-8')
                f.writelines(jsonDoc)
                f.close()

def scrape20Minutos():
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

            articleTagContainer = parsedPage.find(
                'div', {'class': 'module module-related'}
            )

            if articleTagContainer is None:
                continue

            tags = []
            for tagItem in articleTagContainer.find_all('li', {'class': 'tag'}):
                tag = tagItem.find('a').text.strip()
                tags.append(tag)

            noticia = articleContent.text

            doc = {
                'title': titleClean,
                'categoria': categoria['name'],
                'tags': tags,
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
                   '/20 Minutos/Salud',
                   '/20 Minutos/Tecnologia',
                   '/20 Minutos/Ciencia']
    for directory in directories:
        if not os.path.exists(os.getcwd() + '' + directory):
            os.makedirs(os.getcwd() + '' + directory)


def scrapeAll():
    createDirectories()
    scrapeElMundo()
    scrape20Minutos()

scrapeAll()
