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

def get_music_info(soup, music, id, ):
    name = soup.find_all('a', {'class': 's-fc7'})[1].text + ' - ' + music.text
    url = 'http://music.163.com/song/media/outer/url?id=' + id.group() + '.mp3'
    data = requests.get(url)

    for errstr in name:
        if errstr in err_strList:
            index_name = err_strList.index(errstr)
            name = name.replace(errstr, re_strList[index_name])

    with open('./music/'  + name + '.mp3', 'wb') as f:
        f.write(data.content)
    #time.sleep()

if __name__ == "__main__":
    count = 1
    err_strList = ['/', '\\', '<', '>', '|', ':', '?', '*', '"']
    re_strList = ['／', '＼', '〈', '〉', '｜', '：', '？', '﹡', '“']
    se = requests.session()
    se = BeautifulSoup(se.get(base_url, headers=headers).content, 'lxml')
    main = se.find('ul', {'class': 'f-hide'})

    for data in get_music_sheet():
        get_music_info(data[0], data[1], data[2])
        print('已下载' + str(count) + '首')
        count += 1

    print('完成！')