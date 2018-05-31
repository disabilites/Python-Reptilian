import re
import requests
'''
    第一个爬虫程序，抓取电影天堂“新片精品”板块的电影下载地址 
'''
content = requests.get('http://www.dytt8.net/')
content.encoding = 'gb2312'                                             #http://www.dytt8.net/的字符编码
content = re.search('<!--{start:最新影视下载-->.*?<!--}end:最新下载--->', content.text, re.S).group()
pattern = re.compile("<td.*?>.*?<a.*?</a>.*?<a.*?href='(.*?)'>(.*?)</a><br/>", re.S)
results = re.findall(pattern, content)
for result in results:
    print('www.dytt8.net' + result[0], result[1])
