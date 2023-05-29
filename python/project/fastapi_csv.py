from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get('/')
def healthCheck():
    return "OK"


@app.get('/getcsv')
def getcsv():
    csv_file = '123.csv'

    df = pd.read_csv(csv_file)
    json_data = df.to_json()

    return json_data
