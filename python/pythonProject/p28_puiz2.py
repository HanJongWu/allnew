# def 위쪽에서 수식을 만들고 조건도 설정함 // listener 탭에서 수치 insert 가능
def handler():
    while True:
        v1, v2= (yield)
        print(f"{v1} + {v2} = {v1 + v2}")

listener = handler()
listener.__next__()
listener.send([5, 4])
listener.send([3, 6])