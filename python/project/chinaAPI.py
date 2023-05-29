import pandas as pd
from pymongo import MongoClient
from fastapi import FastAPI
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import requests

# ENCODERS_BY_TYPE: pydantic의 JSON 인코더가 MongoDB [ObjectId]를 문자열(str)로 인코딩할 수 있도록 설정
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()  # FastAPI 애플리케이션을 생성

HOSTNAME = '192.168.1.25:27017'

client = mongo_client.MongoClient(f'mongodb://{HOSTNAME}')

print('Connected to Mongodb....')

mydb = client['project']
mycol1 = mydb['AllParticleDatas']
mycol2 = mydb['chinaData']


def save_quarters_data(year, quarters_data):
    # 연도별로 하위 디렉토리를 생성합니다.
    os.makedirs(str(year), exist_ok=True)

    # 각 분기별 JSON 데이터를 연도별 디렉토리에 저장합니다.
    for quarter, data in quarters_data.items():
        with open(os.path.join(str(year), f"{year}_{quarter}_data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


@app.get('/')
async def healthCheck():
    return "OK"


@app.get('/mongo_col2')
async def getMongo():
    return list(mycol2.find())


@app.get('/getmongo')
async def getMongo():
    return list(mycol2.find().limit(20))


@app.get('/getdata')
async def getdata():
    url = "http://localhost:5000/data"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data
    else:
        return {"error": "데이터를 가져오는데 실패했습니다."}


@app.get('/chinaquarterDF')
async def chinaquarter():

    data = mycol2.find(
        {"구분": {"$regex": "2018년|2019년|2020년|2021년|2022년|2023년"}})

    filtered_data = []
    for item in data:
        filtered_item = {}
        for key, value in item.items():
            if key == "구분":
                filtered_item[key] = value
            elif "당월" in key and "누계" not in key or "전년동기대비 증가율 (%)" in key:
                filtered_item[key] = value
        filtered_data.append(filtered_item)

    df = pd.DataFrame(filtered_data)

    # 모든 연도를 추출하고 중복을 제거합니다.
    years = set(df['구분'].str.extract('(\d{4})년')[0].astype(int))

    for year in years:
        # 각 연도에 대해 월별 데이터를 분기별로 나눕니다.
        year_str = f"{year}년"
        year_df = df[df['구분'].str.startswith(year_str)]

        quarter1_df = year_df[year_df['구분'].str.contains('\d{4}년 *0?[1-3]월')]
        quarter2_df = year_df[year_df['구분'].str.contains('\d{4}년 *0?[4-6]월')]
        quarter3_df = year_df[year_df['구분'].str.contains('\d{4}년 *0?[7-9]월')]
        quarter4_df = year_df[year_df['구분'].str.contains('\d{4}년 *1[0-2]월')]

        quarters_data = {
            "Q1": json.loads(quarter1_df.to_json(orient='records')),
            "Q2": json.loads(quarter2_df.to_json(orient='records')),
            "Q3": json.loads(quarter3_df.to_json(orient='records')),
            "Q4": json.loads(quarter4_df.to_json(orient='records')),
        }

        # 연도별로 각 분기별 데이터를 저장합니다.
        save_quarters_data(year, quarters_data)

    return "분기별 데이터가 연도별로 저장되었습니다."
