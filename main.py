from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
	StaleElementReferenceException, NoSuchElementException, InvalidSessionIdException
)

import re
import os
from urllib.request import urlretrieve
import argparse



def main(userid):
	result_dir = 'Results'
	driver = webdriver.Firefox()
	driver.get(f"https://m.xuite.net/photo/{userid}")
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

	os.makedirs(result_dir, exist_ok=True)
	os.chdir(result_dir)
	existing_dirs = os.listdir()
	for album in albums_list:
		base_dir = album['title']
		if base_dir in existing_dirs:
			continue
		os.mkdir(base_dir)
		print(f"Reading contents of {album['title']}...")
		for image_index in range(1, album['count']+1):
			for i in range(3):
				try:
					read_single_image(driver, f"{album['link']}/{image_index}", base_dir)
				except InvalidSessionIdException:
					continue
				else:
					break

	driver.close()


def read_single_image(driver, image_url, base_dir):
	driver.get(image_url)

	image_title = driver.find_element(By.CLASS_NAME, 'title').text.replace('JPG', 'jpg')
	text_title = image_title.replace('jpg', 'txt')

	image_src = driver.find_element(By.CLASS_NAME, 'single-show-image').get_attribute('src')
	urlretrieve(image_src, os.path.join(base_dir, image_title))
	try:
		single_description = driver.find_element(By.CLASS_NAME, 'desc').text
	except NoSuchElementException as e:
		print(f'No description found, skipping the image {image_title}')
		return
	print(f'Retrieving data of {image_title}')
	with open(os.path.join(base_dir, text_title), 'w') as file:
		file.write(single_description)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('userid')
	args = parser.parse_args()
	main(args.userid)
