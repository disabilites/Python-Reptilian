from bs4 import BeautifulSoup
import requests
import re
import time

base_url = '歌单URL，如：https://music.163.com/playlist?id=2246544491'

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def get_music_sheet():
    for music in main.find_all('a'):
        id = re.search('[0-9]+', music['href'])
        suburl = 'https://music.163.com' + music['href']
        html = requests.get(suburl, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        yield soup, music, id

def get_music_info(soup, music, id):
    global music_str
    name = music.text
    artist = soup.find_all('a', {'class': 's-fc7'})[1].text
    url = 'http://music.163.com/song/media/outer/url?id=' + id.group() + '.mp3'
    cover = soup.find('img')['src']
    info['name'] = name
    info['artist'] = artist
    info['url'] = url
    info['cover'] = cover
    music_str += str(info) + ',\n'
    #time.sleep()

if __name__ == "__main__":
    count = 1
    info = {}
    music_str = 'music = ' + '\n'
    se = requests.session()
    se = BeautifulSoup(se.get(base_url, headers=headers).content, 'lxml')
    main = se.find('ul', {'class': 'f-hide'})

    for data in get_music_sheet():
        get_music_info(data[0], data[1], data[2])
        print('已抓取' + str(count) + '首')
        count += 1

    music_str += ']'
    with open('test.js', 'w', encoding='utf-8') as f:
            f.write(music_str)

    print('完成！')