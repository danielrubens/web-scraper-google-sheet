import json
from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time
from bs4 import BeautifulSoup


class GoomerUserService():
    def __init__(self, drive: webdriver, credentials: Dict) -> None:
        self.driver = drive
        self.url = "https://dashboard.goomer.app/login"
        self.username = credentials['username']
        self.password = credentials['password']
        self.lastevent = None

    def update_event(self, newevent: str):
        self.lastevent = newevent

    def enterGoomer(self):
        self.driver.get(self.url)
        self.update_event('pagina_login')

    def login(self):
        self.enterGoomer()
        self.driver.find_element(By.ID, "email").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        try:
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div/section[1]/div/form/button[1]').click()
            self.update_event('pagina_inicial_loja')
            time.sleep(2)
        except:
            print('Erro no Login')


class GoomerStore(GoomerUserService):
    def __init__(self, drive: webdriver, credentials: Dict) -> None:
        super().__init__(drive, credentials)

    def id_store(self):
        try:
            return '83200'
        except:
            print('Erro URL')
            return None

    def url_store(self):
        try:
            return f"https://dashboard.goomer.app/stores/{self.id_store()}/orders"
        except:
            print('Erro URL')
            return None

    def go_to_order_accept(self):
        self.driver.get(self.url_store())
        self.update_event('pagina_store')
        time.sleep(3)
        try:
            self.driver.find_element(By.XPATH,'//*[@id="survicate-box"]/div/div[2]/div[1]/button[2]').click()
        except:
            pass
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH,'//*[@id="root"]/div/section/section/main/div/div/div/div/div[1]/div/div/div[1]/div[1]/div[2]/button').click()
        except:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/section/section/main/div/div/div/div/div[1]/div/div/div[1]/div[1]/div[2]/button'))).click()

        self.update_event('pagina_pedidos_aceitos')
        time.sleep(2)

    def capture_orders(self):
        orders_html = []
        orders_id = []

        try:
            orders = self.driver.find_elements(By.CLASS_NAME, "order-id")
            for order in orders:
                order.click()
                time.sleep(0.7)
                orders_html.append(BeautifulSoup(self.driver.page_source).find('div', {'class': 'ant-modal-body'}))
                time.sleep(0.7)
                self.driver.find_elements(By.CLASS_NAME,"ant-modal-close-x")[0].click()
                time.sleep(0.7)
            return orders_html
        except:
            return orders_html
    
    def extract_pizzas(self,orders):
        
        ID_PEDIDO = []
        NOME_PEDIDO = []
        REFRI = []
        VALOR_02 = []
        FORMA_PAGAMENTO_02 = []
        MOTOBOY = []
        STATUS = []
        BAIRRO = []
        BORDA = []
        SABOR = []
        VALOR = []
        FORMA_PAGAMENTO = []
        TROCO = []
        STRING_ADICIONAR = []
        SABOR_NOVO = []
        NOME_CLIENTE = []
        TELEFONE = []
        PAGAMENTO = []
        ENDERECO = []
        pizzas = []
        
        for o in orders:
            tentativa = 1
            if tentativa > 0:
                for i in range(tentativa):            
                    time.sleep(1)                
                    nome_cliente = o.find('span', {'class': 'text'}).text
                    telefone = o.find('div', {'data-test': 'order-phone'}).find('span',{'class':'text'}).text
                    pagamento = o.find('div', {'data-test': 'order-payment'}).find('span', {'class': 'text'}).text
                    lista = pagamento.split('(')
                    forma_pagamento = lista[0]
                    try:
                        troco = lista[1][-7:-1]
                    except IndexError:
                        try:
                            troco = lista[1]
                        except IndexError:
                            troco = lista[0]
                    try:
                        valor = o.find('div',{'data-test':'total-info'}).text[-6:]
                    except AttributeError:
                        valor = 'A adicionar'
                    try:
                        endereco = o.find('div', {'class': 'address-container'}).find('p', {'class': 'address'}).text
                        lista_endereco = endereco.split(',')
                        bairro = lista_endereco[-3]
                    except AttributeError:
                        bairro = 'Retirada'
                        endereco = 'Retirada'
                    try:
                        time.sleep(2)                       
                        pizza_duas = list(o.findAll('div', {'class':'sc-iMrobD sc-cdJjGe jkJFgU erUTrs'}))
                        quantidade = list(o.findAll('div', {'class':'sc-iMrobD sc-cdJjGe exkbGi erUTrs'}))
                        
                        for j,q in zip(pizza_duas,quantidade):

                                if j.text == 'COMBO #1' or j.text == 'COMBO #2' or j.text == 'COMBO #3' or j.text == 'COMBO #4' or j.text == 'TERÇA DA BORDINHA' or j.text == 'QUARTA DUPLA' or j.text == 'QUINTA DO TBT' or j.text == 'Pizza Pequena' or j.text == 'Pizza Grande' or j.text == 'SEXTOU COM JURASSIC':
 
                                        if j.text == 'QUINTA DO TBT':
                                            REFRI.append(' ')                                                
                                        nm_pedido = j.text
                                        ID_PEDIDO.append(1)
                                        NOME_CLIENTE.append(nome_cliente)
                                        TELEFONE.append(telefone)
                                        PAGAMENTO.append(pagamento)
                                        if 'Pagamento online' in forma_pagamento:
                                            FORMA_PAGAMENTO.append('Transferência (PIX/PicPay)')
                                        else:
                                            FORMA_PAGAMENTO.append(forma_pagamento)
                                        FORMA_PAGAMENTO_02.append(' ')
                                        if 'Maquininha' in forma_pagamento:
                                            TROCO.append(forma_pagamento)
                                        else:
                                            TROCO.append(troco)
                                        
                                        
                                        ENDERECO.append(endereco)
                                        BAIRRO.append(bairro)
                                        NOME_PEDIDO.append(nm_pedido)
                                        VALOR.append(valor)
                                        VALOR_02.append(' ')
                                        MOTOBOY.append(' ')
                                        STATUS.append(' ')
        
                                if 'Guaran' in j.text or 'Coca' in j.text:        
                                        quantidade_refri = int(q.text)
                                        nm_refri = j.text
                                        for i in range(quantidade_refri):
                                            REFRI.append(nm_refri)                                        
                                        
                                        if len(REFRI) < len(NOME_CLIENTE):
                                            diff = len(NOME_CLIENTE) - len(REFRI)
                                            for i in range(diff):
                                                while len(REFRI) != len(NOME_CLIENTE):
                                                    REFRI.append(' ')
   
                                if 'Borda' in j.text:
                                        nm_borda = j.text
                                        quantidade_borda = int(q.text)
                                        for i in range(quantidade_borda):
                                            BORDA.append(nm_borda)
                                                                                
                                if j.text[:3] == '1/2' or j.text[1:4] == '1/2':
                                        nm_sabor = j.text
                                        quantidade_sabor = int(q.text)
                                        
                                        for i in range(quantidade_sabor):
                                            SABOR.append(nm_sabor)
    
                                        try:
                                            STRING_ADICIONAR = [str(SABOR[i])+' '+str(SABOR[i+1]) for i in range(0,len(SABOR),2)]
                                            #for i in STRING_ADICIONAR:
                                            #    print(f'Elemento em STRING_ADICIONAR: {i}')
                                            if len(STRING_ADICIONAR) > len(NOME_CLIENTE):
                                                NOME_CLIENTE.append(nome_cliente)
                                            if len(BORDA) < len(STRING_ADICIONAR):
                                                diff_borda = len(STRING_ADICIONAR) - len(BORDA)
                                                for i in range(diff_borda):
                                                    while len(BORDA) != len(STRING_ADICIONAR):
                                                        BORDA.append(' ')

                                        except IndexError:
                                            print('Erro no Index')
                                            print(f'STRING_ADICIONAR: {STRING_ADICIONAR} LEN: {len(STRING_ADICIONAR)}')
                                            print(f'SABOR: {SABOR} LEN: {len(SABOR)}')
                                            

                                if len(BORDA) == len(STRING_ADICIONAR) and len(STRING_ADICIONAR) > len(NOME_CLIENTE):
                                            while len(NOME_CLIENTE) != len(BORDA):
                                                NOME_CLIENTE.append(NOME_CLIENTE[-1])

                                
                                if len(ID_PEDIDO) < len(NOME_CLIENTE):
                                            while len(ID_PEDIDO) != len(NOME_CLIENTE):
                                                ID_PEDIDO.append(ID_PEDIDO[-1])


                                if len(TELEFONE) < len(NOME_CLIENTE):
                                            while len(TELEFONE) != len(NOME_CLIENTE):
                                                TELEFONE.append(TELEFONE[-1])

                                if len(TROCO) < len(NOME_CLIENTE):
                                            while len(TROCO) != len(NOME_CLIENTE):
                                                TROCO.append(TROCO[-1])
                                
                                if len(VALOR) < len(NOME_CLIENTE):
                                            while len(VALOR) != len(NOME_CLIENTE):
                                                VALOR.append(VALOR[-1])
                                            if len(VALOR)>1:
                                                if VALOR[-1] == VALOR[-2] and NOME_CLIENTE[-1] == NOME_CLIENTE[-2]:
                                                    quantidade_repetido = VALOR.count(VALOR[-1])
                                                    for i in range(quantidade_repetido-1):
                                                        VALOR.pop()
                                                    for i in range(quantidade_repetido-1):
                                                        garantidor = ' '
                                                        VALOR.append(i*garantidor)
                                
                                if len(VALOR_02) < len(NOME_CLIENTE):
                                            while len(VALOR_02) != len(NOME_CLIENTE):
                                                VALOR_02.append(VALOR_02[-1])
                                
                                if len(FORMA_PAGAMENTO) < len(NOME_CLIENTE):
                                            while len(FORMA_PAGAMENTO) != len(NOME_CLIENTE):
                                                FORMA_PAGAMENTO.append(FORMA_PAGAMENTO[-1])

                                if len(FORMA_PAGAMENTO_02) < len(NOME_CLIENTE):
                                            while len(FORMA_PAGAMENTO_02) != len(NOME_CLIENTE):
                                                FORMA_PAGAMENTO_02.append(FORMA_PAGAMENTO_02[-1])

                                if len(MOTOBOY) < len(NOME_CLIENTE):
                                            while len(MOTOBOY) != len(NOME_CLIENTE):
                                                MOTOBOY.append(MOTOBOY[-1])
                                
                                if len(STATUS) < len(NOME_CLIENTE):
                                            while len(STATUS) != len(NOME_CLIENTE):
                                                STATUS.append(STATUS[-1])

                                if len(BAIRRO) < len(NOME_CLIENTE):
                                            while len(BAIRRO) != len(NOME_CLIENTE):
                                                BAIRRO.append(BAIRRO[-1])
           
                        print(f'Comprimento LISTA ID_PEDIDO: {len(ID_PEDIDO)}')
                        print(f'Comprimento LISTA NOME_CLIENTE: {len(NOME_CLIENTE)}')               
                        print(f'Comprimento LISTA TELEFONE: {len(TELEFONE)}')
                        print(f'Comprimento LISTA NOME: {len(NOME_CLIENTE)}')
                        print(f'Comprimento LISTA SABOR: {len(SABOR)}')
                        print(f'Comprimento LISTA STRING_ADICIONAR: {len(STRING_ADICIONAR)}')
                        print(f'Comprimento LISTA BORDA: {len(BORDA)}')
                        
                        if len(REFRI) == 0:
                            REFRI.append(' ')
                        if len(REFRI) < len(NOME_CLIENTE):
                            while len(REFRI) != len(NOME_CLIENTE):
                                REFRI.append('')
                                
                        print(f'Comprimento LISTA REFRI: {len(REFRI)}')
                        print(f'Comprimento LISTA TROCO: {len(TROCO)}')
                        print(f'Comprimento LISTA VALOR: {len(VALOR)}')
                        print(f'Comprimento LISTA VALOR_02: {len(VALOR_02)}')
                        print(f'Comprimento LISTA FORMA_PAGAMENTO: {len(FORMA_PAGAMENTO)}')
                        print(f'Comprimento LISTA FORMA_PAGAMENTO_02: {len(FORMA_PAGAMENTO_02)}')
                        print(f'Comprimento LISTA MOTOBOY: {len(MOTOBOY)}')
                        print(f'Comprimento LISTA STATUS: {len(STATUS)}')
                        print(f'Comprimento LISTA BAIRRO: {len(BAIRRO)}')
                        

                    except AttributeError:
                        print("Pizza não encontrada")
                
        df = dict({'ID_PEDIDO':ID_PEDIDO,'TELEFONE':TELEFONE,'NOME':NOME_CLIENTE,'SABOR':STRING_ADICIONAR,'BORDA':BORDA,'REFRI':REFRI,'TROCO':TROCO,'VALOR':VALOR,'FORMA_PAGAMENTO':FORMA_PAGAMENTO,'VALOR_01':VALOR_02,'FORMA_PAGAMENTO_02':FORMA_PAGAMENTO_02,'MOTOBOY':MOTOBOY,'STATUS':STATUS,'BAIRRO':BAIRRO})
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in df.items()]))    
        df.dropna(subset = ["NOME"], inplace=True)
        df.to_csv('output.csv')

        for g,h,i,j,k,l,m,n,o,p,q,r,s,t in zip(ID_PEDIDO,TELEFONE,NOME_CLIENTE, STRING_ADICIONAR,BORDA,REFRI,TROCO,VALOR,FORMA_PAGAMENTO,VALOR_02,FORMA_PAGAMENTO_02,MOTOBOY,STATUS,BAIRRO):
            if all(x in pizzas for x in [g,h,i,j,k,l,m,n,o,p,q,r,s,t]):
                pass
            else:
                pizzas.append([g,h,i,j,k,l,m,n,o,p,q,r,s,t])
        return pizzas
