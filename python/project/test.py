from fastapi import FastAPI
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json
import csv

# ObjectId 유형의 객체를 JSON으로 직렬화(serialization)할 때 사용되는 인코더(encoder)를 설정하는 코드입니다.


# ENCODERS_BY_TYPE: pydantic의 JSON 인코더가 MongoDB [ObjectId]를 문자열(str)로 인코딩할 수 있도록 설정
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()  # FastAPI 애플리케이션을 생성

HOSTNAME = '192.168.1.189:27017'

# 호스트 이름, 사용자 이름, 비밀번호를 사용하여 mongo_client.MongoClient를 초기화 -> 해당 클라이언트를 사용하여 MongoDB에 연결
client = mongo_client.MongoClient(f'mongodb://{HOSTNAME}')
# 연결에 성공하면 "Connected to Mongodb...." 메시지를 출력
print('Connected to Mongodb....')


mydb = client['test']
mycol1 = mydb['AllParticleDatas']
mycol2 = mydb['FabCapa_All_Trans']

# pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret_file = os.path.join(BASE_DIR, '../secret.json')

# with open(secret_file) as f:
#     secrets = json.loads(f.read())


# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         errorMsg = "Set the {} environment variable.".format(setting)
#         return errorMsg


# HOSTNAME = get_secret("ATLAS_Hostname")
# USERNAME = get_secret("ATLAS_Username")
# PASSWORD = get_secret("ATLAS_Password")

# client = mongo_client.MongoClient(
#     f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
# print('Connected to Mongodb....')

# mydb = client['project']
# mycol = mydb['data']


@app.get('/')
async def healthCheck():
    return "OK"

# /getmongo: MongoDB의 mycol 컬렉션에서 최대 20개의 문서를 가져오는 엔드포인트


@app.get('/mongo_col1')
async def getMongo():
    return list(mycol1.find())


@app.get('/mongo_col2')
async def getMongo():
    return list(mycol2.find())


@app.get('/getissueDate')
async def getissueDate(issueDate: str = None):
    if issueDate is None:
        return "조회하려는 미세먼지 경보 발령 날짜를 입력하세요.(ex. YYYY-MM-DD)"
    else:
        result = list(mycol1.find({"issueDate": str(issueDate)}))

        if result:
            return result
        else:
            return "검색 결과가 없습니다."


@app.get('/getdistrictName')
async def getdistrictName(districtName: str = None):
    if districtName is None:
        return "조회하려는 경보 발령 지역 명을 입력하세요.(ex. 충북, 전북)"
    else:
        result = list(mycol1.find({"districtName": str(districtName)}))
        if result:
            return result
        else:
            return "검색 결과가 없습니다."
