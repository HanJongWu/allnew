import pandas as pd
import json


def excel_to_json(file_path, output_path):
    # Excel 파일을 DataFrame으로 로드합니다.
    df = pd.read_excel(file_path)

    # DataFrame을 JSON으로 변환합니다.
    json_data = df.to_json(orient='records', force_ascii=False)

    with open(output_path, 'w', encoding='utf-8') as f:
        # JSON 데이터를 파일로 저장합니다.
        json.dump(json_data, f, ensure_ascii=False)


# Excel 파일 경로
excel_file_path = '주요제조품 생산량(월별)_2304.xlsx'

# JSON 파일 저장 경로
json_output_path = 'output.json'

# Excel 파일을 JSON으로 변환하고 저장
excel_to_json(excel_file_path, json_output_path)
