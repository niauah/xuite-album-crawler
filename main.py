from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()
driver.get("https://m.xuite.net/photo/zooz103")
more_button = driver.find_element(By.CLASS_NAME, 'albumlist-more')
print(more_button)

more_button.click()
more_button = driver.find_element(By.CLASS_NAME, 'albumlist-more')
print(more_button)
driver.close()
