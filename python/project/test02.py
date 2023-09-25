import pandas as pd
import matplotlib.pyplot as plt
import json
import os

plt.rcParams['font.family'] = 'AppleGothic'

for year in range(2018, 2024):
    json_file = f'./{year}/{year}_year_data.json'

    # json 파일이 있는 경우 읽어오기
    if os.path.isfile(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            year_data = json.load(file)

        # json 데이터를 DataFrame으로 변환
        year_df = pd.DataFrame(year_data)

        # "구분" 열을 날짜 형식으로 변환
        year_df['구분'] = pd.to_datetime(year_df['구분'], format="%Y년 %m월")

        # 원하는 항목의 리스트, 예를 들어 "방직 당월 (억 미터)"만 보고 싶으면 아래 리스트에 단일 항목을 입력
        item_list = ["방직 당월 (억 미터)", "화학섬유 당월 (만 톤)",
                     "공업용로봇 당월 (대)", "플라스틱원료 당월 (만 톤)"]

        # 원하는 항목별 그래프 그리기
        for item in item_list:
            plt.figure(figsize=(12, 6))
            plt.plot(year_df['구분'], year_df[item], marker='o')
            plt.title(f'{year}_{item} 그래프')
            plt.xlabel('기간')
            plt.ylabel(f'{item}')
            plt.grid()

            # 그래프 저장할 폴더와 파일명 설정
            filename = f'./{year}/{year}_{item}_그래프.png'

            # 파일에 그래프 저장
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f'{filename} file saved~!!')
            plt.show()
    else:
        print(f'No json file found for the year {year}')
