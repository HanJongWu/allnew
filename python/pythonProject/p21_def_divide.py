a = input("Input first number : ")
b = input("Input second number : ")

def num(a, b):
    return (a / b, a % b)

print(f"Input number {a} / {b}")
q, r = num(int(a), int(b))
print("Quotient : ", int(q))
print("Remainder : ", r)