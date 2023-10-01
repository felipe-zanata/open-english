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
from pymsgbox import *
from loguru import logger
import pandas as pd
import pyperclip as pc
import time
import os

class Vvlog_UX:

    def __init__(self) -> None:
        logger.success('Consulta no site iniciado com sucesso.')
        # self.proxy = '10.228.5.31:8080'
        self.diretorio_download = os.getcwd()
        self.arquivoParametros = os.getcwd() + "\\" + 'Parametros.txt'
        usuario, senha, dias = self.carrega_parametros(self.arquivoParametros)
        self.lista_de_tempo = []
        self.usuario = usuario
        self.senha = senha
        self.arquivos = ['romaneios', 'entregas', 'BASE ']
        self.lDataInicial = (datetime.now() - timedelta(days=dias)).strftime('%d-%m-%Y')
        self.lDataFinal = datetime.today().strftime('%d-%m-%Y')
        self.urlUXConsulta = 'http://vvlog.uxdelivery.com.br/Listas/listaconsulta'
        self.urlEntrega = 'http://vvlog.uxdelivery.com.br/Entregas/EntregaConsulta'
        self.nomeArquivoSaida = ['BASE VVLOG JDI.csv', 'BASE VVLOG TRANSFERENCIA.csv', 'BASE ROMANEIO.csv']

    def start(self):
        self.limpa_pasta(self.diretorio_download, self.arquivos)
        self.carrega_pagina_web()
        self.login()
        self.consulta_romaneio()
        self.aguarda_download(self.diretorio_download)
        self.nomeRomaneio = self.arquivo_atual(self.arquivos[0], self.diretorio_download)
        romaneios: list = self.filtra_romaneio(self.nomeRomaneio)
        self.listaRomaneiosStr = self.lista_romaneio(romaneios)
        self.navegacao_consulta(self.listaRomaneiosStr)
        self.aguarda_download(self.diretorio_download)
        self.navegacao_Jdi()
        self.aguarda_download(self.diretorio_download)
        self.renomear_arquivo(self.diretorio_download, self.arquivos, self.nomeArquivoSaida)

        time.sleep(1)
        self.driver.quit()
        logger.success('Consulta finalizada com sucesso.')

    def carrega_parametros(self, caminhoArquivo):
        logger.info('Verificando login e dias de extração.')
        try:
            plan = pd.read_table(caminhoArquivo, header=None, sep=":")  # latin-1
            usr = str(plan[1][0]).strip()
            senha = str(plan[1][1]).strip()
            dias = int(plan[1][2])
            logger.info(f'Usuário: {usr}\nExtração de: {dias} dias')
            return usr, senha, dias
        except:
            pass
            logger.warning('Não foi possivel ler o arquivo')

    def carrega_pagina_web(self) -> None:

        options = Options()
        # if not self.proxy == '':
        #     options.add_argument(f'--proxy-server={self.proxy}')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            "download.default_directory": self.diretorio_download,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("--start-maximized")
        logger.info('Iniciando Browser')
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 2)
            self.wait2 = WebDriverWait(self.driver, 120)
            # self.driver.get(self.urlUx)
            self.driver.get(self.urlUXConsulta)
        except:
            logger.critical('Não foi possivel abrir a pagina web.')
            time.sleep(4)

    def login(self) -> None:
        logger.info('Realizando login')
        lLogin: str = "//input[@id='login']"
        lSenha: str = "//input[@id='senha']"
        lEntrar: str = '//button[@type="submit"]'
        lAlerta: str = '//div[@class="alert alert-error"]'
        lCampoVazio: str = '//span[@class="field-validation-error"]'
        lTitulo: str = '/html/body/div[2]/div/section[1]/h1'
        try:
            login = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lLogin)))
            login.send_keys(self.usuario)
        except:
            pass
            logger.critical('Campo login não encontrado.')

        try:
            senha = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSenha)))
            senha.send_keys(self.senha)
        except:
            pass
            logger.critical('Campo senha não encontrado.')

        try:
            bt_entrar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lEntrar)))
            bt_entrar.click()
        except:
            pass
            logger.critical('Botão entrar não encontrado.')

        time.sleep(5)
        if self.valida_elemento(By.XPATH, lAlerta):
            tipo_erro = self.wait.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lAlerta))).text
            logger.warning('Login não efetuado')
            alert(tipo_erro, "Erro de Login")
            self.driver.quit()
        elif self.valida_elemento(By.XPATH, lCampoVazio):
            erro_campo = self.wait.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lCampoVazio)))
            str_erro: str = ''
            for erro in erro_campo:
                str_erro + erro.text + '\n'

            logger.warning('Campos Vazios')
            alert(str_erro, "Campos Vazios")
            self.driver.quit()

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

    def consulta_romaneio(self) -> None:  # , listaRomaneios: list
        lSelecionaCancelado: str = '//*[@id="flagCancelado"]'
        lSelecionaSaida: str = '//select[@id="tipoSaida"]'
        lSelecionaTipo: str = '//select[@id="idTipoLista"]'
        lSelecionaDataInicial = '//*[@id="dtListaIni"]'
        lSelecionaDataFinal = '//*[@id="dtListaFim"]'
        lBuscar: str = '//*[@id="formFiltros"]/div[2]/div[2]/div/div[2]/div[4]/div/div/div/button'
        lBarraProgress: str = '//*[@id="barraProgressoExcel"]/div'
        lDownload: str = '//*[@id="btDownload"]'

        try:
            selecaoCancelado = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaCancelado)))
            selecao_object = Select(selecaoCancelado)
            selecao_object.select_by_value('False')
        except:
            pass
            logger.warning('elemento selecaoCancelado não encontrado.')
        try:
            selecaoTipo = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaTipo)))
            selecao_object = Select(selecaoTipo)
            selecao_object.select_by_value('5')
        except:
            pass
            logger.warning('elemento selecaoTipo não encontrado.')

        try:
            selecaoDataFinal = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaDataFinal)))
            selecaoDataFinal.click()
            selecaoDataFinal.send_keys(self.lDataFinal)
        except:
            pass
            logger.warning('Elemento selecaoDataFinal não encontrado.')

        try:
            selecaoDataInicial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaDataInicial)))
            selecaoDataInicial.click()
            selecaoDataInicial.send_keys(self.lDataInicial)
        except:
            pass
            logger.warning('Elemento selecaoDataInicial não encontrado.')

        try:
            selecionar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, '//*[@id="valorBusca"]')))
            selecionar.click()
        except:
            pass
            logger.warning('Elemento selecionar não encontrado.')

        try:
            selecaoSaida = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSaida)))
            selecaoSaida_object = Select(selecaoSaida)
            selecaoSaida_object.select_by_value('excel')
        except:
            pass
            logger.warning('Elemento selecaoSaida não encontrado.')

        try:
            bt_buscar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBuscar)))
            bt_buscar.click()
        except:
            pass
            logger.warning('Elemento bt_buscar não encontrado.')

        self.barra_progresso(lBarraProgress, lDownload)

    def navegacao_consulta(self, romaneiosStr) -> None:
        lTitulo: str = '/html/body/div[2]/div/section[1]/h1'
        lTipo: str = '//*[@id="tipoBusca"]'
        lTxtArea: str = '//*[@id="valorBusca"]'
        lSelecionaSaida: str = '//*[@id="tipoSaida"]'
        lBuscar: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[15]/input[2]'
        lBarraProgress: str = '//*[@id="barraProgressoExcel"]/div'
        lDownload: str = '//*[@id="btDownload"]'

        self.driver.get(self.urlEntrega)

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

        try:
            selecaoTipo = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTipo)))
            selecao_object = Select(selecaoTipo)
            selecao_object.select_by_value('nro_lista')
        except:
            pass
            logger.warning('elemento selecaoTipo não encontrado.')

        try:
            pc.copy(romaneiosStr)
            textArea = self.wait2.until(condicaoEsperada.presence_of_element_located((By.XPATH, lTxtArea)))
            textArea.send_keys(Keys.CONTROL, 'v')
        except:
            pass
            logger.warning('Elemento textArea não encontrado.')

        try:
            selecaoSaida = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSaida)))
            selecaoSaida_object = Select(selecaoSaida)
            selecaoSaida_object.select_by_value('excel')
        except:
            pass
            logger.warning('Elemento selecaoSaida não encontrado.')

        try:
            bt_buscar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBuscar)))
            bt_buscar.click()
        except:
            pass
            logger.warning('Elemento bt_buscar não encontrado.')

        self.barra_progresso(lBarraProgress, lDownload)

    def navegacao_Jdi(self) -> None:
        lTitulo: str = '/html/body/div[2]/div/section[1]/h1'
        lBotaoFilial: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[2]/div[1]/button'
        lfiltroFilial: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[2]/div[1]/ul/div/input'
        lSelecionaTodos: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/a/label'
        lSelecionaDataInicial = '//*[@id="dtIniSolicitacao"]'
        lSelecionaDataFinal = '//*[@id="dtFimSolicitacao"]'
        lSelecionaSaida: str = '//*[@id="tipoSaida"]'
        lSelecionaArea: str = '//*[@id="valorBusca"]'
        lBuscar: str = '/html/body/div[2]/div/section[2]/div[3]/div[2]/form/div[2]/div[2]/div/div[15]/input[2]'
        lBarraProgress: str = '//*[@id="barraProgressoExcel"]/div'
        lDownload: str = '//*[@id="btDownload"]'

        self.driver.get(self.urlEntrega)

        try:
            self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lTitulo)))
        except TimeoutException as e:
            logger.warning('Tempo de Login atingido.\nVerifique sua conexão e tente novamente.')
            alert(
                'Tempo de Login atingido.\nVerifique sua conexão e tente novamente.', "Tempo de Login")
            self.driver.quit()

        time.sleep(2)

        try:
            selecaoDataFinal = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaDataFinal)))
            selecaoDataFinal.click()
            selecaoDataFinal.send_keys(self.lDataFinal)
        except:
            pass
            logger.warning('Elemento selecaoDataFinal não encontrado.')

        try:
            selecaoDataInicial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaDataInicial)))
            selecaoDataInicial.click()
            selecaoDataInicial.send_keys(self.lDataInicial)
        except:
            pass
            logger.warning('Elemento selecaoDataInicial não encontrado.')

        try:
            selecionaArea = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaArea)))
            selecionaArea.click()
        except:
            pass
            logger.warning('Elemento area não encontrado.')

        try:
            bt_filial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBotaoFilial)))
            bt_filial.click()
        except:
            pass
            logger.warning('Elemento bt_filial não encontrado.')

        try:
            selecaoFilial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lfiltroFilial)))
            selecaoFilial.send_keys('2200')
            selecaoFilial.send_keys(Keys.ENTER)
        except:
            pass
            logger.warning('Elemento selecaoFilial não encontrado.')

        try:
            selecaoTodos = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaTodos)))
            selecaoTodos.click()
        except:
            pass
            logger.warning('Elemento selecaoTodos não encontrado.')

        try:
            bt_filial = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBotaoFilial)))
            bt_filial.click()
        except:
            pass
            logger.warning('Elemento bt_filial não encontrado.')

        try:
            selecaoSaida = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lSelecionaSaida)))
            selecaoSaida_object = Select(selecaoSaida)
            selecaoSaida.click()
            selecaoSaida_object.select_by_value('excel')
        except:
            pass
            logger.warning('Elemento selecaoSaida não encontrado.')

        try:
            bt_buscar = self.wait2.until(
                condicaoEsperada.presence_of_element_located((By.XPATH, lBuscar)))
            bt_buscar.click()
        except:
            pass
            logger.warning('Elemento bt_buscar não encontrado.')

        self.barra_progresso(lBarraProgress, lDownload)

    def lista_romaneio(self, listaRomaneios) -> str:
        romaneiosStr: str = ''
        if len(listaRomaneios) > 0:
            logger.debug(f'Quantidade Consultas: {len(listaRomaneios)} romaneios')
            for idx, romaneios in enumerate(listaRomaneios):
                romaneiosStr += str(romaneios) + '\n'
        return romaneiosStr

    def filtra_romaneio(self, caminhoArquivo):
        logger.info('Extraindo romaneios do data frame')
        df = pd.DataFrame()
        lista_romaneio = []

        try:
            plan = pd.read_csv(caminhoArquivo, sep=';', encoding='latin-1')  # latin-1
            # df = pd.concat(plan, ignore_index=True)
            # df = df.append(plan, ignore_index=True)
            lista_romaneio = plan['Nro. Romaneio'].to_list()
            # print(lista_romaneio)
        except:
            pass
            logger.warning('Não foi possivel ler o arquivo')

        return lista_romaneio

    def arquivo_atual(self, nomeArquivo, diretorio, indice: int = 1):
        l_arquivos = os.listdir(diretorio)
        l_datas = []
        time.sleep(2)
        
        for arquivo in l_arquivos:
            if nomeArquivo in arquivo:
                data = os.path.getmtime(os.path.join(os.path.realpath(diretorio), arquivo))
                l_datas.append((data, arquivo))

        try:
            l_datas.sort(reverse=True)
            # for i in l_datas:
            #     print(i)
            ult_arquivo = l_datas[0]
            nome_arquivo = ult_arquivo[1]
            data_arquivo = ult_arquivo[0]
            arq = os.path.join(os.path.realpath(diretorio), nome_arquivo)
            data_mod = self.data_modificacao(arq)
            # return nome_arquivo, data_arquivo
            caminhoArquivo = os.getcwd() + '\\' + nome_arquivo
            return caminhoArquivo
        except:
            return 'Nenhum arquivo Localizado.'

    def data_modificacao(self, arquivo):

        ti_m = os.path.getmtime(arquivo)

        m_ti = time.ctime(ti_m)
        t_obj = time.strptime(m_ti)
        T_stamp = time.strftime("%d/%m/%Y %H:%M:%S", t_obj)

        logger.info(f"Ultima atualização dop arquivo em {T_stamp}")
        return T_stamp

    def aguarda_download(self, caminho):
        fileends = "crdownload"
        logger.info('Downloading em andamento, aguarde...')
        while "crdownload" == fileends:
            time.sleep(2)
            newest_file = self.arquivo_recente(caminho)
            if "crdownload" in newest_file:
                fileends = "crdownload"
            else:
                fileends = "none"
                logger.info('Downloading Completo...')

    def arquivo_recente(self, caminho):
        path = caminho
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]
        return newest

    def valida_elemento(self, tipo, path) -> bool:
        try:
            self.driver.find_element(by=tipo, value=path)
        except NoSuchElementException as e:
            return False
        return True

    def barra_progresso(self, lBarraProgress, lDownload):
        logger.info('Aguardando barra de progresso')
        time.sleep(3)
        if self.valida_elemento(By.XPATH, lBarraProgress):
            pa = 0
            while True:
                percentual = self.wait2.until(
                    condicaoEsperada.presence_of_element_located((By.XPATH, lBarraProgress))).text
                try:
                    p = int(percentual.replace("%", ""))
                except:
                    p = 0

                if p % 10 == 0 and p != "" and p != pa:
                    logger.debug(f'{percentual}')
                    pa = p
                if percentual == '100%':
                    logger.debug(f'Carregamento {percentual} Concluido.')
                    time.sleep(2)
                    try:
                        download_arquivo = self.wait2.until(
                            condicaoEsperada.presence_of_element_located((By.XPATH, lDownload)))
                        download_arquivo.click()
                        logger.info('Aguardando Download')
                        time.sleep(2)
                    except:
                        pass
                        logger.warning('Elemento download_arquivo não encontrado.')
                    break

    def limpa_pasta(self, caminho, nomeArquivo):
        logger.warning('Limpando pasta...')
        for f in os.listdir(caminho):
            if nomeArquivo[0] in f or nomeArquivo[1] in f or nomeArquivo[2] in f or '.tmp' in f:
                os.remove(os.path.join(caminho, f))

    def renomear_arquivo(self, diretorio, nomesOrigem, nomesDestino):
        logger.info('Renomeando arquivos baixados.')
        l_arquivos = os.listdir(diretorio)
        l_datas = []
        l_nomesOrigem = nomesOrigem
        l_nomesDestino = nomesDestino

        for arquivo in l_arquivos:
            if l_nomesOrigem[0] in arquivo or l_nomesOrigem[1] in arquivo:
                data = os.path.getmtime(os.path.join(os.path.realpath(diretorio), arquivo))
                l_datas.append((data, arquivo))

        if len(l_datas) >= 3:
            try:
                l_datas.sort(reverse=True)
                # for i in l_datas:
                #     print(i)
                for r in range(3):
                    ult_arquivo = l_datas[r - 1]
                    nome_arquivo = ult_arquivo[1]
                    caminhoOrigem = os.getcwd() + '\\' + nome_arquivo
                    caminhoDestino = os.getcwd() + '\\' + l_nomesDestino[r - 1]
                    os.rename(caminhoOrigem, caminhoDestino)
            except:
                return 'Nenhum arquivo Localizado.'
        else:
            logger.warning('Não foi baixados todos os arquivos necessários.')


if __name__ == '__main__':
    executa = Vvlog_UX()
    executa.start()