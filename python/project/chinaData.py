import pandas as pd
import json

excel_file = '(업로드)c3_주요제조품 생산량(월별)_2304.xlsx'

print(excel_file)

df = pd.read_excel(excel_file, engine="openpyxl", header=2, index_col='구분')


df = df.iloc[:, 6:].transpose().fillna(0)

json_file = 'chinaData.json'

# DataFrame 데이터 리스트로 변환
data = []
for index, row in df.iterrows():
    row_dict = {"구분": index}
    row_dict.update(row.to_dict(into=dict))
    data.append(row_dict)

# 리스트를 포함하는 JSON 객체를 만들기
json_output = json.dumps({"data": data}, ensure_ascii=False, indent=2)

with open(json_file, 'w', encoding='utf-8') as file:
    file.write(json_output)

print(df)
print("json saved..")
