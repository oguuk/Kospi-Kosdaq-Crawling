import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup as bs
import re
from collections import defaultdict as dd

time = dd(int)
def KospiKosdaqgetData(code):
    today = ''.join(str(datetime.datetime.now().date()).split('-')) + '1530'
    url = 'https://finance.naver.com/sise/sise_index_time.naver?code={code}&thistime={thistime}&page={page}'.format(
        code=code, thistime=today, page=1)
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = bs(html, 'html.parser')
        lastPage = int(re.findall('page=\d+', str(soup.select('table.Nnavi tr > td.pgRR')))[0].split("page=")[1])
    else:
        raise print("페이지 접근 오류")

    for page in range(1, lastPage + 1):
        url = 'https://finance.naver.com/sise/sise_index_time.naver?code={code}&thistime={thistime}&page={page}'.format(
            code=code, thistime=today, page=page)
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        times = re.findall('[\d:]+', str(soup.select('table.type_1 tr td.date')))#시간 1분 1개 단위로 끊어서
        contents = re.findall('>[\d|.|,]+<', str(soup.select('td.number_1')))# >지수<, >변동량(천주)<, >거래량(천주)<, >거래대금(백만)< 4개 단위로 끊어서
        day_to_day = re.findall('nv|red|\d+.\d+', str(soup.select('td.rate_down > span'))) # 전일비 nv는 하락, red는 상승 2개 단위로 끊어서

        for idx,t in enumerate(times):
            time[t] = (contents[idx*4:(idx+1)*4] + day_to_day[idx*2:(idx+1)*2])

KospiKosdaqgetData("KOSPI")
KospiKosdaqgetData("KOSDAQ")
print(time)


