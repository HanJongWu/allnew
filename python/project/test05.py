import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np


def generate_Ulfptca_graph(year):
    plt.rcParams['font.family'] = 'Malgun Gothic'

    json_file = 'test.json'

    with open(json_file, 'r', encoding='utf-8') as file:
        dataUlfptcaAlarms = json.load(file)  # json.loads()함수: file을 json으로 변환

    # 데이터프레임 생성
    myframe_year = pd.DataFrame(dataUlfptcaAlarms)
    print(f'\n# {year} 데이터프레임 myframe_year 출력')
    print(myframe_year)
