from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

EMAIL_REGEX = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
query = input("What would you like to search: ")

f = open("emails.txt", "w")

driver = webdriver.Chrome()
driver.get("https://www.google.com")


gInput = driver.find_element(By.XPATH, "//textarea[@title='Search']")
gInput.send_keys(query)
gInput.send_keys(Keys.RETURN)


moreBtn = driver.find_element(By.LINK_TEXT, 'More businesses')
moreBtn.click()




websites = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Website']")


webLinks = []
for site in websites:
    webLinks.append(site.get_attribute('href'))



for site in webLinks:
    driver.get(site)
    time.sleep(1)
    
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    time.sleep(1)

    
    try:
        emailElem = driver.find_element(By.PARTIAL_LINK_TEXT, "@")
        if emailElem.text == 'Email':
            continue
        print(emailElem.text)
        f.write(emailElem.text + "\n")

    except:
        
        page_source = driver.page_source

        emails = []
        for re_match in re.finditer(EMAIL_REGEX, page_source):
            email = re_match.group()
            if (email[0] != '/') and ('.com' in email) and (email not in emails):
                emails.append(email)
                f.write(email + "\n")
            
            
        if not emails:
            print('no email found on website: ' + site)
        
            continue

driver.quit()
f.close()
