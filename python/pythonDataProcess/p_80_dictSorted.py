worldInfo = {'세탁기' : 50, '선풍기' : 30, '청소기' : 40, '냉장고' : 60}

myxticks = sorted(worldInfo, key=worldInfo.get, reverse=True)
print(myxticks)

revers_key = sorted(worldInfo.keys(), reverse=True)
print(revers_key)

chartdata = sorted(worldInfo.values(), reverse=True)
print(chartdata)
