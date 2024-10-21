import os.path

import requests
from bs4 import BeautifulSoup

pages = int(input())
article_type = input()


def scrape():
    headers = {
        'Accept': 'text/html',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={pages}'
    response = requests.get(url, headers=headers)
    match response.status_code:
        case 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for i in range(1, pages+1):
                if not os.path.exists(f'Page_{i}'):
                    os.makedirs(f'Page_{i}')
                os.chdir(f'Page_{i}')
                articles = soup.find_all('article')
                links = []
                for article in articles:
                    link = article.find('a', attrs={'data-track-action': 'view article'})
                    if article.find('span', attrs={'data-test': 'article.type'}).text == article_type:
                        links.append(link.get('href'))

                for href in links:
                    url = f'https://www.nature.com{href}'
                    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
                    title = soup.find('h1', attrs={'class': 'c-article-magazine-title'}).text.strip()
                    title = title.replace(' ', '_').replace('?','')
                    content = soup.find('p', attrs={'class': 'article__teaser'}).text or "None"
                    with open(f'{title}.txt', 'wb') as f:
                        f.write(content.encode('utf-8'))
                        # print('Content saved.')
                os.chdir('..')

            print('Saved all articles.')

        case _:
            print(f'The URL returned {response.status_code}')


scrape()
