from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import re

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

print('Collecting album informations...')
album_elements = driver.find_elements(By.CLASS_NAME, 'albumlist-photo-item')
albums_list = []
for element in album_elements:
	photo_name_element = element.find_element(By.CLASS_NAME, 'albumlist-photo-name')
	if '專輯歌錄' not in photo_name_element.text:
		continue
	photo_count = re.match(
			r'共([\d]+)張',
			element.find_element(By.TAG_NAME, 'p').text
		).group(1)
	albums_list.append(
		{
			"title": photo_name_element.text,
			"link": photo_name_element.get_attribute('href'),
			"count": int(photo_count),
		}
	)
print(albums_list)
driver.close()
