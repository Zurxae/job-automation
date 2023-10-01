# Code Written By Steven Zhivov

import time
from selenium import webdriver
from implement import (
    get_queries,
    search_query,
    get_web_links,
    execute_query,
)

INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'output.txt'

# Program start time
st = time.time()

queryList, bad_emails = get_queries(input_file=INPUT_FILE)

# Create Chrome Driver instance
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# To clear existing file or make new one
with open(OUTPUT_FILE, 'w'):
    pass

total_emails = 0

for query in queryList:
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(2)
    driver.implicitly_wait(1)
    
    search_query(driver=driver, query=query)
    webLinks = get_web_links(driver=driver)
    total_emails += execute_query(driver=driver, query=query, webLinks=webLinks, bad_emails=bad_emails)

    driver.quit()

elapsed_time = time.time() - st
print('Total Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
print(f'Total emails found: {total_emails}')
with open(OUTPUT_FILE, 'a') as fout:
    fout.write('Total Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), '\n')
    fout.write(f'Total emails found: {total_emails}')
