import pandas as pd
from fastapi import FastAPI, Path
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import requests
import shutil
from typing import Optional
import matplotlib.pyplot as plt

# ENCODERS_BY_TYPE: pydantic의 JSON 인코더가 MongoDB [ObjectId]를 문자열(str)로 인코딩할 수 있도록 설정
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

plt.rcParams['font.family'] = 'AppleGothic'

app = FastAPI()  # FastAPI 애플리케이션을 생성

# MongoDB Atlas 접속시 비밀정보를 로드하고 가져오기 위한 함수 정의
# 재 스크립트의 상위 디렉토리 경로를 BASE_DIR 변수에 할당
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# BASE_DIR과 상대 경로를 조합하여 비밀 정보가 저장된 파일의 경로를 secret_file 변수에 할당
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:  # secret_file을 열고 파일 객체 f를 생성
    # 파일의 내용을 읽어와 JSON 형식으로 디코딩하여 secrets 변수에 할당
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):  # 비밀 정보를 가져오기 위한 함수
    try:
        # setting 매개변수로 설정 이름을 받음 -> secrets 딕셔너리에서 해당 설정 이름에 해당하는 값을 찾아 반환
        return secrets[setting]
    except KeyError:  # secrets에 존재하지 않는 경우
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg  # 환경 변수를 설정하라는 오류 메시지를 반환


# 정의한 get_secret()함수 사용 => Mongodb 호스트이름, 사용자이름, 비밀번호를 가져와 MongoDB에 연결
HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(
    f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb ATLAS....')  # 연결에 성공

# HOSTNAME = '192.168.1.25:27017'

# client = mongo_client.MongoClient(f'mongodb://{HOSTNAME}')

# print('Connected to Mongodb....')

mydb = client['project']
mycol1 = mydb['AllParticleDatas']
mycol2 = mydb['chinaData']

# 접속 확인


@app.get('/mongo')
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
def save_quarters_data_to_df(year, quarters_data):
    for quarter, data in quarters_data.items():
        if data:
            # JSON 데이터를 DataFrame으로 변환
            quarter_df = pd.DataFrame(data)

            # 출력할 폴더 생성 (폴더가 없는 경우)
            output_dir = f'output/{year}'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # DataFrame을 CSV 파일로 저장
            quarter_df.to_csv(
                f"{output_dir}/{year}_{quarter}.csv", index=False)
# def save_quarters_data(year, quarters_data):
#     os.makedirs(os.path.join(str(year), "quarters"), exist_ok=True)
#     for quarter, data in quarters_data.items():
#         with open(os.path.join(str(year), "quarters", f"{year}_{quarter}_data.json"), "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)


# china data year&quater json save
# FastAPI에서 '/chinaYearAndQuarterDF' 엔드포인트로 비동기 함수 정의
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

        quarters_data = {
            "Q1": json.loads(quarter1_df.to_json(orient='records'))
        }

        if year != 2023:
            quarter2_df = year_df[year_df['구분'].str.contains(
                '\d{4}년 *0?[4-6]월')]
            quarter3_df = year_df[year_df['구분'].str.contains(
                '\d{4}년 *0?[7-9]월')]
            quarter4_df = year_df[year_df['구분'].str.contains(
                '\d{4}년 *1[0-2]월')]
            quarters_data["Q2"] = json.loads(
                quarter2_df.to_json(orient='records'))
            quarters_data["Q3"] = json.loads(
                quarter3_df.to_json(orient='records'))
            quarters_data["Q4"] = json.loads(
                quarter4_df.to_json(orient='records'))

        save_quarters_data_to_df(year, quarters_data)

    return "연도별 및 분기별 데이터가 성공적으로 저장되었습니다."


# china data year&quater request


@app.get("/{year}/{quarter}")
async def get_data(
    year: int = Path(..., description="연도를 입력하세요. ex) 2018~2023"),
    quarter: int = Path(..., description="분기를 입력하세요. ex) 1~4")
):
    if year < 2018 or year > 2023 or quarter < 1 or quarter > 4:
        return {"error": "유효한 날짜를 입력하세요"}

    json_file = f"{year}/quarters/{year}_Q{quarter}_data.json"
    if not os.path.exists(json_file):
        return {"error": "유효한 날짜를 입력하세요"}

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

    # PNG 파일 삭제 부분 추가
    png_files_to_remove = [
        file for file in os.listdir() if file.endswith(".png")]
    for file in png_files_to_remove:
        os.remove(file)

    return "local Data 삭제 완료"


def quarter_mean(year, quarter, item_list):
    file_path = f"./{year}/quarters/{year}_{quarter}_data.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            quarter_data = json.load(file)
    except FileNotFoundError:
        return None

    df = pd.DataFrame(quarter_data)

    mean_values = {}

    for item in item_list:
        mean_values[item] = df[item].mean()

    return mean_values


@app.get('/save_visual')
async def save_visual(item_list: str):
    items = item_list.split(',')
    time_range = pd.date_range(start='2018-01', end='2023-03', freq='QS')
    quarterly_mean_df = pd.DataFrame(columns=items, index=time_range)

    valid_years = range(2018, 2024)
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    for year in valid_years:
        for quarter in quarters:
            mean_values = quarter_mean(
                year, quarter, items)  # items를 파라미터로 전달합니다
            if mean_values is None:
                continue
            last_month = int(quarter[-1]) * 3
            quarterly_mean_df.loc[pd.Timestamp(
                f"{year}-{last_month}")] = [mean_values[item] for item in items]

    plt.figure(figsize=(16, 8))
    plt.plot(quarterly_mean_df)
    plt.title('2018 - 2023 Average Graph')
    plt.xlabel('Time')
    plt.ylabel('Mean Value')
    plt.legend(items)

    file_name = f'{item_list}.png'
    plt.savefig(file_name, dpi=300)
    plt.close()

    return {f'{file_name} saved...'}
