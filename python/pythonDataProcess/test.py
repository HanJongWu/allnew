# a = {1: 'a'}
# a['name'] = "익명"
#
# del a[1]
#
# print(a)
#
# s1 = set([1, 2, 3])
# s1 = {1, 2, 3}
# # print(s1)
#
# l = [1, 2, 2, 3, 4, 3]
# # newlist = list(set(l))
#
# from copy import copy
# a = [1, 2, 3]
# b = copy(a)
# a[1] = 4
# # print(a)
# # print(b)
#
# money = 2000
# card = 1
# if money < 3000:
#      print(1)
# else:
#     print(2)
#
# a = 0
# while a < 10:
#     a = a +1
#     print("나무 %d번 찍음." %a)
# #     if a == 10:
# #         print("나무 컷")
# a = 0
# while a < 10:
#     a = a + 1
#     if a % 2 == 0:
#         continue
#     print(a)
#
# marks = [90, 25, 67, 45, 80]
# number = 0
# for mark in marks:
#     number = number + 1
#     if mark >= 60:
#         print("%d 합격" % number)
#     else:
# #         print("%d 불합격" % number)
#
# for i in range(2,10):        # 1번 for문
#     for j in range(1, 10):   # 2번 for문
#         print(i*j, end=" ")
#     print('')
#
# def sum_and_mul(a, b):
#     return a+b, a*b
#
# # print(sum_and_mul(1,2))
# #
# # f = open("C:/doit/새파일.txt", 'w')
# # for i in range(1, 11):
# #     data = "%d번째 줄입니다.\n" % i
# #     f.write(data)
# # f.close()
#
# with open("foo.txt", "w") as f:
# #     f.write("Life is too short, you need python")
#
# b = [1, 2, 3]
# def vartest2(b):
#     b = b.append(4)
# vartest2(b)
# print(b)

# class Calculator:
#     def __init__(self):
#         self.result = 0
#
#     def add(self, num):
#         self.result += num
#         return self.result
#
# cal1 = Calculator()
# cal2 = Calculator()
#
# print(cal1.add(3))
# print(cal1.add(4))
# print(cal2.add(3))
# print(cal2.add(7))