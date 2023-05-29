from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get('/')
def healthCheck():
    return "OK"


@app.get('/getcsv')
def getcsv():
    csv_file = 'china_re.csv'

    df = pd.read_csv(csv_file)
    dict_data = df.to_dict()

    return dict_data
