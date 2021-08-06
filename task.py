from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import traceback
import re
import time
import numpy as np

# function to initialize the chromedriver
def init_driver():
    driver = webdriver.Chrome(executable_path=r'C:\Users\Ferntech\Desktop\chromedriver.exe')
    driver.maximize_window()
    driver.delete_all_cookies()
    return driver

# login the portal
def login(driver):
    
    goto_link = 'https://www.tred.com/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip='
    try:
        driver.implicitly_wait(20)
        driver.get(goto_link)
        
    except:
        print(traceback.format_exc())

# take input of radius and zipcode from the user
def user_input():
    
    radius = input("Write your Radius including mi, i.e. 50 mi.: ")
    zipcode = input("Write your zipcode in numbers i.e. 1000: ")
    return radius, zipcode

# scrape data from the portal and save it to a CSV
def scrape_data(driver, radius, zipcode):
    li = []     # empty list
    df = pd.DataFrame()     # initialize dataframe

    # select radius, input zipcode
    select = Select(driver.find_element_by_xpath('/html/body/section/div/div/div[3]/div/section/div/div[1]/div/section/form/div[1]/div[2]/div[1]/select'))

    select.select_by_visible_text(radius)

    xpath_link = '/html/body/section/div/div/div[3]/div/section/div/div[1]/div/section/form/div[1]/div[2]/div[2]/input'

    driver.find_element_by_xpath(xpath_link).send_keys(zipcode)

    time.sleep(3)

    xpath_text = '/html/body/section/div/div/div[3]/div/section/div/div[2]/div[1]/div/div[1]/div/div/div/a/div[2]/h5'

    # loop to scrape all cards and scrape data
    i = 1
    while i > 0:

        xpath_text = '/html/body/section/div/div/div[3]/div/section/div/div[2]/div[1]/div/div['+str(i)+']/div/div/div/a/div[2]/h5'
        
        try:
            name = driver.find_element_by_xpath(xpath_text)
        except:
            return df
        try:
            if name.text == '' or name.text == 'nan':
                i = -2
        except:
            pass

        else:
            car_name=''
            car_price=''
            data=''
            try:
                driver.implicitly_wait(10)
                
                driver.find_element_by_xpath(xpath_text).click()
                xpath_text2 = '/html/body/section/div/div/div[2]/div[5]/div[2]/div/h1[1]'
                
                name = driver.find_element_by_xpath(xpath_text2)
                web_name = name.text

                # using re extract the year from text, and slice the string to get required value
                date = re.findall(r'.*([1-3][0-9]{3})',web_name)
                start = web_name.find(date[0])
                car_name = web_name[start:-9]
                print('Car name is : ', car_name)

                # extract price name
                price_xpath = '/html/body/section/div/div/div[2]/div[4]/div/div/div[2]/div/div/h2'
                try:
                    car_price = driver.find_element_by_xpath(price_xpath)
                    car_price = car_price.text
                    print('Car price is ', car_price)
                except:
                    car_price = 'SOLD'

                # extract table data
                for table in driver.find_elements_by_xpath('//*[contains(@id,"summary-table")]//tr'):
                    data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
                    
            except:
                print(traceback.format_exc())
                return df
            
            # append data to dataframe
            df = df.append({'Name': car_name,'Price':car_price,'Vehicle Summary':data}, ignore_index=True)

            driver.back()

        i = i + 1
    