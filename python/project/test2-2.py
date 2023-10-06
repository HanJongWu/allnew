import json
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'


def quarter_mean(year, quarter):
    file_path = f"./{year}/quarters/{year}_{quarter}_data.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            quarter_data = json.load(file)
    except FileNotFoundError:
        return None

    df = pd.DataFrame(quarter_data)

    mean_values = {}
    item_list = ["방직 당월 (억 미터)"]

    for item in item_list:
        mean_values[item] = df[item].mean()

    return mean_values



quarters = ['Q1', 'Q2', 'Q3', 'Q4']

for year in range(2018, 2024):
    for quarter in quarters:
        mean_values = quarter_mean(year, quarter)
        if mean_values is None:
            continue
        last_month = int(quarter[-1]) * 3
        quarterly_mean_df.loc[pd.Timestamp(
            f"{year}-{last_month}")] = list(mean_values.values())

quarterly_mean_df.fillna(method='ffill', inplace=True)

