from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

query = input("What would you like to search: ")

driver = webdriver.Chrome()
driver.get("https://www.google.com")


gInput = driver.find_element(By.XPATH, "//textarea[@title='Search']")
gInput.send_keys(query)
gInput.send_keys(Keys.RETURN)

moreBtn = driver.find_element(By.XPATH, '//*[@id="rso"]/div[2]/div/div/div[1]/div[5]/div/div[1]/a/div/span[1]')
moreBtn.click()

#websites = driver.find_elements_by_css_selector("[aria-label=Website]")
#websites[0].click()

time.sleep(60)
