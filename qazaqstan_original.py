import requests
from bs4 import BeautifulSoup
import codecs
import os
import sys
import time
from selenium import webdriver
import moviepy.editor as mp


driver = webdriver.Chrome(r'/Users/alenadiev/Desktop/crawler/chromedriver')
driver.get('https://qazaqstan.tv/news')

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
try:
    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_id('loadButton').click()
    # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
except Exception:
    print ("no more scroll")
    
html = driver.page_source
soup = BeautifulSoup(html, features = 'lxml')
news = soup.find_all(class_ = 'col-lg-3 col-md-4 col-sm-4 col-6')
links = []
url = 'https://qazaqstan.tv'
for j in range(len(news)):
    try:
        links.append(url + news[j].find(class_='news-block video-hover').get('href'))
    except Exception:
        print('Not an article')
    print (links[-1])
for link in links:
    print (int(link[-6:-1]))
    if int(link[-6:-1]) > 116011:
        continue
    try: 
        print(link)
        r2 = requests.get(link, timeout=100)
        page = r2.content
        soup = BeautifulSoup(page, 'html5lib')
        print('got soup')
    except Exception:
        continue

         #Checking for video
    try:
        link_video = soup.find(class_ = 'ratio16x9').find('iframe').get('src')
        print(link_video)
        r_frame = requests.get(link_video, timeout=100)
        print('got rframe')
        page_frame = r_frame.content
        soup_frame = BeautifulSoup(page_frame, 'html5lib')
        print('got soup frame')

        iframexx = soup_frame.find_all('iframe')
        print('found iframe')
        for iframe in iframexx:

            response = requests.get('https://itube.kaztrk.kz' + iframe.attrs['src'])
            response = response.content

            iframe_soup = BeautifulSoup(response, 'html5lib')
    #             print(iframe_soup)
    #             print("\n")
    #             look at the iframe_soup and extract sources
            script = iframe_soup.find_all('script')[2]
    #             print(script.text)

            video_link = script.text[178:284]
            print(video_link)

    except Exception:
        print('No video')
        print("\n")
        continue

        #downloading video and converting it to audio
    try:
        chunk_size = 256
        r = requests.get(video_link)
        video_name = link.split('/')[-2] + '.mp4'
        with open(video_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = chunk_size):   
                f.write(chunk)
        video = mp.VideoFileClip(video_name)
        audio = video.audio
        audio.write_audiofile(link.split('/')[-2] + '.wav')

            #text extraction
        text = soup.find(class_ = 'article-content')
        text = text.get_text()
        text.encode('unicode-escape').decode('utf-8')
        r2.close()
        filename = link.split('/')[-2] + '.txt'
        with codecs.open(filename, 'w+', 'utf-8') as fp:
            fp.write(text)
    except Exception:
        continue