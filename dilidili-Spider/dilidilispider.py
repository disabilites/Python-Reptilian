import re
import requests
import datetime
import logging
from bs4 import BeautifulSoup

video_pattern = re.compile('/.*?\?1')
image_pattern = re.compile('/.*?\.jpg')
Week = {0: "'elmnt-one'", 1: 'elmnt-two', 2: 'elmnt-three', 3: 'elmnt-four', 4: 'elmnt-five',
        5: 'elmnt-six', 6: 'elmnt-seven'}
logging.basicConfig(filename='program.log', level=logging.INFO)

def get_url(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    week = Week[datetime.datetime.now().weekday()]
    li = soup.find('li', attrs={'class': week})
    return li

def save_html(html):
    with open('result.html', 'w', encoding='utf-8') as f:
        f.write('<link href="http://www.dilidili.wang/css/style.css" rel="stylesheet" type="text/css">' + '\n' +
                '<meta name = "viewport" content = "width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=2.0, user-scalable=yes" />'
                + '\n' + str(html))

def main(url):
    start_html = get_url(url)
    end_html = parse_html(start_html)
    save_html(end_html)
    logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '：获取页面成功！')
