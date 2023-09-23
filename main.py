# Code Written By Steven Zhivov

import time
from selenium import webdriver
from implement import get_queries
from implement import execute_queries

INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'output.txt'

# Program start time
st = time.time()

queryList = get_queries(input_file=INPUT_FILE)

# Create Chrome Driver instance
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

execute_queries(driver, queryList=queryList, output_file=OUTPUT_FILE)


driver.quit()


elapsed_time = time.time() - st
print('Total Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
