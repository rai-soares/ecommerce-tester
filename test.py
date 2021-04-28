import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import glob
import csv

# Global variables
chromeDriverPath = "./chromedriver.exe"
    
# Function to screenshot page desktop
def screenshotPageDesktop(url, name):
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--hide-scrollbars")
    # Initialize driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # Get URL
    driver.get(url)
    time.sleep(3)
    # Find body
    e = driver.find_element_by_tag_name('body')
    total_height = e.size["height"]
    # Take screenshot
    driver.set_window_size(1920, total_height)
    driver.save_screenshot("./desktop/{}.png".format(name))
    driver.quit()
    return True

# Function to screenshot page mobile
def screenshotPageMobile(url, name):
    # Get height of page
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f"--window-size=375,1")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(3)
    height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
    driver.close()

    # Chrome options
    iphoneX = {
        "deviceMetrics": { "width": 375, "height": height, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option("mobileEmulation", iphoneX)
    # Initialize driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # Get URL
    driver.get(url)
    time.sleep(3)
    # Take screenshot
    driver.save_screenshot("./mobile/{}.png".format(name))
    driver.close()
    return True

# Function to clean folders
def cleanFolders():
    for file in glob.glob('./desktop/*'):
        os.remove(file)
    for file in glob.glob('./mobile/*'):
        os.remove(file)
    return True

# Script for run in many pages
cleanFolders()
with open('endpoints.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if (line_count > 0):
            url  = row[0]
            name = row[1]
            print(url)
            print(name)
            screenshotPageDesktop(url, name)
            screenshotPageMobile(url, name)
        line_count += 1

