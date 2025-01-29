from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# initialise WebDriver
driver = webdriver.Chrome()
base_url = 'https://etfdb.com/screener/'

# open the website
driver.get(base_url)
time.sleep(3)

# extract columns
columns = driver.find_elements(By.TAG_NAME, 'th')
headers = [col.text.strip() for col in columns][:7]

print("Extracted columns:", headers)

if not headers:
    raise ValueError("Column headers could not be found!")

# for storing extracted data
data = []
page_number = 1 

while True:
    try:
        print(f"\nScraping page {page_number}...")

        # get current table row count
        rows_before = driver.find_elements(By.XPATH, "//table/tbody/tr")
        rows_count_before = len(rows_before)

        # extract table rows data
        for row in rows_before:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                row_data = [cell.text.strip() for cell in cells][:7]
                data.append(row_data)

        # find "next" button
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next')]")))

            next_button.click()
            time.sleep(3)

            # Wait for new table data (ensures we are on a new page)
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.XPATH, "//table/tbody/tr")) > rows_count_before)

            # next page
            page_number += 1
            time.sleep(2)

        except:
            print("No more 'Next' button found. Exiting loop.")
            break

    except Exception as e:
        print("An error occurred:", e)
        break

# close the browser
driver.quit()

# to df
df = pd.DataFrame(data, columns=headers)

print("\nSample Data Extracted:")
print(df.sample(20))

df.to_csv("scraped_data.csv", index=False)
print("\nData saved to 'scraped_data.csv'")
