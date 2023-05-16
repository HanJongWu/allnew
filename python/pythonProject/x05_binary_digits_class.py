import random

class number:
    def __init__(self, x):
        self.x = x

    def binary(self):
        num = self.x
        i = []

        while True:
            temp = num % 2
            num = num // 2
            i.append(temp)

            if num < 2:
                i.append(num)
                break

        return i


num = random.randint(4, 16)
n = number(num)
print(f'{num} binary number is: {n.binary()}')

