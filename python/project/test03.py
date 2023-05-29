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


@app.get('/')
async def healthCheck():
    return "OK"

# /getmongo: MongoDB의 mycol 컬렉션에서 최대 20개의 문서를 가져오는 엔드포인트


# @app.get('/mongo_col1')
# async def getMongo():
#     return list(mycol1.find())


@app.get('/mongo_col2')
async def getMongo():
    return list(mycol2.find())


@app.get('/getmongo')
async def getMongo():
    return list(mycol2.find().limit(20))

# Json Server에서 데이터 가지고 오기


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

    quarter1_df = df[df['구분'].str.contains('\d{4}년 *0?[1-3]월')]
    quarter2_df = df[df['구분'].str.contains('\d{4}년 *0?[4-6]월')]
    quarter3_df = df[df['구분'].str.contains('\d{4}년 *0?[7-9]월')]
    quarter4_df = df[df['구분'].str.contains('\d{4}년 *1[0-2]월')]

    quarter1_json = quarter1_df.to_json(orient='records')
    quarter2_json = quarter2_df.to_json(orient='records')
    quarter3_json = quarter3_df.to_json(orient='records')
    quarter4_json = quarter4_df.to_json(orient='records')

    return {"Q1": json.loads(quarter1_json),
            "Q2": json.loads(quarter2_json),
            "Q3": json.loads(quarter3_json),
            "Q4": json.loads(quarter4_json)}
