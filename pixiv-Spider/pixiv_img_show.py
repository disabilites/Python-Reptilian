from bs4 import BeautifulSoup
import requests
import re

class PixivShow(object):

    def __init__(self, url):
        self.url = url
        self.html_str = '<meta charset="utf-8" />' \
                        '<style>\n' \
                        'a{ text-decoration:none} body{background:#e4e7ee}\n' \
                        '</style>\n' \
                        '<div style = "width:960px; margin:0px auto;background:#fff">\n'\
                        '<h1 align="center">Pixiv高质量作品推荐</h1>\n'\
                        '<h4 align="center">组图、漫画请点击图片查看（需科学上网，科学上网' \
                        '<a href="http://cp.xqs.ch/" target="_blank">推荐</a>）原图可从页面底部连接下载（日榜）</h4>\n'

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'lxml')
        titleList = soup.findAll('a', attrs={'class': 'title'})
        images = re.compile(r'data-filter="thumbnail-filter lazy-image"data-src="(.+?.jpg)"')
        users = re.compile(r'"/member_illust.*?"')
        imgList = images.findall(html)
        userList = users.findall(html)
        return imgList, userList, titleList

    def get_Page(self, imgList, userList, titleList):
        for (url, user, title) in zip(imgList, userList, titleList):
            title = str(title)
            title = re.search('target="_blank">(.*?)</a>', title)
            user = 'https://www.pixiv.net' + user.replace('"', '')
            self.html_str += '<div style = "width:300px; display:inline-block; margin:10px 5px;text-align:center;">\n' \
                        '<a target="_blank" href="' + user + '' + '">' + '\n' + \
                        '   <img width ="230px" src="' + url + '">' + '\n' + \
                        '<h5>' + title.group(1) + '</h5>\n' \
                        '</a>\n' \
                        '</div>\n'
        self.html_str += '</div>'
        with open('pixiv.html', 'w', encoding='utf-8') as f:
            f.write(self.html_str)
            print('页面已保存')