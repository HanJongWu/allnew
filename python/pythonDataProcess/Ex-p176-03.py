from pandas import Series, DataFrame

myindex1 = ['성춘향', '이몽룡', '심봉사']
mylist1 = [40, 50, 60]

myindex2 = ['성춘향', '이몽룡', '빵덕어멈']
mylist2 = [20, 40, 70]

myseries1 = Series(data=mylist1, index=myindex1)
myseries2 = Series(data=mylist2, index=myindex2)

print('\nSeries1 print')
print(myseries1)

print('\nSeries2 print')
print(myseries2)

print('\nSeries1 + Series2')
result = myseries1.add(myseries2, fill_value = 10)
print(result)

print('\nSeries1 - Series2')
result = myseries1.sub(myseries2, fill_value = 30)
print(result)
