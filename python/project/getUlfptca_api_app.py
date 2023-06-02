from fastapi import FastAPI  # FastAPI와 MongoDB를 사용하여 API를 구현
from pymongo import mongo_client
from pymongo import InsertOne
import pydantic
import requests
from bson.objectid import ObjectId
import os.path
import os
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Union
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# ENCODERS_BY_TYPE: pydantic의 JSON 인코더가 MongoDB [ObjectId]를 문자열(str)로 인코딩할 수 있도록 설정
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()  # FastAPI 애플리케이션을 생성

# MongoDB Atlas 접속시 비밀정보를 로드하고 가져오기 위한 함수 정의
# 재 스크립트의 상위 디렉토리 경로를 BASE_DIR 변수에 할당
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# BASE_DIR과 상대 경로를 조합하여 비밀 정보가 저장된 파일의 경로를 secret_file 변수에 할당
secret_file = os.path.join(BASE_DIR, 'secret1.json')

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
# HOSTNAME = get_secret("ATLAS_Hostname")
# USERNAME = get_secret("ATLAS_Username")
# PASSWORD = get_secret("ATLAS_Password")
# 호스트 이름, 사용자 이름, 비밀번호를 사용하여 mongo_client.MongoClient를 초기화 -> 해당 클라이언트를 사용하여 MongoDB에 연결
# client = mongo_client.MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
# print('Connected to Mongodb ATLAS....') #연결에 성공


# MongoDB Ubuntu 접속
HOSTNAME = '192.168.1.189:27017'
# 해당 클라이언트를 사용하여 MongoDB에 연결
client = mongo_client.MongoClient(f'mongodb://{HOSTNAME}')
# 연결에 성공하면 "Connected to Mongodb...." 메시지를 출력
print('Connected to Mongodb Ubuntu....')

# 이전에 초기화한 client 객체를 사용=>MongoDB의 'test' 데이터베이스에 접속하고, 'testdb' 컬렉션을 선택
mydb = client['test']  # 'test' 데이터베이스에 접속
mycol = mydb['AllUlfptcaAlarms']  # 컬렉션을 선택

# 애플리케이션 상태 확인


@app.get('/')
async def healthCheck():
    return "OK_readytoRequest"

# mongocollectionlist: 2018~2023ParticleDatas, AllParticleDatas
# FabData Collection: FabCapa_All_Trans, FabCapa_Trans


@app.get('/getMongoColData_30')
async def getMongoColData_30(collectionName: str = None):
    get_mycol = mydb[collectionName]  # 컬렉션을 선택
    return list(get_mycol.find().limit(30))


@app.get('/getMongoColData_ALL')
async def getMongoColData_ALL(collectionName: str = None):
    get_mycol = mydb[collectionName]  # 컬렉션을 선택
    return list(get_mycol.find())


@app.get('/dropMongoCol')
async def dropMongoCol(collectionName: str = None):
    drop_mycol = mydb[collectionName]  # drop 컬렉션 선택
    drop_mycol.drop()
    return 'Drop selected collection...'

# url에 http get요청을 보내고, 응답을 딕셔너리객체로 변환하는 함수


def getRequestData(url):
    try:
        response = requests.get(url)  # URL에 HTTP GET 요청을 보냄
        response.raise_for_status()  # 2xx 이외의 상태 코드가 반환되면 예외 발생
        contents = response.text  # 응답에서 JSON 형식의 문자열 추출
        data_dict = json.loads(contents)  # JSON 문자열을 딕셔너리 객체로 변환
        return data_dict
    except requests.exceptions.RequestException as e:
        print(f"{url}에서 데이터를 요청하는 중 오류가 발생했습니다: {str(e)}")
        return None

# 공공데이터포털에서 '한국환경공단_에어코리아_미세먼지 경보 발령 현황'데이터를 가져와 JSON 형식으로 저장


@app.get('/getUlfptcaAlarmInfo_year')  # 연도별 데이터 끌어오게 하는 방법
def getUlfptcaAlarmInfo_year(year: int = None):
    if year is None:  # year 변수가 None인 경우 현재 년도를 할당하도록 함
        now = datetime.now()
        current_year = now.year
        year = current_year
        # return year
    if year < 2018 or year > 2023:
        return '입력한 연도 관련 데이터가 존재하지 않습니다.'

    end_point = 'https://apis.data.go.kr/B552584/UlfptcaAlarmInqireSvc/getUlfptcaAlarmInfo'
    # API 호출에 필요한 파라미터들을 저장하기 위함
    parameters = ''
    parameters += '?serviceKey=' + get_secret("data_apiKey")
    parameters += '&returnType=json'
    parameters += '&numOfRows=500'
    parameters += '&pageNo=1'
    parameters += '&year=' + str(year)  # 측정연도

    url = end_point + parameters

    # getRequestUrl(url) 함수를 사용 => 생성한 URL로 API 요청을 보내고, 응답을 받음
    response = getRequestData(url)
    if (response == None):  # 응답이 None인 경우, None을 반환
        return {'error': 'API 요청에 실패하였습니다.'}
    else:  # 응답이 None이 아닌 경우
        print(f"{year}년도 데이터")
        return response  # 응답을 JSON 형식으로 변환하여 반환


# all을 입력할 경우, 모든연도에 해당하는 데이터를 끌어오는 코드를 알려줘
@app.get('/getUlfptcaAlarmInfo_ALL')
def getUlfptcaAlarmInfo_ALL(year: Union[int, str] = None):
    if isinstance(year, int):
        return getUlfptcaAlarmInfo_year(year)

    if isinstance(year, str) and year.lower() == 'all':
        response = []
        for y in range(2018, 2024):  # 2018~2024
            result = getUlfptcaAlarmInfo_year(y)
            if (result['response']['header']['resultCode'] == '00'):
                totalCount = result['response']['body']['totalCount']
                print('데이터 총 개수 : ', totalCount)
                for item in result['response']['body']['items']:
                    response.append(item)  # 추가되는 연도별 데이터를 response에 추가
                if totalCount == 0:
                    break
            else:
                break
        return response


def makeJSON(year: str = None):
    if year == 'all':
        result = getUlfptcaAlarmInfo_ALL('all')
    else:
        try:
            year = int(year)
            result = getUlfptcaAlarmInfo_year(year)
        except ValueError:
            return {'error': 'Invalid year format'}

    if result is not None:
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        return {'message': 'JSON file created successfully'}
    else:
        return {'message': 'Failed to fetch data'}

# mongodb에 Import


@app.get('/mongoImport_JSON')
async def mongoImport_JSON():
    for year in range(2018, 2024):
        collection = db['{}ParticleDataTests'.format(year)]  # 컬렉션 이름 지정
        makeJSON(year)
    bulk_operations = []
    # 대용량 데이터를 작은 배치로 분할하여 Bulk Write 작업 생성
    for data in json_data:
        bulk_operations.append(InsertOne(data))
        if len(bulk_operations) >= 1000:  # 작은 배치 크기 설정
            collection.bulk_write(bulk_operations, ordered=False)
            bulk_operations = []
    # 남은 데이터에 대해 Bulk Write 작업 실행
    if bulk_operations:
        collection.bulk_write(bulk_operations, ordered=False)
    print(data.json, 'MongoDB imported~!!')
    return {'message': 'Import successful'}

# mongodb에 Export


@app.get('/mongoExport_csv')
async def mongoExport_csv(collectionName: str = None):
    Exportcollection = mydb[collectionName]
    csv_File = 'ExportedCSVFile.csv'
    data = Exportcollection.find()

    with open(csv_File, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        field_names = list(data[0].keys())  # 헤더 작성
        writer.writerow(field_names)

        for document in data:  # 데이터 작성
            writer.writerow(list(document.values()))
    print("CSV 파일로 내보내기가 완료되었습니다.")
    return {'message': 'CSV file exported successfully.'}


def CreateDataFrame(json: str = None):
    selected_df = pd.DataFrame(json, columns=[
                               'districtName', 'issueDate', 'issueGbn', 'issueVal', 'itemCode', 'moveName', 'sn'])
    selected_df = selected_df.set_index('sn')
    selected_df['issueVal'] = selected_df['issueVal'].astype(int)
    selected_df['issueDate'] = pd.to_datetime(selected_df['issueDate'])
    selected_df.fillna(0, inplace=True)
    return selected_df  # 수정된 데이터프레임이 반환됨


def SaveDF_to_CSV(data_frame):
    filename = f'{data_frame}.csv'     # 파일 이름 지정
    try:  # csv 파일로 저장
        # 한글이 포함될 수 있어서 utf-8-sig
        data_frame.to_csv(filename, index=True, encoding='utf-8-sig')
        print(f'{data_frame}이 {filename}파일로 저장되었습니다.')
    except Exception as e:
        print(f'{e}: 파일 저장을 실패했습니다.')

# 연도별(2018, 2019, 2020, 2021, 2022, 2023) 데이터로


@app.get('/getUlfptca_DataFrame_Annual')  # 지역의 연도별 미세먼지농도 추세 df
# 해당 지역의 PM2.5, PM10 미세먼지 농도를 연도별로 추세 분석
def getUlfptca_DataFrame_Annual(city: str = None):
    plt.rcParams['font.family'] = 'Malgun Gothic'
    makeJSON('all')  # data.json파일을 생성
    json_file = 'data.json'  # 파일 이름 저장

    with open(json_file, 'r', encoding='utf-8') as file:
        dataUlfptcaAlarms = json.load(file)

    selected_df = CreateDataFrame(dataUlfptcaAlarms)  # selected_df을 생성

    listData = selected_df['itemCode'].unique()
    result_data = []  # 데이터 초기화

    if city == 'all':
        result_data = []
        for city_name in selected_df['districtName'].unique():
            # df_city = pd.DataFrame(columns=['발령 지역 명', '미세먼지 항목 구분', '발령 연도', '평균 미세먼지 농도'])
            for PMdata in listData:
                print(f'연도별 {PMdata} 농도 추세')
                df_PMdata = selected_df.loc[(selected_df['districtName'] == city_name) & (
                    selected_df['itemCode'] == PMdata), ['itemCode', 'issueDate', 'issueVal']]
                df_YearPMdata_list = []
                for year in range(2018, 2024):
                    print(f'{year}년도 데이터')
                    df_YearPMdata = df_PMdata[df_PMdata['issueDate'].dt.year == year]
                    avg_issueVal_year = np.round(
                        df_YearPMdata['issueVal'].mean(skipna=True))
                    print(avg_issueVal_year)
                    print('-' * 40)
                    df_YearPMdata_list.append(
                        [city_name, PMdata, year, avg_issueVal_year])
                if df_YearPMdata_list:
                    df_YearPMdata_all = pd.DataFrame(df_YearPMdata_list, columns=[
                                                     '발령 지역 명', '미세먼지 항목 구분', '발령 연도', '평균 미세먼지 농도'])
                    result_data.append(df_YearPMdata_all)
                # result_data_unique = [x for x in result_data if result_data.count(x) == 1]
        Df_Result = pd.concat(result_data, ignore_index=True, axis=0)
        # SaveDF_to_CSV(Df_Result) #생성한 도시별 데이터프레임을 csv파일로 저장
        print(Df_Result)
    else:
        result_data = []  # 데이터 초기화
        for PMdata in listData:
            print(f'{city}의 {PMdata} 농도 추세')
            df_PMdata = selected_df.loc[(selected_df['districtName'] == city) & (
                selected_df['itemCode'] == PMdata), ['itemCode', 'issueDate', 'issueVal']]
            for year in range(2018, 2024):
                print(f'{year}년도 데이터')
                df_YearPMdata = df_PMdata[df_PMdata['issueDate'].dt.year == year]
                avg_issueVal_year = np.round(
                    df_YearPMdata['issueVal'].mean(skipna=True))
                print(avg_issueVal_year)
                print('-' * 40)
                result_data.append([city, PMdata, year, avg_issueVal_year])
        Df_Result = pd.DataFrame(result_data, columns=[
                                 '발령 지역 명', '미세먼지 항목 구분', '발령 연도', '평균 미세먼지 농도'])
        print(Df_Result)
    return Df_Result


@app.get('/ShowUlfptca_DataFrame_Annual')  # 지역의 연도별 미세먼지농도 추세 df
# 해당 지역의 PM2.5, PM10 미세먼지 농도를 연도별로 추세 분석
def ShowUlfptca_DataFrame_Annual(city: str = None):
    # 만일 city에all이 입력되어도 전체도시관련 피벗테이블이 출력됨
    Df_Result = getUlfptca_DataFrame_Annual(city)
    # pivot_table 생성
    pivot_Df_Result = Df_Result.pivot_table(
        index=['발령 지역 명', '발령 연도'], columns='미세먼지 항목 구분', values='평균 미세먼지 농도', fill_value=0)
    pivot_Df_Result.reset_index(inplace=True)  # index를 컬럼으로 변환
    pivot_Df_Result.columns.name = None    # 피벗테이블의 컬럼이름 삭제
    print(pivot_Df_Result)
    return pivot_Df_Result


def merge_images(image_path_list):
    images = [Image.open(image_path) for image_path in image_path_list]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    return new_image


@app.get('/getUlfptca_Plot_Annual')  # 지역별 전체연도 미세먼지농도 추세 그래프
def getUlfptca_Plot_Annual(city: str = None):  # 도시별
    # plt.rcParams['font.family'] = 'Malgun Gothic'
    # for city in cities:
    Df_Result = getUlfptca_DataFrame_Annual(city)
    df_PM25 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM25']
    df_PM10 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM10']
    # kind='line'
    plt.figure(figsize=(10, 6))
    plt.plot(df_PM25['발령 연도'], df_PM25['평균 미세먼지 농도'],
             color='r', label='PM25', marker='o')
    plt.plot(df_PM10['발령 연도'], df_PM10['평균 미세먼지 농도'],
             color='b', label='PM10', marker='s')
    plt.xlabel('발령 연도(time: year)')
    plt.ylabel('평균 미세먼지 농도')
    plt.title(f'{city}의 연도별 미세먼지 농도 추세')
    plt.legend()
    plt.savefig(f'./Files/YearImage/{city}연도별_미세먼지 추세.png')
    print(f'{city}_연도별_미세먼지 추세.png file saved~!!')
    plt.show()
    # plt.clf()


@app.get('/getUlfptca_Plot_AllCities')
def getUlfptca_Plot_AllCities(year: int = None):  # 연도별 도시들의 미세먼지 농도 추세
    Df_Result = getUlfptca_DataFrame_Annual('all')  # 전체 발령 데이터를 가져옴

    if year is not None:
        Df_Result = Df_Result[Df_Result['발령 연도']
                              == year]  # 입력된 연도와 일치하는 발령 데이터만 필터링
        df_PM25 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM25']
        df_PM10 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM10']

        # 초미세먼지 plot
        plt.figure(figsize=(10, 6))
        plt.plot(df_PM25['발령 지역 명'], df_PM25['평균 미세먼지 농도'],
                 color='r', label='PM25', marker='o')
        plt.xlabel('발령 지역 명(city)')
        plt.ylabel('평균 미세먼지 농도')
        plt.title(f'도시들의 {year}년도 초미세먼지(PM2.5) 농도 추세')
        plt.legend()
        plt.savefig(f'도시들의 {year}년도 초미세먼지(PM2.5) 농도 추세.png')
        print(f'도시들의 {year}년도 초미세먼지(PM2.5) 농도 추세.png file saved~!!')
        plt.show()

        # 미세먼지 plot
        plt.figure(figsize=(10, 6))
        plt.plot(df_PM10['발령 지역 명'], df_PM10['평균 미세먼지 농도'],
                 color='b', label='PM10', marker='s')
        plt.xlabel('발령 지역 명(city)')
        plt.ylabel('평균 미세먼지 농도')
        plt.title(f'도시들의 {year}년도 미세먼지(PM10) 농도 추세')
        plt.legend()
        plt.savefig(f'도시들의 {year}년도 미세먼지(PM10) 농도 추세.png')
        print(f'도시들의 {year}년도 미세먼지(PM10) 농도 추세.png file saved~!!')
        plt.show()

        image_path_list = [
            f'도시들의 {year}년도 미세먼지(PM10) 농도 추세.png', f'도시들의 {year}년도 초미세먼지(PM2.5) 농도 추세.png']
        merged_image = merge_images(image_path_list)
        merged_image.show()
        merged_image.save(f'./Files/YearImage/연도별 도시들의 미세먼지 농도 추세.png', 'PNG')
        print(f'연도별 도시들의 미세먼지 농도 추세.png file saved...')


# {year}-{month}월별 도시의 미세먼지농도
@app.get('/getUlfptca_DataFrame_Monthly')
async def getUlfptca_DataFrame_Monthly(city: str = None):
    plt.rcParams['font.family'] = 'Malgun Gothic'
    makeJSON('all')  # data.json파일을 생성
    json_file = 'data.json'  # 파일 이름 저장

    with open(json_file, 'r', encoding='utf-8') as file:
        dataUlfptcaAlarms = json.load(file)

    selected_df = CreateDataFrame(dataUlfptcaAlarms)  # selected_df을 생성

    # 해당 지역(city)의 데이터프레임 생성
    listData = selected_df['itemCode'].unique()
    # for city in citylist:
    result_data = []  # 데이터 초기화
    for PMdata in listData:
        print(f'{city}의 월별 {PMdata} 농도 추세')
        df_PMdata = selected_df.loc[(selected_df['districtName'] == city) & (
            selected_df['itemCode'] == PMdata), ['itemCode', 'issueDate', 'issueVal']]

        for year in range(2018, 2024):
            # print(f'{year}년도 데이터')
            df_YearPMdata = df_PMdata[df_PMdata['issueDate'].dt.year == year]
            months = df_YearPMdata['issueDate'].dt.month.unique()

            for month in months:
                df_MonthPMdata = df_YearPMdata[df_YearPMdata['issueDate'].dt.month == month]
                avg_issueVal_month = np.round(
                    df_MonthPMdata['issueVal'].mean(skipna=True))
                # print(f'{year}년 {month}월 {PMdata}')
                # print(avg_issueVal_month)
                # print('-' * 40)
                result_data.append(
                    [city, PMdata, f'{year}-{month}월', avg_issueVal_month])
    Df_Result = pd.DataFrame(result_data, columns=[
                             '발령 지역 명', '미세먼지 항목 구분', '발령 연도별 월', '평균 미세먼지 농도'])
    print(Df_Result)
    return Df_Result

    df_PM25 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM25']
    df_PM10 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM10']
    # kind='line'
    plt.plot(df_PM25['발령 연도별 월'], df_PM25['평균 미세먼지 농도'],
             color='#FF00FF', label='PM25', marker='o')
    plt.xlabel('경보발령 연도-월')
    plt.ylabel('평균 미세먼지 농도')
    plt.title(f'{city}의 월별 초미세먼지(PM25) 농도 추세')
    plt.legend()
    plt.savefig(f'./MonthlyImage/{city}_월별_초미세먼지(PM25)농도 추세.png', dpi=400)
    print(f'{city}_월별_초미세먼지(PM25) 추세.png file saved~!!')
    plt.show()

    plt.plot(df_PM10['발령 연도별 월'], df_PM10['평균 미세먼지 농도'],
             color='#00FF00', label='PM10', marker='s')
    plt.xlabel('경보발령 연도-월')
    plt.ylabel('평균 미세먼지 농도')
    plt.title(f'{city}의 월별 미세먼지(PM10) 농도 추세')
    plt.legend()
    plt.savefig(f'./MonthlyImage/{city}_월별_미세먼지(PM10)농도 추세.png', dpi=400)
    print(f'{city}_월별_미세먼지(PM10) 농도 추세.png file saved~!!')
    plt.show()

    plt.clf()


@app.get('/getUlfptca_DataFrame_Quarter')
async def getUlfptca_DataFrame_Quarter(city: str = None):
    plt.rcParams['font.family'] = 'Malgun Gothic'
    makeJSON('all')  # data.json파일을 생성
    json_file = 'data.json'  # 파일 이름 저장

    with open(json_file, 'r', encoding='utf-8') as file:
        dataUlfptcaAlarms = json.load(file)

    selected_df = CreateDataFrame(dataUlfptcaAlarms)  # selected_df을 생성

    city_frames = []
    listData = selected_df['itemCode'].unique()
# for city in citylist:
    result_data = []  # 데이터 초기화
    for PMdata in listData:
        print(f'{city}의 분기별 {PMdata} 농도 추세')
        df_PMdata = selected_df.loc[(selected_df['districtName'] == city) & (
            selected_df['itemCode'] == PMdata), ['itemCode', 'issueDate', 'issueVal']]
        # df_PMdata['issueDate']
        # 분기별 데이터
        for year in range(2018, 2024):
            print(f'{year}년도 데이터')
            df_YearPMdata = df_PMdata[df_PMdata['issueDate'].dt.year == year]
            months = df_YearPMdata['issueDate'].dt.month.unique()

            for month in months:  # month변수의 값에 따라 분기값을 설정
                # quater = []
                # avg_quater = []

                if month in range(1, 4):
                    # quater.append(f'{year}년도 1분기')
                    quater = f'{year}년도 1분기'
                    df_MonthPMdata = df_YearPMdata[df_YearPMdata['issueDate'].dt.month.isin(
                        [1, 2, 3])]  # df_YearPMdata 데이터프레임에서 1,2,3월에 해당하는 데이터를 추출
                    avg_issueVal_quater = np.round(df_MonthPMdata['issueVal'].mean(
                        skipna=True))  # df_MonthPMdata 데이터프레임에서 issueVal열의 값들의 평균 계산
                    # avg_quater.append(avg_issueVal_quater)
                    result_data.append(
                        [city, PMdata, year, quater, avg_issueVal_quater])
                    print(f'{year}년도 1분기 : {avg_issueVal_quater}')
                    print('-' * 50)
                elif month in range(4, 7):
                    # quater.append(f'{year}년도 2분기')
                    quater = f'{year}년도 2분기'
                    df_MonthPMdata = df_YearPMdata[df_YearPMdata['issueDate'].dt.month.isin([
                                                                                            4, 5, 6])]
                    avg_issueVal_quater = np.round(
                        df_MonthPMdata['issueVal'].mean(skipna=True))
                    result_data.append(
                        [city, PMdata, year, quater, avg_issueVal_quater])
                    # avg_quater.append(avg_issueVal_quater)
                    print(f'{year}년도 2분기 : {avg_issueVal_quater}')
                    # print('-' * 50)
                elif month in range(7, 10):
                    # quater.append(f'{year}년도 3분기')
                    quater = f'{year}년도 3분기'
                    df_MonthPMdata = df_YearPMdata[df_YearPMdata['issueDate'].dt.month.isin([
                                                                                            7, 8, 9])]
                    avg_issueVal_quater = np.round(
                        df_MonthPMdata['issueVal'].mean(skipna=True))
                    # avg_quater.append(avg_issueVal_quater)
                    result_data.append(
                        [city, PMdata, year, quater, avg_issueVal_quater])
                    print(f'{year}년도 3분기 : {avg_issueVal_quater}')
                    print('-' * 50)
                elif month in range(10, 13):
                    # quater.append(f'{year}년도 4분기')
                    quater = f'{year}년도 4분기'
                    df_MonthPMdata = df_YearPMdata[df_YearPMdata['issueDate'].dt.month.isin([
                                                                                            10, 11, 12])]
                    avg_issueVal_quater = np.round(
                        df_MonthPMdata['issueVal'].mean(skipna=True))
                    # avg_quater.append(avg_issueVal_quater)
                    result_data.append(
                        [city, PMdata, year, quater, avg_issueVal_quater])
                    print(f'{year}년도 4분기 : {avg_issueVal_quater}')
                    print('-' * 50)
                # result_data.append([city, PMdata, year, quater, avg_quater])
            result_data_unique = [
                x for x in result_data if result_data.count(x) == 1]
            print(result_data_unique)
    Df_Result = pd.DataFrame(result_data_unique, columns=[
                             '발령 지역 명', '미세먼지 항목 구분', '발령 연도', '분기', '평균 미세먼지 농도'])
    # Df_Result['분기'] = Df_Result['분기'].apply(lambda x: x[0])
    # Df_Result['평균 미세먼지 농도'] = Df_Result['평균 미세먼지 농도'].apply(lambda x: x[0])
    print(f'{city}별 Df_Result 데이터프레임')
    print(Df_Result)
    # Df_Result.to_csv(f'./QuaterDataFrame/{city}의 분기별 미세먼지 농도 추세.csv', encoding='utf-8')
    # print(f'{city} file is saved~!!')
    print('-' * 50)

    df_PM25 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM25']
    df_PM10 = Df_Result[Df_Result['미세먼지 항목 구분'] == 'PM10']
    # kind='line'
    plt.plot(df_PM25['분기'], df_PM25['평균 미세먼지 농도'],
             color='#FF00FF', label='PM25', marker='o')
    plt.xlabel('분기')
    plt.ylabel('평균 초미세먼지(PM25) 농도')
    plt.title(f'{city}의 분기별 초미세먼지(PM25) 농도 추세')
    # plt.xticks(rotation=90)
    plt.legend()
    plt.savefig(
        f'./QuaterImage/{city}_분기별_초미세먼지(PM25) 추세.png', dpi=400, bbox_inches='tight')
    print(f'{city}_분기별_초미세먼지(PM25) 추세.png file saved~!!')
    plt.show()

    plt.plot(df_PM10['분기'], df_PM10['평균 미세먼지 농도'],
             color='#00FF00', label='PM10', marker='s')
    plt.xlabel('분기')
    plt.ylabel('평균 미세먼지(PM10) 농도')
    plt.title(f'{city}의 분기별 미세먼지(PM10) 농도 추세')
    # plt.xticks(rotation=90)
    plt.legend()
    plt.savefig(
        f'./QuaterImage/{city}_분기별_미세먼지(PM10) 추세.png', dpi=400, bbox_inches='tight')
    print(f'{city}_분기별_미세먼지(PM10) 농도 추세.png file saved~!!')
    plt.show()

    plt.clf()


@app.get('/getUlfptca_MakeBoxPlot_Quarter')
async def getUlfptca_MakeBoxPlot_Quarter(q: int = None):
    plt.rcParams['font.family'] = 'Malgun Gothic'
    makeJSON('all')  # data.json파일을 생성
    json_file = 'data.json'  # 파일 이름 저장

    with open(json_file, 'r', encoding='utf-8') as file:
        dataUlfptcaAlarms = json.load(file)

    selected_df = CreateDataFrame(dataUlfptcaAlarms)  # selected_df을 생성

    # '분기' 필드 형성
    citylist = selected_df['districtName'].unique()
    listData = ['PM25', 'PM10']

    result_data = []
    for city in citylist:
        for PMdata in listData:
            # print(f'{city}의 분기별 {PMdata} 농도 추세')
            df_PMdata = selected_df.loc[(selected_df['districtName'] == city) & (
                selected_df['itemCode'] == PMdata), ['districtName', 'itemCode', 'issueDate', 'issueVal']]

            df_YearPMdata_list = []
            for year in range(2018, 2024):
                # print(f'{year}년도 데이터')
                df_YearPMdata = df_PMdata.loc[df_PMdata['issueDate'].dt.year == year, [
                    'districtName', 'itemCode', 'issueDate', 'issueVal']]
                months = df_YearPMdata['issueDate'].dt.month.unique()
                # df_YearPMdata['Quarter'] = ''

                df_Quarter_list = []
                for month in months:  # month변수의 값에 따라 분기값을 설정
                    if month in range(1, 4):
                        quarter = f'{year}년도 1분기'
                        # df_YearPMdata.loc[df_YearPMdata['issueDate'].dt.month.isin([1, 2, 3]), 'quarter'] = quarter
                        df_Q1 = df_YearPMdata.loc[df_YearPMdata['issueDate'].dt.month.isin(
                            [1, 2, 3]), ['districtName', 'itemCode', 'issueDate', 'issueVal']]
                        df_Q1.loc[:, 'Quarter'] = quarter
                        df_Quarter_list.append(df_Q1)
                    elif month in range(4, 7):
                        quarter = f'{year}년도 2분기'
                        # df_YearPMdata.loc[df_YearPMdata['issueDate'].dt.month.isin([1, 2, 3]), 'quarter'] = quarter
                        df_Q2 = df_YearPMdata.loc[df_YearPMdata['issueDate'].dt.month.isin(
                            [4, 5, 6]), ['districtName', 'itemCode', 'issueDate', 'issueVal']]
                        df_Q2.loc[:, 'Quarter'] = quarter
                        df_Quarter_list.append(df_Q2)
                    elif month in range(7, 10):
                        quarter = f'{year}년도 3분기'
                        df_Q3 = df_YearPMdata.loc[df_YearPMdata['issueDate'].dt.month.isin(
                            [7, 8, 9]), ['districtName', 'itemCode', 'issueDate', 'issueVal']]
                        df_Q3.loc[:, 'Quarter'] = quarter
                        df_Quarter_list.append(df_Q3)
                    elif month in range(10, 13):
                        quarter = f'{year}년도 4분기'
                        df_Q4 = df_YearPMdata.loc[df_YearPMdata['issueDate'].dt.month.isin(
                            [10, 11, 12]), ['districtName', 'itemCode', 'issueDate', 'issueVal']]
                        df_Q4.loc[:, 'Quarter'] = quarter
                        df_Quarter_list.append(df_Q4)

                if df_Quarter_list:
                    df_YearPMdata_quarter = pd.concat(
                        df_Quarter_list, ignore_index=True, axis=0)
                    df_YearPMdata_list.append(df_YearPMdata_quarter)
                # print(df_YearPMdata_list)
            if df_YearPMdata_list:
                df_YearPMdata_all = pd.concat(
                    df_YearPMdata_list, ignore_index=True, axis=0)
                result_data.append(df_YearPMdata_all)
                # print(df_YearPMdata_all)

    Df_Result = pd.concat(result_data, ignore_index=True, axis=0)
    print(Df_Result)
    print('-'*50)
    # print(Df_Result['Quarter'].unique())

    # boxplot생성
    # sns.set_style("darkgrid")
    # for q in Df_Result['Quarter'].unique():
    plt.figure(figsize=(12, 6))
    plt.title(f'{q} 각 도시의 미세먼지 농도 Boxplot')
    sns.boxplot(data=Df_Result, x='districtName', y='issueVal', hue='itemCode')
    plt.xlabel(f'{q} 각 도시별 미세먼지 농도')
    plt.ylabel('미세먼지 농도')
    plt.legend()
    plt.savefig(
        f'./QuaterBoxplot/{q}_도시별_미세먼지 농도 추세.png', dpi=400, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
