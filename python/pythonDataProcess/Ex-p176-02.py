from pandas import Series

myindex = ['강감찬', '이순신', '김유신', '광해군', '연산군', '을지문덕']
mylist = [50, 60, 40, 80, 70, 20]

myseries = Series(data=mylist, index=myindex)

print('\n number 1 print')
print(myseries)

print('\n number 2 print')
myseries[1] = 100
myseries[0::5] = 30
myseries[2:5] = 999
print(myseries)