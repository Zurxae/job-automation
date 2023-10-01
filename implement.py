import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Implemenation of all functions file

EMAIL_REGEX = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
OUTPUT_FILE = 'output.txt'
BAD_EMAIL_FILE = 'bad_emails.txt'

def validate_email(email: str, emails: set[str], bad_emails: set[str]) -> bool:
    valid = False
    if (email[0] != '/') and ('.com' in email) and (email not in emails) and (email not in bad_emails):
        print(f'Found: {email}')
        emails.add(email)
        with open(OUTPUT_FILE, 'a') as fout:
            fout.write(email + "\n")
        valid = True
    return valid

def find_with_regex(page_source, emails: set[str], bad_emails: set[str]) -> bool:
    found = False
    for re_match in re.finditer(EMAIL_REGEX, page_source):
        email = re_match.group()
        temp = validate_email(email=email, emails=emails, bad_emails=bad_emails)
        if temp:
            found = True
    return found

# TESTED CHECK
def get_queries(input_file: str) -> tuple[list[str], set[str]]:
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
    
    bad_emails = set()
    with open(BAD_EMAIL_FILE, 'r') as fin:
        for line in fin:
            bad_emails.add(line.strip())

    return queryList, bad_emails

# TESTED CHECK
def search_query(driver, query: str):
    driver.get("https://www.google.com")
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
                driver.quit()
                exit()
                
    gInput.send_keys(query)
    gInput.send_keys(Keys.RETURN)

# TESTED CHECK
def get_web_links(driver) -> list:
    print('Getting website links...')
    moreBtn = driver.find_element(By.LINK_TEXT, 'More businesses')
    moreBtn.click()

    ratingBtn = driver.find_element(By.CSS_SELECTOR, "[data-filter-type='RATING']")
    ratingBtn.click()

    rating_3_5 = driver.find_element(By.CSS_SELECTOR, "[data-filter-type='3_5_AND_UP']")
    rating_3_5.click()

    driver.refresh()

    webLinks = []
    isNext = True

    while isNext:

        websites = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Website']")

        for site in websites:
            webLinks.append(site.get_attribute('href'))
        try:
            nextBtn = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next']")
            nextBtn.click()
        except:
            try:
                nextBtn = driver.find_element(By.CSS_SELECTOR, '[aria-label="Next"]')
                nextBtn.click()
            except:
                isNext = False
    return webLinks

def find_in_contact(driver, emails: set[str], bad_emails: set[str]):    
    try:
        print('trying to find contact link')
        contactBtn = driver.find_element(By.PARTIAL_LINK_TEXT, 'contact')
        print('found contact button')
        try:
            contactBtn.click()
        except:
            try:
                contact_link = contactBtn.get_attribute('href')
                print(f'contact_link: {contact_link}')
                driver.get(contact_link)
            except:
                print('Failed to GET contact page')
                return False
        try:
            emailElem = driver.find_element(By.PARTIAL_LINK_TEXT, "@")
            email = emailElem.text
            validate_email(email=email, emails=emails, bad_emails=bad_emails)
            return True
        except:
            page_source = driver.page_source
            return find_with_regex(page_source=page_source, emails=emails, bad_emails=bad_emails)
    except:
        print('Failed to FIND contact page')
        return False

def find_in_facebook(driver, emails: set[str], site: str, bad_emails: set[str]) -> bool:
    try:
        driver.get(site)
        try:
            facebookElem = driver.find_element(By.CSS_SELECTOR, "a[href^='https://www.facebook.com/']")
            facebook_link = facebookElem.get_attribute('href')
            try:
                driver.get(facebook_link)
                try:
                    closeBtn = driver.find_element(By.CSS_SELECTOR, "[aria-label='Close']")
                    closeBtn.click()
                    try:
                        emailElems = driver.find_elements(By.CSS_SELECTOR, '.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h')
                        for elem in emailElems:
                            email = elem.text
                            valid = validate_email(email=email, emails=emails, bad_emails=bad_emails)
                            if valid:
                                return True
                    except:
                        print('Could not find elements on facebook page')
                        return False
                except:
                    print('Could not perform close button action')
                    return False
            except:
                print('Could not get facebook page')
                return False
        except:
            print('Could not find facebook link')
            return False
    except:
        print('Could not get back to home page')
        return False

def execute_query(driver, query: str, webLinks: list, bad_emails: set[str]) -> int:

    with open(OUTPUT_FILE, 'a') as fout:
        fout.write('-' * 70)
        fout.write('\n\n')
        fout.write(f'Query: {query}\n\n\n')
        
    print(f'\n\nQuery: {query}\n')
        
    queryStartTime = time.time()
        
    emails = set()
    
    for site in webLinks:
        try:
            driver.get(site)
            print(f'CHECKING {str(site)}')
        except:
            continue
    
        try:
            emailElem = driver.find_element(By.PARTIAL_LINK_TEXT, "@")
            validate_email(email=emailElem.text, emails=emails, bad_emails=bad_emails)
        except:
            page_source = driver.page_source

            if not find_with_regex(page_source=page_source, emails=emails, bad_emails=bad_emails):
                print('Did not find email on home page')
                if not find_in_contact(driver=driver, emails=emails, bad_emails=bad_emails):
                    print('Did not find email in contact page')
                    if not find_in_facebook(driver=driver, emails=emails, site=site, bad_emails=bad_emails):
                        print('Did not find email in facebook')
        
    with open(OUTPUT_FILE, 'a') as fout:
        fout.write('\n\n')
        fout.write('-' * 70)
        fout.write('\n\n\n\n')

    print(f'\n\n\nVisited {len(webLinks)} company websites.\n')
    print(f'Found emails: {len(emails)} / {len(webLinks)}\n')

    elapsed_time = time.time() - queryStartTime
    print('Single Query Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), '\n')
    return len(emails)