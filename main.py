from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

driver = webdriver.Firefox()
driver.get("https://m.xuite.net/photo/zooz103")
more_button = driver.find_element(By.CLASS_NAME, 'albumlist-more')

while True:
	try:
		more_button.click()
		print('Clicked the "more" button')
	except StaleElementReferenceException as e:
		print('The "more" button is stale, reached the end of album list.')
		break

driver.close()
