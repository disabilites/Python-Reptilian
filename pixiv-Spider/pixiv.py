from bs4 import BeautifulSoup
import requests
import re
import time

url = 'https://www.pixiv.net/ranking.php?mode=weekly'

html_str = '<meta charset="utf-8" />' \
           '<style>\n' \
           'a{ text-decoration:none} body{background:#e4e7ee}\n' \
           '</style>\n' \
           '<div style = "width:960px; margin:0px auto;background:#fff">\n' \

html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
title_List = soup.findAll('a', attrs={'class': 'title'})
images = re.compile(r'data-filter="thumbnail-filter lazy-image"data-src="(.+?.jpg)"')
users = re.compile(r'"/member_illust.*?"')
Bef_imgs_url_List = images.findall(html)
Bef_users_url_List = users.findall(html)
start_time = time.time()
def get_data():
    global html_str
    for (url, user, title) in zip(Bef_imgs_url_List, Bef_users_url_List, title_List):
        title = str(title)
        title = re.search('target="_blank">(.*?)</a>', title)
        user = 'https://www.pixiv.net' + user.replace('"', '')
        html_str += '<div style = "width:300px; display:inline-block; margin:10px 5px;text-align:center;">\n' \
                    '<a target="_blank" href="' + user + '' + '">' + '\n' + \
                    '   <img width ="230px" src="' + url + '">' + '\n' + \
                    '<h5>' + title.group(1) + '</h5>\n' \
                    '</a>\n' \
                    '</div>\n'
    html_str += '</div>'
    with open('pixiv.html', 'w', encoding='utf-8') as f:
        f.write(html_str)
    print(html_str)
get_data()

