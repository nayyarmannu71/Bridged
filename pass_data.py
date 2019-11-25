from rq import Queue
from redis import Redis
from indeed_worker import crawl_indeed
import requests
from bs4 import BeautifulSoup


redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

headers = {
    'authority': 'www.indeed.co.in',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'referer': 'https://www.indeed.co.in/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'CTK=1dq9oikla9d32800; INDEED_CSRF_TOKEN=weLYhPaaNiUiB7eBrvZ5h4G6IXZpNcRv; hpnoproxy=1; mobile_pool_id=1af7e1; jasx_pool_id=9c4c03; _ga=GA1.3.739581769.1574433283; _gid=GA1.3.578468319.1574433283; JSESSIONID=B167E23CEA4D63A8F14519C6F08D4019.jasxB_lon-job72; _gcl_au=1.1.1046425040.1574433294; pjps=1; jobAlertPopoverShown=1; PREF="TM=1574434005449:L=Bengaluru+Karnataka"; JCLK=-1; UD="LA=1574434005:CV=1574433293:TS=1574433293:SG=608cdf9d34c4e9f9803b9f1306cc3a69"; RQ="q=content+writer&l=Bengaluru+Karnataka&ts=1574434005498:q=content+writer&l=Bengaluru%2C+Karnataka&ts=1574433488963"; jaSerpCount=3; PPN=1; _gat=1; LV="LA=1574434005:CV=1574433293:TS=1574433281"; gonetap=closed; ac="l:#q:f=gnrs&k=14&t=4954"',
}

# Give space while changing the value with format <city_name state_name>
location = "Bengaluru Karnataka"
# Change the job keyword with space between each keyword like <data engineer>
job_keyword = "Content Writer"


updated_location = ",+".join(location.split(' '))
updated_keyword = "+".join(job_keyword.split(' '))
new_url = "https://www.indeed.co.in/jobs?q={}&l={}".format(updated_keyword, updated_location)

r = requests.get(new_url, headers=headers)

soup = BeautifulSoup(r.content, 'html.parser')

total_page_count = int(soup.select("#searchCountPages")[0].text.replace('Page 1 of', '').replace('jobs', '').strip())


for page_no in range(0, total_page_count+1, 10):
    constructed_url = "{}&start={}".format(r.url, page_no)
    q.enqueue(crawl_indeed, constructed_url)
    print(constructed_url)

# for pages in soup.select(".pagination > a"):
#     if 'Next' in pages.text:
#         next_url = "https://www.indeed.co.in" + pages['href']
#         print(next_url)
#         r1 = requests.get(next_url, headers=headers)
#         with open("/Users/rahul/Desktop/test_file1.html", "wb") as fle:
#             fle.write(r1.content)
#     else:
#         next_url = "https://www.indeed.co.in" + pages['href']
#         print(next_url)
#         q.enqueue(crawl_indeed, str("https://www.indeed.co.in" + pages['href']))
