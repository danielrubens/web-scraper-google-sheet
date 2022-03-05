from typing import List
import gspread


class DataWriter:
    def __init__(self, key:str, credentials:str) -> None:
        self.key = key
        self.credentials = credentials
        self.gs = gspread.service_account(filename=self.credentials)
        self.sh = self.gs.open_by_key(self.key)
        self.worksheet = self.sh.worksheet('PDV JP')          
        self.orders_written = []

    def write_data(self, dados:List):
        search = list(filter(lambda x: x == dados, self.orders_written))
        if not search:
            self.worksheet.append_row(dados)
            self.orders_written.append(dados)
