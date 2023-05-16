import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
print(type(driver))
print('-' * 50)

print('Go Daum~!!')
url = 'http://www.daum.net'
driver.get(url)

search_texbox= driver.find_element(By.NAME, 'q')

word = '집에가는법'
search_texbox.send_keys(word)

search_texbox.submit()

wait = 3
print(str(wait) + '동안 기다립니다.')
time.sleep(wait)

imagefile = '집에가는법.png'
driver.save_screenshot(imagefile)
print(imagefile + '이미지 저장')

wait = 3
driver.implicitly_wait(wait)

driver.quit()
print('brower를 종료합니다.')
