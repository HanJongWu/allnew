import json
from pymongo import MongoClient

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

print('JSON 파일 import 완료')
