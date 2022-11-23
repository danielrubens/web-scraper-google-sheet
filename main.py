import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
from ingestors import ingestors
from scrapy import GoomerStore
from writer import DataWriter
from schedule import repeat, every, run_pending


if __name__ == "__main__":

    store_name = 'STORE_NAME'

    key_gspread = 'GOOGLE_GSPREAD_KEY'
    credentials_gspread = 'JSON_GSPREAD'

    with open(f'{store_name}.json', 'r') as file:
            store = json.load(file)
    options = ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    goomer = GoomerStore(drive=driver, credentials=store)
    goomer.login()

    ws = DataWriter(key_gspread, credentials_gspread)

    goomer_ingestor = ingestors(
        store=store,
        writer=ws,
        driver=driver,
        goomer=goomer
    )

    @repeat(every(2).seconds)
    def job():
        goomer_ingestor.ingest()


    while True:
        run_pending()
        time.sleep(3)
