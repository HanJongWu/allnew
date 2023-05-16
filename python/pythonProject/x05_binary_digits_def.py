import random

def number(num):
    i = []

    while True:
        temp = num % 2
        num = num // 2
        i.append(temp)

        if num < 2:
            i.append(num)
            # return i
            break

    return i

num = random.randint(4, 16)
print(f'{num} binary number is : {number(num)}')

