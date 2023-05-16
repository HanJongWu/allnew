import numpy as np
import pandas as pd
from pandas import Series, DataFrame

#.read_csv함수를 이용하여 파일을 읽어들여서 DataFrame 객체로 변환한 후 출력
filename = '과일매출현황.csv' #filename변수에 과일매출현황.csv파일명 저장
myframe = pd.read_csv(filename, index_col='과일명') #pd.read_csv함수를 이용하여 DataFrame객체로 변환. 과일명 열을 index로 사용
print('\n# 원본 데이터프레임')
print(myframe)
#       구입액   수입량
# 과일명
# 바나나   NaN  20.0
# 망고   30.0  25.0
# 멜론   60.0  30.0
# 사과   80.0   NaN

#.loc[] 메소드를 이용하여 결측치 채워넣기
print('\n# 누락 데이터 채워 놓기')
myframe.loc[myframe['구입액'].isnull(), ['구입액']] = 50.00
myframe.loc[myframe['수입량'].isnull(), ['수입량']] = 20.00
print(myframe)
#       구입액   수입량
# 과일명
# 바나나  50.0  20.0
# 망고   30.0  25.0
# 멜론   60.0  30.0
# 사과   80.0  20.0

# fillna() 메소드: DataFrame이나 Series에서 결측치를 지정된 값으로 대체
#print('\n# fillna() 메소드 이용하여 누락 데이터 채워넣기')
#mydict = {'구입액':50, '수입량':20}
#myframe.fillna(mydict, inplace=True)
#print(myframe)
#       구입액   수입량
# 과일명
# 바나나  50.0  20.0
# 망고   30.0  25.0
# 멜론   60.0  30.0
# 사과   80.0  20.0

print('\n# 구입액과 수입량의 각 소계')
print(myframe.sum(axis=0))
# 구입액    220.0
# 수입량     95.0
# dtype: float64

print('\n# 과일별 소계')
print(myframe.sum(axis=1))
# 과일명
# 바나나     70.0
# 망고      55.0
# 멜론      90.0
# 사과     100.0
# dtype: float64

print('\n# 구입액과 수입량의 평균')
print(myframe.mean(axis=0))
# 구입액    55.00
# 수입량    23.75
# dtype: float64

print('\n# 과일별 평균')
print(myframe.mean(axis=1))
# 과일명
# 바나나    35.0
# 망고     27.5
# 멜론     45.0
# 사과     50.0
# dtype: float64