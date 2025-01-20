import requests
from bs4 import BeautifulSoup
import pandas as pd

# this script is for the most actively traded stocks in the market
url_most_active = 'https://uk.finance.yahoo.com/markets/stocks/most-active/?start={}&count=25'

# this function splits a list of html table rows into records (list of lists)
def splitted(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

stocks_no = 0
df = pd.DataFrame()

# yahoo finance was blocking the initial webscraping attempt, this fix handled that
http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# to iterate over all 60 pages
for page in range(60):
    print(f"Fetching data from: {url_most_active.format(stocks_no)}")

    # retrieve page content
    r_active = requests.get(url_most_active.format(stocks_no), headers=http_headers)
    
    # successful or no
    if not r_active.ok:
        print(f"Failed to fetch data for page {page}, Status Code: {r_active.status_code}")
        break

    # parse html using lxml
    active_soup = BeautifulSoup(r_active.text, 'lxml')

    # Extract table headers
    table_headers = active_soup.find_all('th')
    titles = [header.text.strip() for header in table_headers]

    if not titles:
        print(f"No headers found on page {page}. Skipping this page.")
        continue

    # headers for the first iteration
    if df.empty:
        df = pd.DataFrame(columns=titles)

    # extract table rows (td)
    rows = active_soup.find_all('td')
    lines = []

    for row in rows:
        line = row.text.strip()
        lines.append(line)

    # previously had some issues pertaining to the headers
    if len(lines) % len(titles) != 0:
        print(f"Skipping page {page}: Data rows not divisible by headers.")
        continue

    # splitting list into iterable rows
    chunks = splitted(lines, len(titles))

    # append rows to df
    for chunk in chunks:
        if len(chunk) == len(titles) and not df.isin([chunk]).all(axis=1).any():
            df.loc[len(df)] = chunk

    # next page
    stocks_no += 25

# Save the data to a CSV file
df.to_csv("most_active_stocks.csv", index=False)