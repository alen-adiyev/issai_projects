
import requests
from bs4 import BeautifulSoup
import codecs
import os
import sys
from pytube import YouTube
from pytube import Playlist

END = 3540



for i in range(3540, 3560, 20):
    url = 'https://khabar.kz/kk/news?start='
    print('page',i)
    url = url + str(i)
    print(url)
    r1 = requests.get(url, timeout=5, verify=False)
    page = r1.content
    soup1 = BeautifulSoup(page, 'html5lib')
    news = soup1.find_all(class_ = 'itemContainer')
    r1.close()

    links = []

    for j in range(len(news)):

        link = news[j].find(class_ = 'itemImage')
        try:
            links.append('https://khabar.kz/' + link.get('href'))
        except Exception:
            print('Not an article')

    for link in links:
        print(link)
        r2 = requests.get(link, timeout=5, verify=False)
        print('accessed')
        page = r2.content
        print('got content')
        soup = BeautifulSoup(page, 'html5lib')
        print('got soup')
        text = soup.find(class_ = 'itemFullText')
        
        #extracting audio from video
        try:
            video_link = soup.find('iframe').get('src')
            ytd = YouTube(video_link)
            video_file = ytd.streams.filter(only_audio = True).first().download()
            filename_video = link.split('/')[-1][0:6] + '.wav'
            os.rename(video_file, filename_video)
            print ("audio is downloaded")
        except Exception:
            print('No video')
            print("\n")
            continue
        
        #extracting text 
        text = text.get_text()
        text.encode('unicode-escape').decode('utf-8')
        r2.close()
        filename = link.split('/')[-1][0:6] + '.txt'

        with codecs.open(filename, 'w+', 'utf-8') as fp:
            fp.write(text)