from multiprocessing import Pool, cpu_count
import requests
import re
import time
import os

class PixivImg(object):

    def __init__(self, url, path, referer):
        object.__init__(self)
        self.url = url
        self.path = path
        self.referer = referer
        self.err_strList = ['/', '\\', '<', '>', '|', ':', '?', '*', '"']
        self.re_strList = ['／', '＼', '〈', '〉', '｜', '：', '？', '﹡', '“']
        isExists = os.path.exists(self.path)

        if not isExists:
            os.makedirs(path)
            print(self.path + '创建目录成功')
        else:
            print(self.path + '已存在')

    def get_elem(self, params):
        Page = requests.get(self.url, params=params, timeout=2)
        elem = str(Page.json()['contents'])  # 处理json文件 然后转换为字符串类型
        return elem

    def get_data(self, elem):
        img = re.compile(r'\'url\': \'(.+?.jpg)\'')
        title = re.compile(r'\'title\': \'(.*?)\'')
        id = re.compile(r'/([0-9]+)_p0')
        imgList = img.findall(elem)
        titleList = title.findall(elem)
        idList = id.findall(elem)
        return imgList, titleList, idList

    def img_download(self, img, title, id):
        img = img.replace(r'c/240x480/img-master', 'img-original')
        img = img.replace(r'_master1200', '')

        for errstr in title:
            if errstr in self.err_strList:
                index = self.err_strList.index(errstr)
                title = title.replace(errstr, self.re_strList[index])

        referer = self.referer + id
        headers = {'referer': referer}
        data = requests.get(img, headers=headers)
        if data.status_code == (404 or 403):
            img = img.replace(r'jpg', 'png')
            data = requests.get(img, headers=headers)
            with open(self.path + title + '.png', 'wb') as f:
                f.write(data.content)
            print(title, '下载完成')
        else:
            with open(self.path + title + '.jpg', 'wb') as f:
                f.write(data.content)
            print(title, '下载完成')

if __name__ == "__main__":

    url = 'https://www.pixiv.net/ranking.php?mode=daily'
    referer = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
    now = time.strftime('%Y-%m-%d', time.localtime())
    path = './img/' + now + '/'
    pixiv = PixivImg(url=url, referer=referer, path=path)

    for page in range(1, 3):
        params = {'p': str(page), 'format': 'json', 'tt': '9ab895a5bb3a3ccceb03da532c30dc16'}
        Elem = pixiv.get_elem(params)
        imgList, titleList, idList = pixiv.get_data(Elem)
        p = Pool(cpu_count())
        for title, img, id in zip(titleList, imgList, idList):
            p.apply_async(pixiv.img_download, args=(img, title, id))
        p.close()
        p.join()
