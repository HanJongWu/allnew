import pandas as pd

afile = 'data03.csv'
bfile = 'data04.csv'
a = ['이름', '성별', '국어', '영어', '수학']
atable = pd.read_csv(afile, header=0, encoding='utf-8')
btable = pd.read_csv(bfile, header=None, encoding='utf-8', names=a)

atable['반'] = '1반'
btable['반'] = '2반'

mylist = []
mylist.append(atable)
mylist.append(btable)

result = pd.concat(objs=mylist, axis=0, ignore_index=True)
print(result)
print('-' * 40)

## 밑에거 필수
dropindex = result[result['이름'] == '심형식'].index
print(dropindex)
print('-' * 40)

newResult = result.drop(dropindex)
print(newResult)
print('-' * 40)

filename = 'result.csv'
result.to_csv(filename, encoding='utf-8')
print(filename+' saved...')