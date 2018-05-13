import dilidilispider
import updatehtml
import sendhtml
import datetime
import time
import logging

cleartime = 0
logging.basicConfig(filename='program.log', level=logging.INFO)

while True:
    now = datetime.datetime.now()
    if now.hour == 2 and now.minute == 0:
        dilidilispider.main('http://www.dilidili.wang/')
        updatehtml.update()
        sendhtml.send()
        logging.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '：本日推送完成！')
        cleartime = cleartime + 60
        time.sleep(60)
    if cleartime == 30*24*60*60:
        with open('program.log', 'w') as f:
            f.truncate()
        cleartime = 0
