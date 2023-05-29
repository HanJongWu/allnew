import pandas as pd
import csv
import os
import json

# excel file csv 변환
excel_file = 'FabCapacityData.xlsx'

csv_file = 'FabCapacityData.csv'

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
origin_csv = 'FabCapacityData.csv'
output_csv = 'test123.csv'

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


csv_file = 'test123.csv'
json_file = 'result.json'

csv_to_json(csv_file, json_file)

# def csv_to_json(csv_file, json_file):
#     with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file, \
#             open(json_file, 'w', newline='', encoding='utf-8') as json_file:
#         reader = csv.reader(csv_file)
#         col_names = next(reader)
#         data = []
#         for row in reader:
#             row_data = {}
#             for i, col in enumerate(row):
#                 row_data[col_names[i]] = col
#             data.append(row_data)
#         json.dump(data, json_file, ensure_ascii=False)


# csv_file = 'test123.csv'
# json_file = 'result.json'

# csv_to_json(csv_file, json_file)

# def csv_to_json(csv_file, json_file):
#     with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file, \
#             open(json_file, 'w', newline='', encoding='utf-8') as json_file:
#         reader = csv.reader(csv_file)
#         col_names = next(reader)
#         data = {}
#         for cols in reader:
#             for i, col in enumerate(cols):
#                 if col_names[i] not in data:
#                     data[col_names[i]] = col
#         json.dump(data, json_file, ensure_ascii=False)


# csv_file = 'test123.csv'
# json_file = 'result.json'

# csv_to_json(csv_file, json_file)

# def csv_to_json(csv_file, json_file):
#     with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file, \
#             open(json_file, 'w', newline='', encoding='utf-8') as json_file:
#         reader = csv.reader(csv_file)
#         col_names = next(reader)
#         docs = []
#         for cols in reader:
#             doc = {col_name: col for col_name, col in zip(col_names, cols)}
#             docs.append(doc)
#         json.dump(docs, json_file, ensure_ascii=False)


# csv_file = 'test123.csv'
# json_file = 'result.json'

# csv_to_json(csv_file, json_file)
