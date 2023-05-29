from xml.etree.ElementTree import parse

tree = parse('xmlEx_03.xml')
myroot = tree.getroot()
print(type(myroot))
print('-' * 40)

familes = myroot.findall('가족')
print(type(familes))
print('-' * 40)

for onefamily in familes:
    for onesaram in onefamily:
        if len(onesaram) >= 1:
            print(onesaram[0].text)
        else:
            print(onesaram.attrib['이름'])
    print('-' * 40)
print('finished')
