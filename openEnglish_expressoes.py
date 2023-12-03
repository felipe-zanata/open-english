from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.edge.service import Service as EdgeService
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from datetime import timedelta
from loguru import logger
import pandas as pd
import time
import os

class Open_English:

    def __init__(self) -> None:
        logger.success('Bot iniciado com sucesso.')
        self.usuario = 'felipepxd@hotmail.com'
        self.senha = 'erika2808'
        self.openEnglish = 'https://student.openenglish.com/'

    def start(self):
        self.carrega_pagina_web()
        self.login()

        self.atividade_diaria()

        time.sleep(1)
        self.driver.quit()
        logger.success('Consulta finalizada com sucesso.')

    def carrega_pagina_web(self) -> None:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--start-maximized")
        logger.info('Iniciando Browser')
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            # self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            self.wait = WebDriverWait(self.driver, 10)
            self.wait2 = WebDriverWait(self.driver, 120)
            self.driver.get(self.openEnglish)
        except:
            logger.critical('Não foi possivel abrir a pagina web.')
            time.sleep(4)

    def login(self) -> None:
        logger.info('Realizando login')
        lLogin: str = 'login-email' 
        lSenha: str = 'login-password'
        lEntrar: str = 'login-submit'
        lTitulo: str = '//*[@id="lp2-practice-section"]/section/lp2-news-carousel'

        try:
            login = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.ID, lLogin)))
            login.send_keys(self.usuario)
        except:
            logger.critical('Campo login não encontrado.')

        try:
            senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.ID, lSenha)))
            senha.send_keys(self.senha)
        except:
            logger.critical('Campo senha não encontrado.')

        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.ID, lEntrar)))
            bt_entrar.click()
        except:
            logger.critical('Botão entrar não encontrado.')

        time.sleep(5)

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            self.driver.quit()

    def atividade_diaria(self) -> None:  # , listaRomaneios: list
        lSelecionaNoticia: str = '(//*[@id="lp2-practice-section"]//lp2-carousel/div[2]/div[1]/div/div[1])[3]'
        lFrame = '//iframe'
        lSelecionaResposta: str = '//*[@class="topic-li idiomsInteractionBased-li idiomsd-lcAnswerOption "]/span'
        lSelecionaCorrect: str = '//*[@correct="true"]'
        lSelecionaCaixa: str = '//*[@class="answerBox"]'
        lSelecionaStart: str = '//*[@class="button next"]'
        lSelecionaFinish: str = '//*[@class="button finish"]'
        lSelecionaClose: str = '//*[@class="button finish check"]'
        lSelecionaBotaoCheck: str = '/html/body//button[@class = "button check"]'
        lSelecionaBotaoNext: str = '/html/body//button[@class = "button next"]'

        while True:

            time.sleep(3)

            try:
                selecaoNoticia = self.wait.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaNoticia)))
                selecaoNoticia.click()
            except:
                logger.complete("Noticias finalizadas")
                break

            try:
                selecaoFrame = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lFrame)))
                self.driver.switch_to.frame(selecaoFrame)
            except:
                logger.warning('Elemento não encontrado.')
            
            try:
                selecaoStart = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaStart)))
                selecaoStart.click()
            except:
                logger.warning('Elemento não encontrado.')
            
            x=1
            while x <= 3:

                try:
                    selecaoRespostas = self.driver.find_elements(By.XPATH, lSelecionaResposta)
                except:
                    logger.warning('Elemento não encontrado.')

                time.sleep(1)
                i = 0
                while i <= 5:
                    elemento_resposta = selecaoRespostas[i]
                    elemento_check = selecaoRespostas[i +1]

                    if elemento_check.get_attribute('correct') == 'true':

                        elemento_resposta.click()
                    
                        try:
                            selecaoBotao = self.wait2.until(
                                condicaoEsperada.element_to_be_clickable((By.XPATH, lSelecionaBotaoCheck)))
                            selecaoBotao.click()
                        except:
                            logger.warning('Elemento não encontrado.')
                        if x == 3:
                            try:
                                selecaoBotao = self.wait2.until(
                                    condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaFinish)))
                                selecaoBotao.click()
                            except:
                                pass
                                logger.warning('Elemento não encontrado.')
                        else:        
                            try:
                                selecaoBotao = self.wait2.until(
                                    condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaBotaoNext)))
                                selecaoBotao.click()
                            except:
                                pass
                                logger.warning('Elemento não encontrado.')
                            
                        break
                    i += 2

                if x == 3:            
                    try:
                        selecaoBotao = self.wait2.until(
                            condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaClose)))
                        selecaoBotao.click()
                    except:
                        pass
                        logger.warning('Elemento não encontrado.')
                    
                    break

                x += 1

            self.driver.switch_to.default_content()

    def valida_elemento(self, tipo, path) -> bool:
        try:
            self.driver.find_element(by=tipo, value=path)
        except NoSuchElementException as e:
            return False
        return True

if __name__ == '__main__':
    executa = Open_English()
    executa.start()