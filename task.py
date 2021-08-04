from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import traceback
import time


def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.delete_all_cookies()
    return driver

def login(driver):
    
    goto_link = 'https://www.tred.com/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip='
    try:
        driver.implicitly_wait(10)
        driver.get(goto_link)
    except:
        print(traceback.format_exc())

# take input of radius and zipcode from the user
def user_input():
    
    radius = input("Write your Radius: ")
    zipcode = input("Write your zipcode: ")
    return radius, zipcode

def scrape_data(driver, radius, zipcode):
    select = Select(driver.find_element_by_xpath('/html/body/section/div/div/div[3]/div/section/div/div[1]/div/section/form/div[1]/div[2]/div[1]/select'))

    select.select_by_visible_text(radius)

    xpath_link = '/html/body/section/div/div/div[3]/div/section/div/div[1]/div/section/form/div[1]/div[2]/div[2]/input'

    driver.find_element_by_xpath(xpath_link).send_keys(zipcode)
