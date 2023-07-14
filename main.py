# Code Written By Steven Zhivov

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time
import re

st = time.time()

EMAIL_REGEX = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

fout = open("output.txt", "w")

print('\nWelcome! Would you like to perform a single line or bulk search request?')

validInput = False
while not validInput:
    print('Please enter the number of the option you would like to select.\n')
    print('(1) Single Line Search\n')
    print('(2) Bulk Search Request  (Must prepare .txt file with each query on a new line.)\n')
    print('(3) Quit the program.\n')

    mode = input('')
    queryList = []

    if mode == '1':
        validInput = True
        query = input("\n\n\nWhat would you like to search: ")
        queryList.append(query)
    elif mode == '2':
        validInput = True
        with open('input.txt') as fin:
            for line in fin:
                queryList.append(line.strip())
    elif mode == '3':
        validInput = True
        exit()
    elif not mode.isdigit():
        print('\n\nPlease enter only the number.\n\n')
    else:
        print('\n\nPlease select one of the options.\n\n')


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)

for query in queryList:
    fout.write('-' * 70)
    fout.write('\n\n')
    fout.write(f'Query: {query}\n\n\n')
    print(f'\n\nQuery: {query}\n')
    queryStartTime = time.time()
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
            nextBtn = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next']")
            nextBtn.click()
            time.sleep(1)

        except:
            isNext = False
        

    emails = []
    blackListEmails = ['example@gmail.com', 'info@email.com', 'email', 'Email', 'Email Us']

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
            email = emailElem.text
            if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
                print(email)
                emails.append(email)
                fout.write(email + "\n")
                foundEmail = True

        except:
            
            page_source = driver.page_source

            
            for re_match in re.finditer(EMAIL_REGEX, page_source):
                email = re_match.group()
                if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
                    print(email)
                    emails.append(email)
                    fout.write(email + "\n")
                    foundEmail = True
                
            if not foundEmail:
                try:
                    contactBtn = driver.find_element(By.PARTIAL_LINK_TEXT, "Contact")
                except:
                    try:
                        contactBtn = driver.find_element(By.PARTIAL_LINK_TEXT, "contact") 
                    except:
                        try:
                            contactBtn = driver.find_element(By.PARTIAL_LINK_TEXT, "CONTACT")
                        except:
                            print('no email found on website: ' + site)
                            continue
                
                contactBtnPressed = False
                try:
                    contactBtn.click()
                    contactBtnPressed = True
                except:
                    pass

                if contactBtnPressed:
                    time.sleep(1)
            
                    html = driver.find_element(By.TAG_NAME, 'html')
                    html.send_keys(Keys.END)
                    time.sleep(.5)

                    foundEmail = False
                    
                    try:
                        emailElem = driver.find_element(By.PARTIAL_LINK_TEXT, "@")
                        email = emailElem.text
                        if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
                            print(email)
                            emails.append(email)
                            fout.write(email + "\n")
                            foundEmail = True

                    except:
                        
                        page_source = driver.page_source

                        
                        for re_match in re.finditer(EMAIL_REGEX, page_source):
                            email = re_match.group()
                            if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
                                print(email)
                                emails.append(email)
                                fout.write(email + "\n")
                                foundEmail = True

                if not foundEmail:
                    if contactBtnPressed:
                        driver.back()
                        time.sleep(1)

                        html = driver.find_element(By.TAG_NAME, 'html')
                        html.send_keys(Keys.END)
                        time.sleep(.5)

                    try:
                        facebookVisited = False
                        possibleFacebookList = driver.find_elements(By.TAG_NAME, 'a')
                        for link in possibleFacebookList:
                            if facebookVisited:
                                break
                            link = link.get_attribute('href')
                            if 'facebook.com' in str(link):
                                driver.get(link)
                                time.sleep(1)
                                closeBtn = driver.find_element(By.CSS_SELECTOR, "[aria-label='Close']")
                                closeBtn.click()
                                try:
                                    emailElems = driver.find_elements(By.CSS_SELECTOR, '.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h')
                                    
                                    for elem in emailElems:
                                        email = elem.text
                                        if (email[0] != '/') and ('@' in email) and ('.com' in email) and (email not in emails) and (email not in blackListEmails):
                                            print(email)
                                            emails.append(email)
                                            fout.write(email + "\n")
                                            foundEmail = True
                                            break
                                    facebookVisited = True
                                except:
                                    pass
                        if not foundEmail:
                            print('no email found on website: ' + site)
                    except:
                        print('no email found on website: ' + site)
                        continue
    
    fout.write('\n\n')
    fout.write('-' * 70)
    fout.write('\n\n\n\n')

    print(f'\n\n\nVisited {len(webLinks)} company websites.\n')
    print(f'Found emails: {len(emails)} / {len(webLinks)}\n')                       

    elapsed_time = time.time() - queryStartTime
    print('Single Query Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), '\n')


driver.quit()
fout.close()


elapsed_time = time.time() - st
print('Total Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
