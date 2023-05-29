import csv
from pymongo import MongoClient
from pymongo import InsertOne


client = MongoClient('mongodb://192.168.1.189:27017')
db = client['test']
collection = db['FabCapa_All_Trans']

csv_file = 'test123.csv'

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    documents = [row for row in reader]
    collection.insert_many(documents)

print('CSV 파일 import 완료')
