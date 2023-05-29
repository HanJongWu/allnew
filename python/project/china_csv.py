import pandas as pd
import csv
import os
import json
from pymongo import MongoClient

# excel file csv 변환
excel_file = '(업로드)c3_주요제조품 생산량(월별)_2304.xlsx'

csv_file = 'result.csv'

data = pd.read_excel(excel_file)

data.to_csv(csv_file, index=False, encoding='utf-8')

temp_filename = 'temp.csv'

with open(csv_file, 'r', newline='', encoding='utf-8') as file, open(temp_filename, 'w', newline='', encoding='utf-8') as temp_file:
    reader = csv.reader(file)
    writer = csv.writer(temp_file)

    for i, row in enumerate(reader):
        if i > 1:
            if len(row) > 6:
                writer.writerow(row[:1] + row[7:])

os.remove(csv_file)
os.rename(temp_filename, csv_file)

print('CSV 파일로 변환 완료:', csv_file)

# csv 파일 행,열 변환
origin_csv = 'result.csv'
output_csv = 'temp.csv'

df = pd.read_csv(origin_csv, encoding='utf-8', index_col='구분')
df_transposed = df.T

print(df_transposed)

df_transposed.to_csv(output_csv, encoding='utf-8', index_label='구분')
print(origin_csv, '파일이', output_csv, '파일로 행과 열을 바뀌어서 저장되었습니다.')

print(df_transposed)


# # csv 파일 json 변환

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file, \
            open(json_file, 'w', newline='', encoding='utf-8') as json_file:
        reader = csv.DictReader(csv_file)
        data = []
        for row in reader:
            data.append(row)
        temp = {}
        temp['data'] = data
        json.dump(temp, json_file, ensure_ascii=False)


csv_file = 'temp.csv'
json_file = 'chinaData.json'

csv_to_json(csv_file, json_file)

# MongoDB import

client = MongoClient('mongodb://192.168.1.25:27017')
db = client['project']
collection = db['chinaData']

json_file = 'chinaData.json'

with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)
    file = data['data']
    if isinstance(file, dict):
        file = [file]
    collection.insert_many(file)

print('MongoDB import..')
