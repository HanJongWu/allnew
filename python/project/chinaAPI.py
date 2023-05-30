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
    return "정상적으로 접속 했습니다."


@app.get('/getjsonserver')
async def getdata():
    url = "http://localhost:5000/data"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data
    else:
        return {"error": "데이터를 가져오는데 실패했습니다."}


@app.get('/getmongoselect20')
async def getMongoSelect():
    return list(mycol2.find().limit(20))


@app.get('/mongodbALL')
async def getAllMongo():
    return list(mycol2.find())


def save_yearly_data(year, data):
    os.makedirs(str(year), exist_ok=True)
    with open(os.path.join(str(year), f"{year}_year_data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_quarters_data(year, quarters_data):
    os.makedirs(os.path.join(str(year), "quarters"), exist_ok=True)
    for quarter, data in quarters_data.items():
        with open(os.path.join(str(year), "quarters", f"{year}_{quarter}_data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


@app.get('/chinaYearAndQuarterDF')
async def chinaYearAndQuarter():

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

    years = set(df['구분'].str.extract('(\d{4})년')[0].astype(int))

    for year in years:

        year_str = f"{year}년"
        year_df = df[df['구분'].str.startswith(year_str)]

        year_data = json.loads(year_df.to_json(orient='records'))

        save_yearly_data(year, year_data)

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

        save_quarters_data(year, quarters_data)

    return "연도별 및 분기별 데이터가 성공적으로 저장되었습니다."


@app.get("/china_data/{year}/{quarter}")
def china_data(year: int, quarter: int):
    query = {"year": year, "quarter": quarter}
    data = list(mycol2.find(query))
    return {"results": data}


# @app.get('/chinaQuarterDF')
# async def chinaQuarterDF(year: int, quarter: int):
#     json_file = f"{year}_Q{quarter}_data.json"
#     json_path = os.path.join('.', str(year), json_file)

#     if not os.path.exists(json_path):
#         return 'Error: No such file.'

#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.loads(f.read())

#     df = pd.DataFrame.from_records(data, index='구분')

#     return df.to_json(orient='records', force_ascii=False)
# # @app.get('/chinaDF')


# async def chinaQuarterDF():
#     path = './'

#     # 2018년 ~ 2023년 디렉토리 내의 모든 json 파일 경로 목록을 가져옵니다.
#     json_paths = []
#     for year in range(2018, 2024):
#         for quarter in range(1, 5):
#             json_path = os.path.join(path, str(year), f"{year}_Q{quarter}_data.json")
#             json_paths.append(json_path)
# async def chinaDF(year: int, quarter: int):
#     json_file = f"{year}_Q{quarter}_data.json"

#     with open(json_file, 'r', encoding='utf-8') as f:
#         data = json.loads(f.read())

#     df = pd.DataFrame.from_records(data, index='구분')

#     return df.to_json(orient='records', force_ascii=False)
