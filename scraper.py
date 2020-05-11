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



def scrapeElPais():
    noticiarios = [{'name': 'Sanidad', 'code': 'noticias/salud'}, {'name': 'Ciencia',
                                                                 'code': 'ciencia'}, {'name': 'Tecnologia', 'code': 'tecnologia'}]
    for noticiario in noticiarios:
        print('noticia')
        r = requests.get(f'https://elpais.com/{noticiario["code"]}/')
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            title = article.find('h2').text
            linkNoParsed = article.find('h2').find('a')['href']
            if(linkNoParsed[0] != '/'):
                link = article.find('h2').find('a')['href']
            else:
                link = 'https://elpais.com' + article.find('h2').find('a')['href']
            try:
                req = requests.get(link)
            except:
                continue
            
            soupArt = BeautifulSoup(req.text, 'html.parser')

            articleTagContainer = soupArt.find(
                'ul', {'class': 'tags_list'}
            )

            if articleTagContainer is None:
                continue

            tags = []
            for tag in articleTagContainer.find_all('a'):
                tags.append(tag.text)
            
            fecha1 = soupArt.find('time')
            if fecha1:
                fecha = fecha1['datetime']
            if fecha1 is None:
                fecha1 = soupArt.find('div', attrs={'class': 'place_and_time'})
                if(fecha1 != None):
                    fecha = fecha1.find('a').text
            if fecha1 is None:
                fecha = soupArt.find('a', attrs={'class': 'a_ti'}).text
            noticia = ''
            section = soupArt.find('section', attrs={'class': 'article_body'})
            if(section != None):
                everyP = section.find_all('p')
                for eachP in everyP:
                    noticia += eachP.text
            div = soupArt.find('div', attrs={'id': 'cuerpo_noticia'})
            if(div != None):
                everyP = div.find_all('p')
                for eachP in everyP:
                    noticia += eachP.text
            div = soupArt.find('div', attrs={'class': 'article_body'})
            if(div != None):
                everyP = div.find_all('p')
                for eachP in everyP:
                    noticia += eachP.text
            if(noticia == ''):
                continue
            
            doc = {
                'title': title,
                'categoria': noticiario['name'],
                'tags': tags,
                'noticia': noticia,
                'fecha': fecha
            }
            jsonDoc = json.dumps(doc)
            print(jsonDoc)
            path = os.getcwd()
            f = open(path + f'/El Pais/{noticiario["name"]}/{noticiario["name"]}.{fecha}.txt', 'w+')
            f.writelines(jsonDoc)
            f.close()
            req.close()


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
    # createDirectories()
    # scrapeElMundo()
    # scrapeElPais()
    scrape20Minutos()

scrapeAll()
