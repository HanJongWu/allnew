import pandas as pd
from fastapi import FastAPI, Path
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import requests
import shutil

# ENCODERS_BY_TYPE: pydantic의 JSON 인코더가 MongoDB [ObjectId]를 문자열(str)로 인코딩할 수 있도록 설정
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()  # FastAPI 애플리케이션을 생성

HOSTNAME = '192.168.1.25:27017'

client = mongo_client.MongoClient(f'mongodb://{HOSTNAME}')

print('Connected to Mongodb....')

mydb = client['project']
mycol1 = mydb['AllParticleDatas']
mycol2 = mydb['chinaData']

# 접속 확인


@app.get('/')
async def healthCheck():
    return "정상적으로 접속 했습니다."


# jsonserver data request
@app.get('/getjsonserver')
async def getjsonserver():
    url = "http://localhost:5000/data"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data
    else:
        return {"error": "데이터를 가져오는데 실패했습니다."}


# jsonserver data request > mongodb
@app.get('/getjsonservermongodb')
async def getjsonservermongodb():
    url = "http://localhost:5000/data"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        if isinstance(data, dict):
            data = [data]

        mycol2.insert_many(data)
        return {"status": "mongoDB insert.."}

    else:
        return {"error"}


# mongodb select 20
@app.get('/getmongoselect20')
async def getMongoSelect():
    return list(mycol2.find().limit(20))


# mongdb data all
@app.get('/mongodbALL')
async def getAllMongo():
    return list(mycol2.find())


# year data function
def save_yearly_data(year, data):
    os.makedirs(str(year), exist_ok=True)
    with open(os.path.join(str(year), f"{year}_year_data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# quater data function
def save_quarters_data(year, quarters_data):
    os.makedirs(os.path.join(str(year), "quarters"), exist_ok=True)
    for quarter, data in quarters_data.items():
        with open(os.path.join(str(year), "quarters", f"{year}_{quarter}_data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


# china data year&quater json save
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


# china data year&quater request


@app.get("/{year}/{quarter}")
async def get_data(
    year: int = Path(..., description="연도를 입력하세요. ex) 2018~2023"),
    quarter: int = Path(..., description="분기를 입력하세요. ex) 1~4")
):
    if year < 2018 or year > 2023 or quarter < 1 or quarter > 4:
        return {"error": "Invalid year or quarter"}

    json_file = f"{year}/quarters/{year}_Q{quarter}_data.json"
    if not os.path.exists(json_file):
        return {"error": "File not found"}

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    df = pd.DataFrame.from_records(data)

    result_json_file = f'{year}_Q{quarter}.json'
    with open(result_json_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

    return {"message": f"{year}년 {quarter}분기 데이터를 불러옵니다", "data": df.to_dict(orient="records")}


# mongoDB drop

@app.get('/dropMongoCollectionData')
async def dropMongoCollectionData(collectionName: str = None):
    drop_mycol = mydb[collectionName]
    drop_mycol.drop()
    return 'mongoDB 데이터 삭제 완료'


# local data drop

@app.get('/droplocalData')
async def droplocalData():
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    quarters = ["Q1", "Q2", "Q3", "Q4"]

    for year in years:
        if os.path.exists(str(year)):
            shutil.rmtree(str(year))

    for quarter in quarters:
        files_to_remove = [file for file in os.listdir(
        ) if file.endswith(".json") and quarter in file]
        for file in files_to_remove:
            os.remove(file)

    if os.path.exists('chinaData.json'):
        os.remove('chinaData.json')

    return "local Data 삭제 완료"
