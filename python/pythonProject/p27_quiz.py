def square_number(nums):
    for i in nums:
        yield i * i

mynum = [1, 2, 3, 4, 5]
result = square_number(mynum)

for i in range(len(mynum))
    print(f"Square value of mynum[{i}] = {mynum[i]} : {next(result)}")
    # mynum = [1, 2, 3, 4, 5]
    # for nums in [1, 2, 3, 4, 5]:
    #     print(f'Square value of mynum[{nums - 1}] = {nums} : {nums * nums}')
    # # i = 1:
    # # nums = 5:

# for i in [1, 2, 3, 4, 5]:
#     print(f'Square value of mynum[{i-1}] = {i} : {i * i}')