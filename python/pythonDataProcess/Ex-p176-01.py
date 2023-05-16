from pandas import Series

myindex = ['손오공', '저팔계', '사오정', '삼장법사']
mylist = [200, 300, 400, 100]

myseries = Series(data=mylist, index=myindex)

# print('\nseries name')
# print(myseries)

myseries.index.name='실적 현황'
print('\n# 시리즈의 색인 이름')
print(myseries.index.name) # 실적 현황

myseries.name='직원 실명'
print('\n# 시리즈의 이름')
print(myseries.name) # 직원 실명

print('\n# 반복하여 출력해보기')
for i in myseries.index:
    print('색인 : ' + i + ', 값 : ' + str(myseries[i]))