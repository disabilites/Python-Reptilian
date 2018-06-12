from pixiv_img_show import PixivShow
from pixiv_img_download import PixivImg
from multiprocessing import Pool, cpu_count
import filezip
import time
import os

if __name__ == "__main__":

    os.startfile('SSR启动路径')
    print('SSR启动')
    time.sleep(1)

    url = 'https://www.pixiv.net/ranking.php?mode=daily'
    referer = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
    now = time.strftime('%Y-%m-%d', time.localtime())
    path = './img/' + now + '/'
    filename = './img/' + now + '.zip'

    pixivimg = PixivImg(url=url, referer=referer, path=path)
    pixivshow = PixivShow(url=url)
    imgList, userList, titleList = pixivshow.get_data()
    pixivshow.get_Page(imgList, userList, titleList)

    for page in range(1, 3):
        params = {'p': str(page), 'format': 'json', 'tt': '9ab895a5bb3a3ccceb03da532c30dc16'}
        elem = pixivimg.get_elem(params)
        imgsList, titlesList, idList = pixivimg.get_data(elem)
        p = Pool(cpu_count())
        for img, title, id in zip(imgsList, titlesList, idList):
            p.apply_async(pixivimg.img_download, args=(img, title, id))
        p.close()
        p.join()

    filezip.filezip(filename, path)
    os.system("taskkill /F /IM ShadowsocksR-dotnet4.0.exe")
    print('完成！')
