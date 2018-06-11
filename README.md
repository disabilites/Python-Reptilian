# Python-Reptilian
## 爬虫实践记录


### 1、dytt8-Reptilian.py：
[dytt8-Spider.py](https://github.com/disabilites/Python-Spider/blob/master/dytt8-Spider.py) | [电影天堂“新片精品”](http://www.dytt8.net/)板块的电影下载链接和电影标题
  
### 2、hshfy-Spider：
[hshfy-Spider](https://github.com/disabilites/Python-Spider/tree/master/hshfy-Spider) | [上海高级人民法院](http://www.hshfy.sh.cn/shfy/gweb2017/index.html)公开的[开庭公告](http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search_content.jsp)，并写入txt文件
  
### 3、dilidili-Spider：
[dilidili-Spider](https://github.com/disabilites/Python-Spider/tree/master/dilidili-Spider) | [嘀哩嘀哩](http://www.dilidili.wang/)的番剧推送板块，保存为html文件，并发送到指定邮箱
  
### 4、pixiv-Spider：
[pixiv.py](https://github.com/disabilites/Python-Spider/blob/master/pixiv-Spider/pixiv.py) | 爬取[P站（pixiv）](https://www.pixiv.net/)（需翻墙）的排行榜，抓图每个作品的展示图，介绍页，标题，并保存为html文件。如需要下载原图，可通过替换原图URL，并通过作品介绍页面发送请求，即可下载。否则会出现403错误。
  
[pixiv_img_download.py](https://github.com/disabilites/Python-Spider/blob/master/pixiv-Spider/pixiv_img_download.py) | 下载pixiv日榜，需要爬取周榜或月榜更换URL即可。
  
### 5、music163-Spider：
[music163-Spider.py](https://github.com/disabilites/Python-Spider/blob/master/music163-Spider/music163-Spider.py) | 爬取[网易云歌单](http://music.163.com/discover/playlist)（需去掉URL中的#）中的歌曲标题，歌手名字，歌曲链接以及封面链接（可设置time.sleep()防止爬取过快被封IP）。保存为js文件主要是为了配合[Aplayer播放器](https://aplayer.js.org/#/zh-Hans/ )使用，需要下载可使用下面的程序

[music163-Spider.py](https://github.com/disabilites/Python-Spider/blob/master/music163-Spider/music163-Spider.py) | 下载歌单中的歌曲（有版权限制的无法下载，time.sleep()同上）
