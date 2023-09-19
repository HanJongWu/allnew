import pandas as pd
from fastapi import FastAPI, Path, Query
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import requests
import shutil
from typing import Optional
import matplotlib.pyplot as plt
from typing import List

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

plt.rcParams['font.family'] = 'AppleGothic'

app = FastAPI() 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:  # secret_file을 열고 파일 객체 f를 생성
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):  # 비밀 정보를 가져오기 위한 함수
    try:
        return secrets[setting]
    except KeyError:  # secrets에 존재하지 않는 경우
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg  # 환경 변수를 설정하라는 오류 메시지를 반환


HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(
    f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb ATLAS....')  # 연결에 성공


mydb = client['project']
mycol1 = mydb['AllParticleDatas']
mycol2 = mydb['chinaData']



@app.get('/mongo')
async def healthCheck():
    return "정상적으로 접속 했습니다."


@app.get('/getjsonserver')
async def getjsonserver():
    url = "http://localhost:5000/data"

    response = requests.get(url)

        data = response.json()

        return data
    else:
        return {"error": "데이터를 가져오는데 실패했습니다."}


@app.get('/getjsonservermongodb')
async def getjsonservermongodb():
    url = "http://localhost:5000/data"

    response = requests.get(url)
    if response.status_code === 200:
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
    os.makedirs(os.path.join(str(year), "quarters"), exist_ok=True)
    for quarter, data in quarters_data.items():
        with open(os.path.join(str(year), "quarters", f"{year}_{quarter}_data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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


# china data year&quater json save
@app.get('/chinaYearAndQuarterDF')
async def chinaYearAndQuarter():

    # 몽고DB에서 2018년부터 2023년까지 데이터를 조회
    data = mycol2.find(
        {"구분": {"$regex": "2018년|2019년|2020년|2021년|2022년|2023년"}})

    # 데이터 필터링 작업을 수행할 빈 리스트 생성
    filtered_data = []

    # 데이터를 순회하면서 필터링 작업 수행
    for item in data:
        filtered_item = {}
        for key, value in item.items():
            if key == "구분":
                filtered_item[key] = value
            # '당월' 포함하며 '누계'를 포함하지 않는 데이터 또는 '전년동기대비 증가율 (%)' 데이터 필터링
            elif "당월" in key and "누계" not in key:
                filtered_item[key] = value
        filtered_data.append(filtered_item)

    # 필터링된 데이터를 Pandas DataFrame으로 변환
    df = pd.DataFrame(filtered_data)

    # 구분 컬럼에서 년도를 추출하여 중복 없이 저장
    years = set(df['구분'].str.extract('(\d{4})년')[0].astype(int))

    # 각 년도별로 데이터를 처리
    for year in years:

        year_str = f"{year}년"

        # 해당 년도의 데이터만 추출
        year_df = df[df['구분'].str.startswith(year_str)]

        # 해당 년도의 데이터를 JSON 형식으로 변환
        year_data = json.loads(year_df.to_json(orient='records'))

        # 년도별 데이터를 저장하는 함수 호출
        save_yearly_data(year, year_data)

        # 분기별 데이터 처리 및 저장
        quarter1_df = year_df[year_df['구분'].str.contains('\d{4}년 *0?[1-3]월')]
        quarters_data = {
            "Q1": json.loads(quarter1_df.to_json(orient='records'))
        }

        # 2023년 이외의 년도의 경우, 분기별 데이터 처리
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

        # 분기별 데이터를 저장하는 함수 호출
        save_quarters_data_to_df(year, quarters_data)

    # 연도별 및 분기별로 처리된 데이터가 저장되었다는 정상 실행 결과 메시지 반환
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
async def save_visual(item_list: str = Query(..., min_length=1, max_length=40)):
    items = item_list.split(',')

    if len(items) < 1 or len(items) > 3:
        return {"error": "Invalid number of items. Please enter between 1 to 3 items separated by commas."}

    time_range = pd.date_range(start='2018-01', end='2023-03', freq='QS')
    quarterly_mean_df = pd.DataFrame(columns=items, index=time_range)

    valid_years = range(2018, 2024)
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    for year in valid_years:
        for quarter in quarters:
            mean_values = quarter_mean(year, quarter, items)
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
