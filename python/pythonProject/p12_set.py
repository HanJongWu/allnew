#!/usr/bin/env python

even = set([0, 2, 4, 6, 8])
print(even)

hello = set("Hello")
print(hello)

s = even | hello
print(s)

p = even & hello
print(p)

even.add(10)
print(even)

hello.remove('e')
print(hello)

s1 = set([1, 2, 3, 4, 5])
s2 = set([4, 5, 6, 7, 8])

# intersection
print(s1.intersection(s2))
print(s1 & s2)

# union
print(s1.union(s2))
print(s1 | s2)

# difference
print(s1.difference(s2))
print(s2.difference(s1))

print(s1 - s2)
print(s2 - s1)

s3 = {1, 2, 3, 4, 5}

if s1 == s2:
    print("s1, s2 is same...")
else:
    print("s1, s2 is not same...")

if s1 == s3:
    print("s1, s3 is same...")
else:
    print("s1, s3 is not same...")

s4 = {6, 7, 8, 9, 10}

# isdisjoint 두 Set의 공통 요소 유무 체크
if s1.isdisjoint(s2):
    print("s1, s2 not have in common")
else:
    print("s1, s2 is have is common")

if s1.isdisjoint(s4):
    print("s3, s4 not have in common")
else:
    print("s3, s4 is have is common")

# issubset 서브 Set인지 체크
print(s1.issubset(s2))

s5 = {4, 5}

print(s1.issubset(s5))

s = {'r', 'd', 'n', 'd', 'o', 'm'}
print(f'set : {s}')

s.update({'a', 'b', 'c'})
print(f'set : {s}')

s.update({11, 12, 13})
print(f'set : {s}')

s.remove('a')
print(f'set : {s}')

s.discard("b")
print(f'set : {s}')

s.discard("a")
print(f'set : {s}')

print(f'set.pop() : {s.pop()}')
print(f'set : {s}')

print(f'set.pop() : {s.pop()}')
print(f'set : {s}')

print(f'set.pop() : {s.pop()}')
print(f'set : {s}')

s.clear()
print(f'set : {s}')

s = {'a', 'b', 'c'}

if 'a' in s:
    print('a is Exist')
else:
    print('a is not Exist')

if 'z' in s:
    print('z is Exist')
else:
    print('z is not Exist')

# len 문자열의 문자 개수를 반환하는 내장함수
print(f'Length of set : {len(s)}')