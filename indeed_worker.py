import requests
from bs4 import BeautifulSoup
from urllib import unquote
import time
import random
import re


def crawl_indeed(url):
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

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_details = soup.find_all("div", class_="result")
    jobs = []

    for job_detail in job_details:
        job = dict()
        job['title'] = job_detail.select("#resultsCol div.result .title a[title]")[0]['title'].strip()
        job['company_name'] = job_detail.select("#resultsCol div.result .sjcl .company")[0].text
        job['job_location'] = job_detail.select("#resultsCol div.result .sjcl .location")[0].text
        if job_detail.select("#resultsCol div.result .salaryText"):
            job['salary_bracket'] = unquote(job_detail.select("#resultsCol div.result .salaryText")[0].text.strip())
            job_salary = re.sub(r'[^\w]', ' ', job_detail.select("#resultsCol div.result .salaryText")[0].text.strip()).replace('a year', '').replace('a month', '').strip().split('  ')[0]
            job['salary_checker'] = int(re.sub(r'\s+', '', job_salary))
        summary = []
        for job_summary in job_detail.select("#resultsCol div.result .summary li"):
            summary.append(job_summary.text)
        job['summary'] = '|'.join([sum for sum in summary])
        jobs.append(job)

    with open("data.json", "a") as fle:
        fle.write("{},\n".format(jobs))
    print(jobs)
    time.sleep(random.randint(3, 9))
