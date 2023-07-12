# Code Written By Steven Zhivov

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time
import re

st = time.time()

EMAIL_REGEX = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
query = input("What would you like to search: ")

f = open("emails.txt", "w")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")


gInput = driver.find_element(By.XPATH, "//textarea[@title='Search']")
gInput.send_keys(query)
gInput.send_keys(Keys.RETURN)


moreBtn = driver.find_element(By.LINK_TEXT, 'More businesses')
moreBtn.click()


ratingBtn = driver.find_element(By.CSS_SELECTOR, "[data-filter-type='RATING']")
ratingBtn.click()

rating_3_5 = driver.find_element(By.CSS_SELECTOR, "[data-filter-type='3_5_AND_UP']")
rating_3_5.click()
time.sleep(1)

driver.refresh()
time.sleep(1)





webLinks = []
isNext = True

while isNext:

    websites = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Website']")

    for site in websites:
        webLinks.append(site.get_attribute('href'))
    
    try:
        nextBtn = driver.find_element(By.CSS_SELECTOR, "[jsname='db9cze']")
        nextBtn.click()
        time.sleep(1)

    except:
        isNext = False

emails = []
blackListEmails = ['example@gmail.com', 'info@email.com']

for site in webLinks:
    try:
        driver.get(site)
    except:
        continue
    time.sleep(1.5)
    
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    time.sleep(1)

    foundEmail = False
    
    try:
        emailElem = driver.find_element(By.PARTIAL_LINK_TEXT, "@")
        if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
            print(emailElem.text)
            emails.append(email)
            f.write(emailElem.text + "\n")
            foundEmail = True

    except:
        
        page_source = driver.page_source

        
        for re_match in re.finditer(EMAIL_REGEX, page_source):
            email = re_match.group()
            if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
                print(email)
                emails.append(email)
                f.write(email + "\n")
                foundEmail = True
            
            
        if not foundEmail:
            print('no email found on website: ' + site)

driver.quit()
f.close()



print(f'\n\n\nVisited {len(webLinks)} company websites.\n\n')

elapsed_time = time.time() - st
print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
