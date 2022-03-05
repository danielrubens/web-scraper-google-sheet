import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
from ingestors import ingestors
from scrapy import GoomerStore
from writer import DataWriter
from schedule import repeat, every, run_pending



if __name__ == "__main__":

                
    # jurassicPizza
    # lamafiaPizza
    store_name = 'jurassicPizza'

    #key_gspread = '1Z4Q3QLlxh_VgBfQ_zr8iP0CB5bszSo8tdOrTDHdRr-c'
    key_gspread = '18jBfYs5sAN1lKiJxYAPeEVIovgc8S_82wwATZ9-KLo4'
    #credentials_gspread = 'jurassicpizza-api-6147e389352e.json'
    credentials_gspread = 'my-project-1499973958458-6e8cb64fe192.json'

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