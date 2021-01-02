
import requests
from bs4 import BeautifulSoup
import codecs
import os
import sys
from pytube import YouTube
from pytube import Playlist

# for i in range(1, 20):
#     url = 'https://kitap.kz/audio-book?page='
#     print('page',i)
#     url = url + str(i)
#     print(url)
#     r1 = requests.get(url, timeout=5, verify=False)
#     page = r1.content
#     soup1 = BeautifulSoup(page, 'html5lib')
#     news = soup1.find_all(class_ = 'book-item__block swiper-slide')
#     r1.close()

#     links = []

#     for j in range(len(news)):

#         link = news[j].find(class_ = 'book-item__link')
#         try:
#             links.append(link.get('href'))
#         except Exception:
#             print('Not an article')

#     for link in links:
#         print(link)
#         r2 = requests.get(link, timeout=5, verify=False)
#         print('accessed')
#         page = r2.content
#         print('got content')
#         soup = BeautifulSoup(page, 'lxml')
#         print('got soup')

#         text = soup.find('li')
#         print(text.contents)
    
        
#         extracting text 
#         text = text.get_text()
#         text.encode('unicode-escape').decode('utf-8')
#         r2.close()
#         filename = link.split('/')[-1][0:6] + '.txt'

#         with codecs.open(filename, 'w+', 'utf-8') as fp:
#             fp.write(text)


url = 'https://kitap.kz/book/4738/'

r1 = requests.get(url, timeout=5, verify=False)
page = r1.content
soup = BeautifulSoup(page, 'html5lib')

iframe = soup.find('iframe')
print (iframe)
print('found iframe')

response = requests.get('https://kitap.kz/book/4738/' + iframe.attrs['src'])
response = response.content

soup1 = BeautifulSoup(response, 'html5lib')
            
script = soup1.find_all('p')
text = script.text
# #text.encode('unicode-escape').decode('utf-8')
print (text)
r1.close()


# text = soup.find(class_ = 'calibre1')
# text = text.get_text()
# text.encode('unicode-escape').decode('utf-8')
# r2.close()
# filename = link.split('/')[-2] + '.txt'
# with codecs.open(filename, 'w+', 'utf-8') as fp:
#     fp.write(text)