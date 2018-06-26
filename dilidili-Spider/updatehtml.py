import re
import datetime
import logging

def update():
    logging.basicConfig(filename='program.log', level=logging.INFO)

    with open('result.html', 'r', encoding='utf-8') as f:
        html = f.read()

    str_html = str(html)
    video_pattern = re.compile('href="/anime')
    image_pattern = re.compile('src="/uploads')
    li_attr = str(re.search('<li class=.*"elmnt-.*?"', html).group())
    video_pos = 0
    image_pos = 0
    str_html = str_html.replace(li_attr, li_attr + ' style="list-style-type:none;"')

    while video_pattern.search(html, video_pos):
        video_str = video_pattern.search(html, video_pos)
        str_html = str_html.replace(video_str.group(), 'href="http://www.dilidili.wang/anime')
        video_pos = video_str.span()[1]

    while image_pattern.search(html, image_pos):
        image_str = image_pattern.search(html, image_pos)
        str_html = str_html.replace(image_str.group(), 'src="http://www.dilidili.wang/uploads')
        image_pos = image_str.span()[1]

    with open('result.html', 'w', encoding='utf-8') as f:
        f.write(str_html)

    logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '：页面属性替换成功！')

update()

