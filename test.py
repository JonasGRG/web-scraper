import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

url = 'https://markets.ft.com/data/funds/tearsheet/historical?s=DK0060697548:DKK'
r = requests.get(url)

soup = BeautifulSoup(r.text, "xml")

table = soup.find('table', class_ ="mod-ui-table mod-tearsheet-historical-prices__results mod-ui-table--freeze-pane")

headers_row = []
for tr in table.find_all('tr'):
    for th in tr.find_all('th'):
        headers_row.append(th.text)
 

for match in table.find_all('span', {'class' : 'mod-ui-hide-small-below'}):
    match.clear()
    
data_rows = []
for tr in table.find_all('tr') [1:]:
    td_tags = tr.find_all('td')
    td_val  = [td_tag.text for td_tag in td_tags]
    data_rows.append(td_val)


data_frame = pd.DataFrame(data_rows, columns = headers_row)

# Function that converts the date format (thur, feb 02, 2023) to the format (dd-mm-year)
def format_date(x):
    return datetime.datetime.strptime(x, '%a, %b %d, %Y').strftime(
        '%d-%m-%Y')


data_frame['Date'] = data_frame['Date'].map(format_date)

# add ID_index column
data_frame.insert(0, 'ID_index', range(0, len(data_frame)))

headers_to_use = ["ID_index", "Date", "Close"]

date =  datetime.datetime.now().strftime("%d-%m-%Y")
file_name = f"data_{date}.csv"
data_frame.to_csv('/Users/jonas/Documents/SecureSpectrum/web-scraper/data_out/' + file_name, columns = headers_to_use, index=False)

current_date = datetime.date(2022, 12, 25)
print(current_date)