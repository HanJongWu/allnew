import requests
import pandas as pd


def excel_to_json(file_path):
    df = pd.read_excel(file_path)  # Excel 파일을 DataFrame으로 로드합니다.
    json_data = df.to_json(orient='records')  # DataFrame을 JSON으로 변환합니다.
    return json_data


# Excel 파일 경로
excel_file_path = '주요제조품 생산량(월별)_2304.xlsx'

# Excel 파일을 JSON으로 변환
json_data = excel_to_json(excel_file_path)


def send_json_data(json_data, server_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(server_url, data=json_data, headers=headers)
    return response


# JSON 서버 URL
server_url = 'http://localhost:8000/data'  # 적절한 URL로 대체해야 합니다.

# JSON 데이터를 서버에 전송
response = send_json_data(json_data, server_url)
