from bs4 import BeautifulSoup
import requests
import json
import time
import datetime

SLEEP_TIME = 60*60*12
ERROR_SLEEP_TIME = 60*60*2

def get_html(url,data):
    response = requests.get(url, data)
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find("table", attrs={"id": "report"})
    trs = table.find("tr").find_next_siblings()
    for tr in trs:
        tds = tr.find_all("td")
        yield [
            tds[0].text.strip(),
            tds[1].text.strip(),
            tds[2].text.strip(),
            tds[3].text.strip(),
            tds[4].text.strip(),
            tds[5].text.strip(),
            tds[6].text.strip(),
            tds[7].text.strip(),
            tds[8].text.strip(),
        ]

def write_to_file(content):

    with open("result.txt", 'a', encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False)+"\n")

def get_page_nums():
    base_url = "http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search_content.jsp"
    date_time = datetime.date.fromtimestamp(time.time())
    data = {
        "ktrqjs": date_time,
    }
    while True:
        html = get_html(base_url, data)
        soup = BeautifulSoup(html, 'lxml')
        if soup.body.text.strip() == "System busy":
            print("The system is busy, the login is too frequent, and IP is blocked")
            time.sleep(ERROR_SLEEP_TIME)
            continue
        else:
            break
    res = soup.find("div", attrs={"class": "meneame"})
    page_nums = int(res.find('strong').text)
    if page_nums % 15 == 0:
        page_nums = page_nums//15
    else:
        page_nums = page_nums//15 + 1
    print("PageCount：", page_nums)
    return page_nums

def main():
    page_nums = get_page_nums()
    base_url = "http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search_content.jsp"
    while True:
        date_time = datetime.date.fromtimestamp(time.time())
        page_num = 1
        data = {
            "Current_Time": date_time,
            "Page": page_num
        }
        while page_num <= page_nums:
            print('Current time：', data['Current_Time'], '     Page：', data['Page'])
            while True:
                html = get_html(base_url, data)
                soup = BeautifulSoup(html, 'lxml')
                if soup.body.text.strip() == "System busy":
                    print("The system is busy, the login is too frequent, and IP is blocked")
                    time.sleep(ERROR_SLEEP_TIME)
                    continue
                else:
                    break
            res = parse_html(html)
            for i in res:
                write_to_file(i)
            print("Crawl out [%s] page, total [%s] pages" % (page_num, page_nums))
            page_num += 1
            data["Page"] = page_num
            time.sleep(1)
        else:
            print("Complete!")
        print("Sleep it......")
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
