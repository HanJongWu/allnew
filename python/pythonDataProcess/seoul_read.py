import pandas as pd
from pandas import Series, DataFrame

filename = 'seoul.csv'
df = pd.read_csv(filename)

print(df)
print('-' * 50)

result = df.loc[(df['시군구'] == ' 서울특별시 강남구 신사동')]
print(result)
print('-' * 50)

result = df.loc[(df['시군구'] == ' 서울특별시 강남구 신사동') & (df['단지명'] == '삼지')]
print(result)
print('-' * 50)

## index를 설정후 불러오기 [[ 두개 사용 불가능 ]]
newdf = df.set_index(keys=['도로명'])
print(newdf)
print('-' * 50)

result = newdf.loc[['동일로']]
count = len(newdf.loc[['동일로']])
print(result)
print('count : ', count)
print('-' * 50)

