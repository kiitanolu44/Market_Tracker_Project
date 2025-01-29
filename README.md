# Market Tracker Project

## Overview

The aim of this project is to develop a web scraping tool that tracks financial data from either **Yahoo Finance** or **VettaFi**.

Throughout the development process, I experimented with two different web scraping libraries: **Selenium** and **BeautifulSoup**. After testing both, I decided to use **BeautifulSoup** due to its simplicity and ease of use.  

While **Selenium** is an extremely powerful package, I found it challenging to wrap my head around it for this particular use case. In contrast, **BeautifulSoup** provided a more straightforward approach to extracting the required financial data.  

---

## Technologies Used

- **Python**  
- **BeautifulSoup** (for web scraping)  
- **Selenium** (tested but not used in the final version)  
- **Pandas** (for handling data)  
- **Requests** (for making HTTP requests)  

---

## Features

- Scrapes financial market data from **Yahoo Finance**/**VettaFi**  
- Extracts stock prices, trends, and other financial metrics  
- Outputs structured data in a readable format  
- Uses **BeautifulSoup** for parsing HTML  

---

## Potential Improvements

- **Automate Daily Scraping** – Set up a scheduled job to run the script daily.  
- **Database Storage** – Store scraped data in a database (PostgreSQL, MongoDB).  
- **Data Visualisation** – Use Matplotlib or Seaborn for trend analysis.  
