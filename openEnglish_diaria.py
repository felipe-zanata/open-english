from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
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
            self.wait = WebDriverWait(self.driver, 2)
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
        lSelecionaNoticia: str = '//*[@id="lp2-practice-section"]/section/lp2-news-carousel/div/div/lp2-carousel/div[2]/div[1]/div/div[1]'
        lSelecionaListaNoticia: str = '//*[@id="lp2-practice-section"]/section/lp2-news-carousel/div/div/lp2-carousel/div[2]/div/div/div'
        lSelecionaSeta: str = '//*[@id="lp2-practice-section"]/section/lp2-news-carousel/div/div/lp2-carousel//i[@class="icon-arrow-right"]'
        lFrame = '//*[@id="angular-body"]/ngb-modal-window/div/div/lp2-media-player/div[2]/div/iframe'
        lSelecionaAssunto: str = '/html/body/div[2]/div[1]/div/div[1]/div/div[1]'
        lSelecionaBotao: str = '/html/body/div[2]/div[2]/div/div[2]/div[2]/button'
        lSelecionaBotaoCheck: str = '/html/body//button[@class = "button check"]'
        lSelecionaBotaoNext: str = '/html/body//button[@class = "button next"]'
        lSelecionaFeedBack: str = '/html/body/div[2]/div[2]/div/div[1]/div/div[4]/div[2]/div[3]'

        try:
            selecaoNoticia = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaNoticia)))
        except:
            logger.warning('elemento não encontrado.')

        try:
            listaNoticia = self.driver.find_elements(By.XPATH, lSelecionaListaNoticia)
        except:
            logger.warning('elemento não encontrado.')
        
        for l in listaNoticia:

            try:
                l.click()
            except:
                logger.warning('Elemento não encontrado.')
            
            try:
                selecaoFrame = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lFrame)))
                self.driver.switch_to.frame(selecaoFrame)
            except:
                logger.warning('Elemento não encontrado.')
            
            try:
                selecaoAssunto = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaAssunto)))
                selecaoAssunto.click()
            except:
                logger.warning('Elemento não encontrado.')
            
            i = 1
            while i <=3:
            
                x = 1
                while x <= 3:

                    try:
                        listaResposta = self.driver.find_elements(By.XPATH, 
                            f'/html/body/div[2]/div[{i+1}]/div/div[1]/div/div[4]/div[{x+1}]/div[2]/div/span[@class="answerBox"]')
                    except:
                        pass

                    for r in listaResposta:
                        r.click()

                        try:
                            selecaoBotao = self.wait2.until(
                                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaBotao)))
                            selecaoBotao.click()
                        except:
                            logger.warning('Elemento não encontrado.')
                        
                        try:
                            selecaoFeedback = self.wait2.until(
                                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaFeedBack)))
                            feedback = selecaoFeedback.text
                        except:
                            logger.warning('Elemento não encontrado.')

                        if "incorrect" not in feedback: break

                    try:
                        selecaoBotao = self.wait2.until(
                            condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaBotao)))
                        selecaoBotao.click()
                        x += 1
                    except:
                        pass
                        logger.warning('Elemento não encontrado.')

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

# Pega o XPath do iframe e atribui a uma variável
# iframe = driver.find_element_by_xpath("//*[@id="editor"]/div[3]/div[3]/iframe")

# Muda o foco para o iframe
# driver.switch_to.frame(iframe)

# Retorna para a janela principal (fora do iframe)
# driver.switch_to.default_content()