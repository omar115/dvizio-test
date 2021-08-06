from os import name
import task
import traceback
import pandas as pd
import numpy as np

# driver code
def main():
    
    radius, zipcode = task.user_input()

    driver = task.init_driver()
    
    print("---Process Started---")

    task.login(driver)
    
    df = task.scrape_data(driver, radius, zipcode)

    # remove all whitespace
    df.replace(r'^\s*$', np.nan, regex=True)

    #remove null
    df = df.apply(lambda x: pd.Series(x.dropna().values))

    #save CSV
    df.to_csv(r'C:\Users\Ferntech\final_output.csv', index=False, header=True, mode='a')

    driver.quit()

    print("---Process Finished---")

main()