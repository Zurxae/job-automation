import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Implemenation of all functions file

EMAIL_REGEX = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

def get_queries(input_file):
    print('\nWelcome! Would you like to perform a single line or bulk search request?')

    validInput = False
    while not validInput:
        print('Please enter the number of the option you would like to select.\n')
        print('(1) Single Line Search\n')
        print('(2) Bulk Search Request  (Must prepare a \'input.txt\' file with each query on a new line.)\n')
        print('(3) Quit the program.\n')

        mode = input('')
        queryList = []

        if mode == '1':
            validInput = True
            query = input("\n\n\nWhat would you like to search: ")
            queryList.append(query)
        elif mode == '2':
            validInput = True
            with open(input_file, 'r') as fin:
                for line in fin:
                    queryList.append(line.strip())
        elif mode == '3':
            exit()
        elif not mode.isdigit():
            print('\n\nPlease enter only the number.\n\n')
        else:
            print('\n\nPlease select one of the options.\n\n')
    
    return queryList

def get_web_links(driver, query):
    driver.get("https://www.google.com")
    time.sleep(1)

    try:
        gInput = driver.find_element(By.ID, "APjFqb")
    except:
        try:
            gInput = driver.find_element(By.CSS_SELECTOR, "textarea[title='Search']")
        except:
            try:
                gInput = driver.find_element(By.CSS_SELECTOR, "input[title='Search']")
            except:
                print('Could not find google search box. Exiting program...')
                exit()
                
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
    return webLinks

def execute_queries(driver, queryList, output_file):
    # To clear existing file or make new one
    with open(output_file, 'w'):
        pass

    for query in queryList:
        with open(output_file, 'a') as fout:
            fout.write('-' * 70)
            fout.write('\n\n')
            fout.write(f'Query: {query}\n\n\n')
        
        print(f'\n\nQuery: {query}\n')
        
        queryStartTime = time.time()
        
        webLinks = get_web_links(driver=driver, query=query)

        emails = set()
        
        for site in webLinks:
            try:
                website = requests.get(site)
            except:
                continue
            
            page_source = website.text
            # foundEmail = False

            for re_match in re.finditer(EMAIL_REGEX, page_source):
                email = re_match.group()
                if (email[0] != '/') and ('.com' in email) and (email not in emails):
                    print(email)
                    emails.add(email)
                    with open(output_file, 'a') as fout:
                            fout.write(email + "\n")
                    # foundEmail = True
            
            
                
            
        with open(output_file, 'a') as fout:
            fout.write('\n\n')
            fout.write('-' * 70)
            fout.write('\n\n\n\n')

        print(f'\n\n\nVisited {len(webLinks)} company websites.\n')
        # print(f'Found emails: {len(emails)} / {len(webLinks)}\n')                       

        elapsed_time = time.time() - queryStartTime
        print('Single Query Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), '\n')