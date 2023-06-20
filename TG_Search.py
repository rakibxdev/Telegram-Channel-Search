import requests
from bs4 import BeautifulSoup
import re

def get_photos(channel, search):
    photos = []
    try:
        response = requests.get(f'https://t.me/s/{channel}?q={search}')
        if response.ok:
            results = response.text
            regex = re.findall(r'<a class="tgme_widget_message_photo_wrap [0-9_-]+ [0-9_-]+" href="([A-Za-z0-9_/:.-]+)" style="width:([0-9]+px);background-image:url\(\'([A-Za-z0-9_/:.-]+)', results)
            for r in regex:
                photos.append({'link': r[0], 'width': r[1], 'photo': r[2]})
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    
    return photos

def get_videos(channel, search):
    videos = []
    try:
        response = requests.get(f'https://t.me/s/{channel}?q={search}')
        if response.ok:
            soup = BeautifulSoup(response.content, "lxml")
            link = soup.find_all("a", {"class": "tgme_widget_message_video_player blured js-message_video_player"})
            videos = [l.attrs['href'] for l in link]
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    
    return videos

def get_files(channel, search):
    files = []
    try:
        response = requests.get(f"https://t.me/s/{channel}?q={search}")
        if response.ok:
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.find_all("a", {"class": "tgme_widget_message_document_wrap"})
            for t in text:
                title = t.text.strip().split('\n')[0]
                url = t.attrs['href'].strip().split('\n')[0]
                files.append({'title': title, 'link': url})
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    
    return files

def get_links(channel, search):
    links = []
    try:
        response = requests.get(f'https://t.me/s/{channel}?q={search}')
        if response.ok:
            soup = BeautifulSoup(response.content, "lxml")
            link = soup.find_all("a", {"class": "tgme_widget_message_link_preview"})
            links = [l.attrs['href'] for l in link]
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    
    return links

def search_channel():
    print('''
    ( 1 ) Photos
    ( 2 ) Videos
    ( 3 ) Links
    ( 4 ) Files
    ''')

    select = input('For what you want to search: ').strip()
    channel = input('Enter the channel username: ').strip().replace('@', '')
    search = input('Enter the keyword: ').strip()

    if select == '1':
        photos = get_photos(channel, search)
        if photos:
            print(photos)
        else:
            print('No photos found.')
    elif select == '2':
        videos = get_videos(channel, search)
        if videos:
            print(videos)
        else:
            print('No videos found.')
    elif select == '3':
        links = get_links(channel, search)
        if links:
            print(links)
        else:
            print('No links found.')
    elif select == '4':
        files = get_files(channel, search)
        if files:
            print(files)
        else:
            print('No files found.')
    else:
        print('Wrong number selected!')

search_channel()
