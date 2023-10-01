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
import pywhatkit as kit

class Open_English_Unidade:

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
            self.wait2 = WebDriverWait(self.driver, 60)
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
        lFrame: str = '//iframe'
        lQuantidadeUnidade: str = '//*[@id="current-unit-indicator"]'
        lQuantidadeLicao: str = '(//*[@class="progress-bar-component"]/span)[2]'
        lSelecionaUnidade: str = '//*[@class="owl-item active"]'
        llabelAtividade: str = '//*[@class="css-1rynq56 r-1i10wst r-hbpseb"]'
        lSeta: str = '//*[@class="css-175oi2r r-1loqt21 r-1awozwy r-1777fci r-5scogr r-1udh08x r-u8s1d r-rxieca r-pezta r-ufaz5t"]'
        lContinuar: str = '//*[text()="Continuar"]'
        lVerDica: str = '//*[text()="Ver Dica"]'
        lVerificarResposta: str = '//*[contains(text(),"Resposta")]'
        lProximaLicao: str = '//*[text()="Próxima lição"]'
        lPreencherCampo: str = '//input'
        lCaixaSelecionar: str = '//*[@class="css-175oi2r r-1awozwy r-z2wwpe r-eg6o18 r-rs99b7 r-15ysp7h r-ggk5by r-1pn2ns4"]'
        lCaixaSequencia: str = '//*[@class="css-175oi2r r-r7j6xl r-18p6if4 r-kdyh1x r-rs99b7 r-ymttw5 r-5njf8e"]'
        lRespostaAudio: str = '//*[@class="css-175oi2r r-1awozwy r-r7j6xl r-kdyh1x r-d045u9 r-18u37iz r-1777fci r-1guathk r-1rcbeiy r-13awgt0"] '
        lCaixaImageText: str = '//*[@class="css-175oi2r r-1i6wzkk r-lrvibr r-1loqt21 r-1otgn73 r-1ydw1k6 r-y3xmzu"]'
        lImagemCorreta: str = '//*[@class="css-175oi2r r-r7j6xl r-d045u9 r-edyy15 r-1dzdj1l"]'


        self.elementos_seguir = [
            ("Continuar", lContinuar),
            ("VerificarResposta", lVerificarResposta),
            ("VerDica", lVerDica),
        ]

        elementos = [
            ("Seta", lSeta),
            ("PreencherCampo", lPreencherCampo),
            ("CaixaSelecionar", lCaixaSelecionar),
            ("CaixaSequencia", lCaixaSequencia),
            ("RespostaAudio", lRespostaAudio),
            ("CaixaImageText", lCaixaImageText),
            ("ImagemCorreta", lImagemCorreta),
            ("ProximaLicao", lProximaLicao),
            ]
        
        self.elementos_acoes = {
            "Seta": self.acao_seta,
            "Continuar": self.acao_continuar,
            "VerificarResposta": self.acao_verificar_resposta,
            "VerDica": self.acao_ver_dica,
            "ProximaLicao": self.acao_proxima_licao,
            "PreencherCampo": self.acao_preencher_campo,
            "CaixaSelecionar": self.acao_caixa_selecionar,
            "CaixaSequencia": self.acao_caixa_sequencia,
            "RespostaAudio": self.acao_resposta_audio,
            "CaixaImageText": self.acao_caixa_image_text,
            "ImagemCorreta": self.acao_imagem_correta,
        }
        
        try:
            selecaoQuantidadeLicao = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lQuantidadeLicao)))
            quantidadeLicao = selecaoQuantidadeLicao.text
        except:
            logger.warning('elemento não encontrado.')

        try:
            valores = quantidadeLicao.split('/')
            inicioUnidade = int(valores[0])
            fimUnidade = int(valores[1])
        except:
            pass

        try:
            selecaoUnidade = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaUnidade)))
            listaUnidade = self.driver.find_elements(By.XPATH, lSelecionaUnidade)
        except:
            logger.warning('elemento não encontrado.')

        try:
            listaUnidade[2].click()
        except:
            logger.warning('elemento não encontrado.')

        try:
            selecaoFrame = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lFrame)))
            self.driver.switch_to.frame(selecaoFrame)
        except:
            logger.warning('Elemento não encontrado.')
        
        while inicioUnidade < fimUnidade:
            time.sleep(1)

            validar_quantidade = self.validar_quantidade(llabelAtividade)
            if validar_quantidade:
                self.acao_proxima_licao()
                inicioUnidade += 1

            if self.valida_elemento():
                self.acao_seguir()
            else:
                lElemento = False
                for elemento_nome, elemento_xpath in elementos:
                    try:
                        elemento = self.driver.find_elements(By.XPATH, elemento_xpath)
                        if len(elemento) > 0:
                            logger.success(f"{elemento_nome} está ativo. Clicando nele...")
                            lElemento = True
                            break
                    except Exception as e:
                        print(e)    
                if lElemento:
                    self.elementos_acoes[elemento_nome](elemento_xpath, elemento_nome, elemento)
                else:
                    self.acao_continuar(xPathBotao=lContinuar)

        self.driver.switch_to.default_content()

        self.enviar_mensagem()

    def validar_quantidade(self, llabelAtividade) -> bool:
        try:
            selecaoQuantidade = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, llabelAtividade)))
            quantidade = selecaoQuantidade.text
        except:
            logger.warning('Elemento não encontrado.')
        
        try:
            valores = quantidade.split('/')
            inicio = int(valores[0])
            fim = int(valores[1])
        except:
            pass

        if inicio == fim:
            return True
        else:
            return False
     
    def valida_elemento(self) -> bool:
        tipo = By.XPATH
        path = self.elementos_seguir[0][1]

        try:
            self.driver.find_element(by=tipo, value=path)
        except NoSuchElementException as e:
            return False
        return True

    def acao_seguir(self):
        time.sleep(1)
        while True:
            for elemento_nome, elemento_xpath in self.elementos_seguir:
                try:
                    elemento = self.driver.find_elements(By.XPATH, elemento_xpath)
                    if len(elemento) > 0:
                        logger.success(f"{elemento_nome} está ativo. Clicando nele...")
                        break
                except Exception as e:
                    print(e)

            self.elementos_acoes[elemento_nome](elemento_xpath, elemento_nome)
            
            if elemento_nome == 'Continuar':
                break
            elif elemento_nome == "VerificarResposta":
                self.acao_verificar_resposta(tipo="Preenchido")
                self.acao_seguir()
                break
        
    def acao_proxima_licao(self, xPathBotao: str = None, nome: str = None, elemento: str = None):
        llabelAtividade: str = '//*[@class="css-1rynq56 r-1i10wst r-hbpseb"]'
        lProximaLicao: str = '//*[text()="Próxima lição"]'
        lFrame: str = '//iframe'
        lXis: str = '//*[text()="×"]'

        if self.valida_elemento():
            self.acao_seguir()

        try:
            selecaoQuantidade = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lProximaLicao)))
            selecaoQuantidade.click()
        except:
            logger.warning('Elemento não encontrado.')

        try:
            selecaoQuantidade = self.wait2.until_not(
                condicaoEsperada.presence_of_element_located((By.XPATH, lProximaLicao)))
        except:
            logger.warning('Elemento não encontrado.')

        time.sleep(1)

        self.driver.switch_to.default_content()

        try:
            selecaoFrame = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lFrame)))
            self.driver.switch_to.frame(selecaoFrame)
        except:
            logger.warning('Elemento não encontrado.')

    def acao_continuar(self, xPathBotao, nome: str = None):
        try:
            selecaoBotao = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, xPathBotao)))
            selecaoBotao.click()
        except:
            logger.warning(f'{nome} não encontrado.')
    
    def acao_ver_dica(self, xPathBotao, nome):
        try:
            selecaoBotao = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, xPathBotao)))
            selecaoBotao.click()
        except:
            pass
        
        self.acao_verificar_resposta(tipo='loop')

    def acao_verificar_resposta(self, xPathBotao: str = None, nome: str = None, tipo: str = None):
        xPathBotao = self.elementos_seguir[1][1]
        if tipo == 'loop':
            for i in range(3):
                try:
                    selecaoBotao = self.wait.until(
                        condicaoEsperada.presence_of_element_located((By.XPATH, xPathBotao)))
                    selecaoBotao.click()
                except:
                    pass
                
                if self.valida_elemento():
                        break
        elif tipo == 'Preenchido':
            try:
                selecaoBotao = self.wait.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, '//*[text()="Verifique a Resposta"]')))
                selecaoBotao.click()
            except:
                pass
        else:
            try:
                selecaoBotao = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, xPathBotao)))
                selecaoBotao.click()
            except:
                pass

    def acao_seta(self, xPathBotao, nome: str = None, elemento: str = None):
        for i in range(10):
            time.sleep(1)
            try:
                selecaoBotao = self.wait.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, xPathBotao)))
                selecaoBotao.click()
            except:
                logger.warning(f'{nome} não encontrado.')
            
            if self.valida_elemento():
                break
        
        self.acao_seguir()

    def acao_preencher_campo(self, xPathBotao, nome, elemento):
        for e in elemento:
            e.send_keys('a')

        self.acao_verificar_resposta(tipo='Preenchido')
        self.acao_seguir()

    def acao_caixa_selecionar(self, xPathBotao, nome, elemento):
        lOpcao = '//*[@class="css-175oi2r r-18u37iz"]'
        for e in elemento:
            try:
                e.click()
            except:
                pass
            time.sleep(1)
            try:
                selecaoBotao = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lOpcao)))
                selecaoBotao.click()
            except:
                pass
        
        self.acao_verificar_resposta(tipo='validar')
        self.acao_seguir()
            

    def acao_caixa_sequencia(self, xPathBotao, nome, elemento):
        for e in elemento:
            time.sleep(1)
            e.click()
        
        self.acao_verificar_resposta(tipo='Preenchido')
        self.acao_seguir()

    def acao_resposta_audio(self, xPathBotao, nome, elemento):
        for e in elemento:
            time.sleep(2)
            e.click()

            if self.valida_elemento():
                self.acao_seguir()
                break

    def acao_caixa_image_text(self, xPathBotao, nome, elemento):
        for e in elemento:
            time.sleep(1)
            e.click()

        self.acao_seguir()

    def acao_imagem_correta(self, xPathBotao, nome, elemento):
        time.sleep(1)
        for e in elemento:
            try:
                e.click()
            except:
                pass

            time.sleep(1)
            self.acao_verificar_resposta(tipo='validar')

            if self.valida_elemento():
                self.acao_seguir()
                break
    def enviar_mensagem(self):
        hoje = datetime.now()
        hora = hoje.hour
        minute = hoje+timedelta(minutes=1)
        minuto = minute.minute

        kit.sendwhatmsg("+5511992022640" ,  "Faz a ultima lição da unidade lá cara!!" ,  hora ,  minuto ,  10 ,  True ,  2 )

if __name__ == '__main__':
    executa = Open_English_Unidade()
    executa.start()