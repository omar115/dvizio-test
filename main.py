from os import name
import task
import traceback

def main():

    radius, zipcode = task.user_input()

    driver = task.init_driver()
    
    task.login(driver)

    task.scrape_data(driver, radius, zipcode)


main()