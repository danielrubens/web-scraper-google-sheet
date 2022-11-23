
import time
from scrapy import GoomerStore
from writer import DataWriter
from pydantic import BaseModel

class Pizza(BaseModel):
    nome: str
    sabor: str
    borda: str


class ingestors:
    def __init__(self, store, writer:DataWriter, driver, goomer:GoomerStore) -> None:
        self.store = store
        self.writer = writer
        self.driver = driver
        self.goomer = goomer
        

    def ingest(self):
        self.goomer.go_to_order_accept()
        orders = self.goomer.capture_orders()
        pizzas = self.goomer.extract_pizzas(orders)
        for pizza in pizzas:
           self.writer.write_data(pizza)#pizza[0], pizza[1], pizza[2]
        time.sleep(1)
