import pandas as pd
import json

# json_file = 'test.json'

# with open(json_file, 'r', encoding='utf-8') as f:
#     secrets = json.loads(f.read())

# print(type(secrets))

# # df = pd.DataFrame(list(secrets), index=None)
# df = pd.DataFrame.from_records(secrets, index='구분')
# print(type(df))
# print(df)

a_lsit = [1, 2, 3, 4]
b_list = ["a", "b", "c", "d"]
df2 = pd.DataFrame(a_lsit)
df = pd.DataFrame(b_list)

df3 = pd.concat([df2, df], axis=0)
print(df)
print(df2)
print(df3)

# with open(json_file, 'w', encoding='utf-8') as file:
#     json.dump(json_file)

# with open(json_file, 'r', encoding='utf-8') as f:
#     secrets = json.loads(f.read())


# dictionary = dict.fromkeys(secrets)
# print(dictionary)
# date = []
# value = []
# unit = []
# obs_status = []
# decimal = []
# for i in range(len(contents[1])):
#     date.append(contents[1][i]["date"])
#     value.append(contents[1][i]["value"])
#     unit.append(contents[1][i]["unit"])
#     obs_status.append(contents[1][i]["obs_status"])
#     decimal.append(contents[1][i]["decimal"])
# USA_GDP = pd.DataFrame({"date": date,
#                        "value": value,
#                         "unit": unit,
#                         "obs_status": obs_status,
#                         "decimal": decimal})
