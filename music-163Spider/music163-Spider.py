import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

base_url = '歌单URL，如：https://music.163.com/playlist?id=2246544491'

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

with open('test.js', 'w', encoding='utf-8') as f:
    f.write('music = [' + '\n')

info = {}
se = requests.session()
se = BeautifulSoup(se.get(base_url, headers=headers).content, 'lxml')
main = se.find('ul', {'class': 'f-hide'})

for music in main.find_all('a'):
    id = re.search('[0-9]+', music['href'])
    suburl = 'https://music.163.com' + music['href']
    html = requests.get(suburl, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    cover = soup.find('img')['src']
    artist = soup.find_all('a', {'class': 's-fc7'})[1].text
    info['name'] = music.text
    info['artist'] = artist
    info['url'] = 'http://music.163.com/song/media/outer/url?id=' + id.group() + '.mp3'
    info['cover'] = cover
    print(info['name'])
    print(info['artist'])
    print(info['url'])
    print(info['cover'])
    print('------------------------------------------------------------------------------------------------------')
    time.sleep(2)

    with open('test.js', 'a', encoding='utf-8') as f:
        f.write(str(info) + ',\n')

with open('test.js', 'a', encoding='utf-8') as f:
    f.write(']')