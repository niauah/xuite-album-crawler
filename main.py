from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

import re


def main():
	driver = webdriver.Firefox()
	driver.get("https://m.xuite.net/photo/zooz103")
	more_button = driver.find_element(By.CLASS_NAME, 'albumlist-more')

	while True:
	# for i in range(5):
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
	for album in albums_list[:2]:
		print(f"Reading contents of {album['title']}...")
		for image_index in range(1, album['count']+1):
			read_single_image(driver, f"{album['link']}/{image_index}")

	driver.close()


def read_single_image(driver, image_url):
	driver.get(image_url)

	image_title = driver.find_element(By.CLASS_NAME, 'title').text
	text_title = image_title.replace('jpg', 'txt')
	# TODO: download the image
	try:
		single_description = driver.find_element(By.CLASS_NAME, 'desc').text
	except NoSuchElementException as e:
		print(f'No description found, skipping the image {image_title}')
		return
	print(f'Retrieving data of {image_title}')
	with open(text_title, 'w') as file:
		file.write(single_description)

if __name__ == '__main__':
	main()
