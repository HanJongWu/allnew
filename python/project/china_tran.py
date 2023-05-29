import pandas as pd

origin_csv = 'FabCapacityData.csv'
output_csv = 'test123.csv'

df = pd.read_csv(origin_csv, encoding='utf-8', index_col='구분')
df_transposed = df.T

print(df_transposed)
# 구분         방직 당월 (억 미터)  방직 누계 (억 미터)  ...  핸드폰 전년동기대비 증가율 (%)  핸드폰 누계 증가율(%)
# 2017년 7월           60.2         216.8  ...                 4.1            9.8
# 2017년 8월           62.9         280.0  ...                 0.0            9.1

# df_transposed.columns = df_transposed.iloc[0]
# df_transposed = df_transposed[1:]

df_transposed.to_csv(output_csv, encoding='utf-8', index_label='구분')
print(origin_csv, '파일이', output_csv, '파일로 행과 열을 바뀌어서 저장되었습니다.')

print(df_transposed)
# 구분         방직 당월 (억 미터)  방직 누계 (억 미터)  ...  핸드폰 전년동기대비 증가율 (%)  핸드폰 누계 증가율(%)
# 2017년 7월           60.2         216.8  ...                 4.1            9.8
#
