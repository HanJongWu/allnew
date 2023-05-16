while True:
    i = input("Input the number(q : Quit) : ")

    if i == 1:
        break
    else:
        if int(i) > 0:
            print("This is positive")
        elif int(i) == 0:
            print("This is zero")
        else:
            print("This is negative")