#!/usr/bin/env python

me = {"name":"Han", "age" : 22, "gender" : "male"}
print(me)

myname = me["name"]
print(myname)

me["age"] = 25
print(me)

# dict ◈키 (key) 로 색인되는 객체들을 저장한 해시테이블
dict={}
print(dict)

me[10] = 10
print(me)

me['10'] = 10
print(me)

me['job'] = "teacher"
print(me)

me['List'] = [1, 2, 3, 4, 5]
print(me)

me[(1, 2)] = "this is value"
print(me)

me[3] = (3, 'aa', 5)
print(me)

print("=========")
print(f'me[list] : {me["List"]}')
print(f'me[(1, 2] : {me[(1, 2)]}')
print(f'me[(3] : {me[(3)]}')

print(f'me[(1, 2] : {me[(1, 2)]}')
me[(1, 2)] = "This is real value"
print(f'me[(1, 2] : {me[(1, 2)]}')

# dict ◈키 (key) 로 색인되는 객체들을 저장한 해시테이블
dic = {'a' : 1234, "b" : "blog", "c" : 3333}

if 'b' in dic:
    print("b is exist")
else:
    print("b is not exist")

if 'e' in dic:
    print("e is exist")
else:
    print("e is not exist")

if 'blog' in dic.values():
    print("value is exist")
else:
    print("value is not exist")

print(dic.keys())

# dic.key 딕셔너리는 키와 값의 쌍으로 이루어진 데이터 타입, key 값만 뽑을때 사용
for k in dic.keys():
    print(f'key : {k}')

print(dic.values())

for v in dic.values():
    print(f'value : {v}')

print(dic.items())

for i in dic.items():
    print(f'all : {i}')
    print(f'key : {i[0]}')
    print(f'value : {i[1]}')
    print()

# dic.get get(x) 함수는 x라는 key에 대응되는 value값을 돌려준다.
v1 = dic.get('b')
print(f"dic.get['b'] : {v1}")

v2 = dic.get('z')
print(f"dic.get['z'] : {v2}")

# del
print(f'before : {dic}')

del dic['c']

print(f'after : {dic}')

# clear
dic.clear()
print(f'doc : {dic}')