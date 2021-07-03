
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import uniform
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class PinterestScraper(object):


	def __init__(self,username,password,keyword,chromedriver_path='/Users/sebastian/Documents/Selenium Fun/chrome profile/chromedriver'):


		opt = Options()
		opt.add_experimental_option("debuggerAddress","localhost:9222")
		self.password = password
		self.driver = webdriver.Chrome(executable_path = chromedriver_path, chrome_options=opt)
		self.keyword = keyword

		self.driver.get("https://www.pinterest.co.uk/login/")
		self.scraped_list = []


	def loginPinterest(self):

		try:
			user_elem = self.driver.find_element_by_id("email")
			pass_elem = self.driver.find_element_by_id("password")

			#Enter username in email form field with delay

			for i in self.username:
				user_elem.send_keys(i)
				time.sleep(random.uniform(0.01,0.1))

			#Enter password in password form field with delay

			for i in self.password:
				pass_elem.send_keys(i)
				time.sleep(random.uniform(0.01,0.1))

			#Submit form

			pass_elem.send_keys(Keys.RETURN)

		except NoSuchElementException:
			print("Already logged in")

	def keywordSearch(self):


		try:

			#Find search box on pinterest

			search_box = self.driver.find_element_by_name('searchBoxInput')

			#Enter keyword into search box

			for i in self.keyword:
				search_box.send_keys(i)
				time.sleep(0.01)

			#Submit search
			search_box.send_keys(Keys.RETURN)
		except NoSuchElementException:
			print("Page Error")



	def findImages(self):

		#Wait until images are loaded

		delay = 5

		try:
			WebDriverWait(self.driver,delay).until(EC.presence_of_element_located((By.XPATH, "//img[@class='hCL kVc L4E MIw']")))
		except TimeoutError:
			print("Loading timed out")

		imageresults = self.driver.find_elements_by_xpath("//img[@class='hCL kVc L4E MIw']")


		for i in imageresults:
			self.scraped_list.append(i.get_attribute('src'))

		arr = self.scraped_list
		return arr

	def main(self):
		print("Attempting login...")
		self.loginPinterest()
		print("Searching for images...")
		self.keywordSearch()
		print("Image search succesful! Analysing results...")
		return self.findImages()


