import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime
import schedule

# Function that converts the date format (thur, feb 02, 2023) to the format (dd-mm-year)
def format_date(x):
    return datetime.datetime.strptime(x, '%a, %b %d, %Y').strftime(
        '%d-%m-%Y')


# main function that scrapes the table in the url and saves a file csv named data_{date}.csv containing ID's dates and closing prices
def scrape():
    url = 'https://markets.ft.com/data/funds/tearsheet/historical?s=DK0060697548:DKK'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "xml")

    table = soup.find('table', class_ ="mod-ui-table mod-tearsheet-historical-prices__results mod-ui-table--freeze-pane")

    # The headers are found and stored in a list
    headers_row = []
    for tr in table.find_all('tr'):
        for th in tr.find_all('th'):
            headers_row.append(th.text)
 

    # Here replicated data in the td's is removed
    for match in table.find_all('span', {'class' : 'mod-ui-hide-small-below'}):
        match.clear()

    # The data in the td's is located and stored a list
    data_rows = []
    for tr in table.find_all('tr') [1:]:
        td_tags = tr.find_all('td')
        td_val  = [td_tag.text for td_tag in td_tags]
        data_rows.append(td_val)

    # The lists containing the headers and data are stored in a pandas data frame
    data_frame = pd.DataFrame(data_rows, columns = headers_row)

    # The dates are reformated
    data_frame['Date'] = data_frame['Date'].map(format_date)

    # add ID_index column
    data_frame.insert(0, 'ID_index', range(0, len(data_frame)))

    # These are the headers which we wish to store in the csv
    headers_to_use = ["ID_index", "Date", "Close"]


    # The dataframe i saved as a csv file in the data_out folder. The file name will contain the current days date
    date =  datetime.datetime.now().strftime("%d-%m-%Y")
    file_name = f"data_{date}.csv"
    data_frame.to_csv('/Users/jonas/Documents/SecureSpectrum/web-scraper/data_out/' + file_name, columns = headers_to_use, index=False)
    
    
    # The code below ensures that the main function runs once a day at 08:00 until 2027-01-01
    schedule.every().day.at("08:00").do(scrape) 

    end_date = datetime.date(2027, 01, 01)
    run_script = True 
    while run_script:
        current_date = datetime.date.today()
        if current_date != end_date:
            run_script = False

        schedule.run_pending()
        time.sleep(1)


