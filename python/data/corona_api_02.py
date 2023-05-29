import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from fastapi import FastAPI
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg


app = FastAPI()


@app.get('/')
async def healthCheck():
    return "OK"


@app.get('/hello')
async def Hello():
    return "Hello World~!!"


@app.get('/getdata')
async def getData(today=None):
    if today is None:
        today = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
        print(today)
    else:
        print(today)
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'

    # "%Y%m%d"는 strftime 메서드에서 사용되는 형식 지정자(format specifier)입니다.
    # 각 지정자는 날짜 및 시간 값의 특정 부분을 나타내며,
    # %Y는 4자리 연도, %m은 2자리 월, %d는 2자리 일을 나타냅니다

    today = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
    print(today)

    params = '?serviceKey=' + get_secret("data_apiKey")
    params += '&pageNo=1'
    params += '&numOfRows=500'
    params += '&apiType=JSON'
    params += '&status_dt=' + str(today)

    url += params
    print(url)

    response = requests.get(url)
    print(response)
    print('-' * 50)

    contents = response.text
    print(type(contents))
    print(contents)
    print('-' * 50)

    dict = json.loads(contents)
    print(type(dict))
    print(dict)
    print('-' * 50)

    items = dict['items'][0]
    print(type(items))
    print(items)
    print('-' * 50)

    item = ['gPntCnt', 'hPntCnt', 'accExamCnt', 'statusDt']

    validItem = {}
    for _ in item:
        validItem[_] = items[_]
    print(validItem)
    print('-' * 50)

    return validItem
