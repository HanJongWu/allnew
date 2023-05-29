import requests
import json
import pandas as pd
from datetime import datetime, timedelta
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


url = 'http://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'


# "%Y%m%d"는 strftime 메서드에서 사용되는 형식 지정자(format specifier)입니다.
# 각 지정자는 날짜 및 시간 값의 특정 부분을 나타내며,
# %Y는 4자리 연도, %m은 2자리 월, %d는 2자리 일을 나타냅니다

today = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
print("today", today)

params = '?serviceKey=' + get_secret("data_apiKey")
params += '&pageNo=1'
params += '&mumOfRows=500'
params += '&apiType=JSON'
params += '&status_dt=' + str(today)

url += params
print("url", url)

response = requests.get(url)
print("response", response)
print('-' * 50)

contents = response.text
print("contents", type(contents))
print(contents)
print('-' * 50)

dict = json.loads(contents)
print("dict", type(dict))
print(dict)
print('-' * 50)

# json 끌어올때는 대괄호 []
items = dict['items'][0]
print("items", type(items))
print(items)
print('-' * 50)

item = ['gPntCnt', 'hPntCnt', 'accExamCnt', 'statusDt']

# validItem = {key: value for key, value in items.fromkeys(item).items()}
# print("validItem", type(validItem))

validItem = {}
for _ in item:
    validItem[_] = items[_]
print("validItem", type(validItem))
print(validItem)
print('-' * 50)

# dict로 가져왔기 떄문에 T를 붙이지 않아도 나옴
df = pd.DataFrame.from_dict(
    validItem, orient='index').rename(columns={0: "result"})
print("df", type(df))
print(df)
print('-' * 50)
