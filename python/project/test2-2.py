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


item_list = ["방직 당월 (억 미터)"]
time_range = pd.date_range(start='2018-01', end='2023-12', freq='QS')
quarterly_mean_df = pd.DataFrame(columns=item_list, index=time_range)

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

plt.figure(figsize=(16, 8))
plt.plot(quarterly_mean_df)
plt.title('2018 - 2023 24 Quarters Average Graph')
plt.xlabel('Time')
plt.ylabel('Mean Value')
plt.legend(item_list)

plt.savefig('quarterly_average_graph.png', dpi=300)
print(item_list, "saved..")
plt.show()