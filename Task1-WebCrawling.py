import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

HEADERS = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

section_query = 'physics news'.replace(' ', '-')
BASE_URL = 'https://phys.org/{0}/'.format(section_query)

items = []

def get_articles():
  for i in range(1, 5):
    print('Processing {0} ...'.format(BASE_URL + 'page{0}.html'.format(i)))
    response = requests.get(BASE_URL + 'page{0}.html'.format(i), headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('article', class_='sorted-article')

    for index, result in enumerate(results):
      article_title = result.h3.text
      link = result.find('img')['data-src']
      
      try:
        date_ago = result.find('p', class_='text-uppercase text-low').text

      except AttributeError:
        continue

      try:
        article_section = result.find('p', class_='mb-1 pr-1').text
        article_url = result.h3.a['href']

        items.append([article_title, date_ago, article_section, article_url])

      except AttributeError:
        continue

      try:
      
        with open(f'posts/{i}/{index}' + '.jpg', 'wb') as f:
          im = requests.get(link)
          f.write(im.content)
        print(f'File saved: page {i} of {index}')
      except AttributeError:
        continue
    sleep(1.5)

def save_datas_to_csv():
  df = pd.DataFrame(items, columns=['title', 'date', 'secton', 'url'])
  df.to_csv('posts/{0}.csv'.format(section_query), index=False)
    
if __name__ == '__main__':
    while True:
        get_articles()
        save_datas_to_csv()
