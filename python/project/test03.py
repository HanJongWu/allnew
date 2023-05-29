from fastapi import FastAPI  # FastAPI와 MongoDB를 사용하여 API를 구현
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json

# ENCODERS_BY_TYPE: pydantic의 JSON 인코더가 MongoDB [ObjectId]를 문자열(str)로 인코딩할 수 있도록 설정
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()  # FastAPI 애플리케이션을 생성

HOSTNAME = '192.168.1.189:27017'

# 호스트 이름, 사용자 이름, 비밀번호를 사용하여 mongo_client.MongoClient를 초기화 -> 해당 클라이언트를 사용하여 MongoDB에 연결
client = mongo_client.MongoClient(f'mongodb://{HOSTNAME}')
# 연결에 성공하면 "Connected to Mongodb...." 메시지를 출력
print('Connected to Mongodb....')

# 이전에 초기화한 client 객체를 사용=>MongoDB의 'test' 데이터베이스에 접속하고, 'testdb' 컬렉션을 선택
mydb = client['test']
mycol1 = mydb['AllParticleDatas']
mycol2 = mydb['FabCapa_All_Trans']


@app.get('/')
async def healthCheck():  # 서버의 연결상태 확인
    return "OK"

# /getmongo: MongoDB의 mycol 컬렉션에서 최대 20개의 문서를 가져오는 엔드포인트


@app.get('/mongo_col1')
async def getMongo():
    return list(mycol1.find())


@app.get('/mongo_col2')
async def getMongo():
    return list(mycol2.find())


@app.get('/getmongo')
async def getMongo():
    return list(mycol1.find().limit(20))

# /getissueDate: 지정된 issueDate에 해당하는 사용자를 MongoDB의 mycol 컬렉션에서 검색하는 엔드포인트


@app.get('/getissueDate')
async def getissueDate(issueDate: str = None):
    if issueDate is None:
        return "조회하려는 미세먼지 경보 발령 날짜를 입력하세요.(ex. YYYY-MM-DD)"  # 달별로
    else:
        result = list(mycol1.find({"issueDate": str(issueDate)}))
        if result:  # issueDate가 존재하는지 여부
            return result  # 요청으로 받은 발령날짜에 해당하는 미세먼지 농도를 mycol 컬렉션에서 검색하여 결과를 반환
        else:
            return "검색 결과가 없습니다."


@app.get('/getdistrictName')
async def getdistrictName(districtName: str = None):
    if districtName is None:
        return "조회하려는 경보 발령 지역 명을 입력하세요.(ex. 충북, 전북)"
    else:
        result = list(mycol1.find({"districtName": str(districtName)}))
        if result:  # issueDate가 존재하는지 여부
            return result  # 요청으로 받은 발령날짜에 해당하는 미세먼지 농도를 mycol 컬렉션에서 검색하여 결과를 반환
        else:
            return "검색 결과가 없습니다."
