"""
Módulo de Instancia do Navegador. 

Este módilo contém o código dedicado a reescrever algumas funções padrões do Selenium, para uma melhor leitura e manutenção dos códigos adjacentes.

O intuito dele é facilitar a legibilidade do código para futuras manutenções.

"""

# Importações do Python
import os
from time import sleep
from random import randint
from functools import partial
from typing import Dict
from typing import List

# Importações de Bibliotecas Externas
from selenium import webdriver
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Importações Internas
from utilitarios.funcoes_globais import GeneralFuncs

class Navegador(webdriver.Chrome):
    """
    Classe base para realizar as automações na Web.

    :param somente_terminal: Iniciar navegação sem exibir o navegador (bool).
    :type somente_terminal: bool
    :param salvar_cache: Caminho do arquivo de cache (str). 
    :type salvar_cache: str
    :param tela_cheia: Iniciar em tela cheia.
    :type tela_cheia: bool
    :param logs: Caminho para salvar o arquivo de Logs (str).
    :type logs: str
    :param agentes: Agentes do Usuário (UserAgent) (bool).
    :type agentes: bool
    :param incognite: Navegação em aba anônima (bool).
    :type incognite: bool
    """
    
    def __init__(self, 
        somente_terminal=False,
        salvar_cache="",
        tela_cheia=True,
        logs="",
        agentes=False, 
        incognite=False):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-block')
        chrome_options.add_argument("no-default-browser-check")

        if somente_terminal == True:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--mute-audio")
        
        if salvar_cache != "":
            if os.path.exists(salvar_cache) == False:
                  os.makedirs(salvar_cache)
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--user-data-dir=" + salvar_cache)
        
        if tela_cheia == True:
            chrome_options.add_argument('--start-maximized')
        
        if logs != "":
            ...
        
        if agentes == True:
            age = [ 
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" ,
		    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
		    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63",
		    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0",
		    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
		    ]
            agente = age[randint(0, len(age) - 1)]
            chrome_options.add_argument("user-agent=" + agente)

        if incognite == True:
            chrome_options.add_argument("--incognito")
        
        servico = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(chrome_options, servico)
        self.action = ActionChains(self.driver)

    def navegar(self, url):
        """Navega para uma página da web."""
        return self.driver.get(url)

    def avancar(self):
        """Avança par aa navegação a frente."""
        return self.driver.forward(self)
    
    def voltar(self):
        """Volta a sessão anterior de navegação."""
        return self.driver.back(self)

    def abrir_nova_janela(self):
        """Abre uma nova aba no navegador."""
        return self.driver.switch_to.new_window()

    def atualizar(self):
        return self.driver.refresh()

    def fechar_janela(self):
        """fecha a janela."""
        return self.driver.close()
    
    def encerrar_navegador(self):
        """Encerra a sessão do navegador."""
        return self.driver.quit()

    def url_atual(self):
        """Retorna a URL atual."""
        return self.driver.current_url
    
    def id_janela_atual(self):
        """Retorna o número do identificador da janela atual."""
        return self.driver.current_window_handle
    
    def deletar_cookies(self, todos=False):
        """
        Deleta os cookies da sessão de navegação.
        :param todos: Deletar todos os cookies (bool).
        :type todos: bool
        """
        if todos:
            return self.driver.delete_all_cookies()
        else:
            return self.driver.delete_cookie()

    def executar_script(self, script=str, assincrono=True, *args):
        """
        Executa um Script do JavaScript.
        :param script: Script a ser executado (str).
        :type script: str
        :param assincrono: Executar o script de forma Assíncrona (bool).
        :type assincrono: bool
        :param *args: Quaisquer argumentos aplicáveis ao Script.
        :type *args: *args
        """
        if assincrono:
            return self.driver.execute_async_script(script, args)
        else:
            return self.driver.execute_script(script, args)
    
    def executar_devtools_cmd(self, cmd=str, cmd_args=dict):
        """
        Execute o comando do protocolo Chrome Devtools 
        e obtenha o resultado retornado.
        consulte: https://chromedevtools.github.io/devtools-protocol/
        """
        return self.driver.execute_cdp_cmd(cmd, cmd_args)
    
    def obter_elemento(self, tipo='ID', valor=str):
        """
        Encontre um elemento passando um Seletor e um Localizador.
        
        :param tipo: Tipo do Seletor (str).
        :type tipo: str
        :param valor: Valor do Localizador (str)
        :type valor: str
        :return: Elemento da Web (WebElement).
        """
        if tipo.upper() == 'ID':
            seletor = By.ID
        elif tipo.upper() == 'XPATH':
            seletor = By.XPATH
        elif tipo.upper() == 'LINK_TEXT':
            seletor = By.LINK_TEXT
        elif tipo.upper() == 'PARTIAL_LINK_TEXT':
            seletor = By.PARTIAL_LINK_TEXT
        elif tipo.upper() == 'NAME':
            seletor = By.NAME
        elif tipo.upper() == 'TAG_NAME':
            seletor = By.TAG_NAME
        elif tipo.upper() == 'CLASS_NAME':
            seletor = By.CLASS_NAME
        elif tipo.upper() == 'CSS_SELECTOR':
            seletor = By.CSS_SELECTOR

        elemento = self.driver.find_element(seletor, valor)
        return elemento
 
    def obter_elementos(self, tipo='ID', valor=str):
        """
        Encontre mais de um elemento passando um Seletor e um Localizador.
        
        :param tipo: Tipo do Seletor (str).
        :type tipo: str
        :param valor: Valor do Localizador (str).
        :type valor: str
        :return: Lista de Elementos Web.
        """
        if tipo.upper() == 'ID':
            seletor = By.ID
        elif tipo.upper() == 'XPATH':
            seletor = By.XPATH
        elif tipo.upper() == 'LINK_TEXT':
            seletor = By.LINK_TEXT
        elif tipo.upper() == 'PARTIAL_LINK_TEXT':
            seletor = By.PARTIAL_LINK_TEXT
        elif tipo.upper() == 'NAME':
            seletor = By.NAME
        elif tipo.upper() == 'TAG_NAME':
            seletor = By.TAG_NAME
        elif tipo.upper() == 'CLASS_NAME':
            seletor = By.CLASS_NAME
        elif tipo.upper() == 'CSS_SELECTOR':
            seletor = By.CSS_SELECTOR

        return self.driver.find_elements(seletor, valor)
    
    def esperar(self, 
                tipo='ID',
                valor=str,
                tempo_limite=10, 
                elemento_ativo=False, 
                elemento_visivel=False, 
                elemento_selecionado=False
                ):
        """
        Espera o Elemento estar disponível no HTML da página.
        
        :param tipo: Tipo do Seletor (str).
        :type tipo: str
        :param valor: Valor do Localizador (str).
        :type valor: str
        :param tempo_limite: Tempo de espera máximo (int).
        :type tempo_limite: int
        :param elemento_ativo: Espera o elemento estar ativo (bool).
        :type elemento_ativo: bool
        :param elemento_visivel: Espera o elemento estar visível (bool).
        :type elemento_visível: bool
        :param elemento_selecionado: Espera o elemento estar selecionado (bool).
        :type elemento_selecionado: bool
        """
        def espera(by, element, webdriver):
            return bool(webdriver.find_elements(by, element))
        
        if tipo.upper() == 'ID':
            seletor = By.ID
        elif tipo.upper() == 'XPATH':
            seletor = By.XPATH
        elif tipo.upper() == 'LINK_TEXT':
            seletor = By.LINK_TEXT
        elif tipo.upper() == 'PARTIAL_LINK_TEXT':
            seletor = By.PARTIAL_LINK_TEXT
        elif tipo.upper() == 'NAME':
            seletor = By.NAME
        elif tipo.upper() == 'TAG_NAME':
            seletor = By.TAG_NAME
        elif tipo.upper() == 'CLASS_NAME':
            seletor = By.CLASS_NAME
        elif tipo.upper() == 'CSS_SELECTOR':
            seletor = By.CSS_SELECTOR

        saida = 0
        espera_webdriver = WebDriverWait(self.driver, tempo_limite)
        espera_webdriver.until(partial(espera, seletor, valor))

        if elemento_ativo:
            while not self.driver.find_element(seletor, valor).is_enabled():
                sleep(0.5)
                if saida == tempo_limite * 2:
                    return False
                saida += 1
            return True
        elif elemento_visivel:
            while not self.driver.find_element(seletor, valor).is_displayed():
                sleep(0.5)
                if saida == tempo_limite * 2:
                    return False
                saida += 1
            return True
        elif elemento_selecionado:
            while not self.driver.find_element(seletor, valor).is_selected():
                sleep(0.5)
                if saida == tempo_limite * 2:
                    return False
                saida += 1
            return True
    
    def espera_aleatoria(self, valor_inicial=1, valor_final=3):
        """
        Espera um tempo aleatório (em segundos).
        
        :param valor_inicial: O primeiro valor da aleatoriedade (int).
        :type valor_inicial: int
        :param valor_final: O último valor da aleatoriedade (int).
        :type valor_final: int
        """
        return sleep(randint(valor_inicial, valor_final))
    
    def obter_tamanho_tela(self, id_janela):
        """
        Retorna a largura e a altura da janela (Padrão: atual).

        :param id_janela: Nome ou ID da Window.
        """
        return self.driver.get_window_size(id_janela)

    def minimizar_janela(self):
        """Minimixa o navegador."""
        return self.driver.minimize_window()
    
    def maximizar_janela(self):
        """Coloca o navegador em tela cheia."""
        return self.driver.maximize_window()

    def captura_de_tela(self, arquivo=str):
        """
        Salva uma captura de tela da janela atual em um arquivo de imagem PNG. 

        :Args:
         - arquivo: o caminho completo no qual você deseja salvar sua captura de tela. Isso deve terminar com uma extensão .png.
        """
        return self.driver.get_screenshot_as_file(arquivo)

    def salvar_janela_pdf(self):
        """Salva a página web, no formato PDF.

        O driver faz o possível para retornar um PDF com base nos parâmetros fornecidos.
        """
        return self.driver.print_page()

    def definir_tamanho_posicao_janela(self, x, y, largura, altura, janela="atual"):
        """Define a posição ou o tamanho da tela a partir dos parâmetro informados.

            - x e y: Define a posição x, y da janela atual.
            - largura e altura: Define a largura e a altura da janela atual.
            - x, y, largura e altura: Define as coordenadas x, y da janela, bem como a altura e largura da janela atual.
        """
        if janela == "atual":
            janela = "current"
        if x != None and y != None and largura != None and altura != None:
            return self.driver.set_window_rect(x, y, largura, altura)
        elif x != None and y != None:
            return self.driver.set_window_position(x, y, janela)
        elif largura != None and altura != None:
            return self.driver.set_window_size(largura, altura, janela)
    
    def mudar_foco(self, id_frame=False, janela_padrao=False, alerta=False):
        """
        Muda o foco do navegador para algum objeto específico.
        
        :param id_frame: Recebe o Identificados do iframe (str).
        :type id_frame: str
        :param janela_padrao: Se quer mudar para a janela padrão (bool).
        :type janela_padrao: bool
        :param alerta: Se quiser mudar o foco para um alert (bool).
        :type alerta: bool
        """
        if janela_padrao:
            return self.driver.switch_to.default_content()
        elif alerta:
            return self.driver.switch_to.alert
        elif id_frame:
            return self.driver.switch_to.frame(id_frame)
        else:
            return self.driver.switch_to

    def mudar_janela(self, id_janela):
        """
        Muda o foco do navegador para alguma janela.

        :param id_janela: Pode receber o identificador da janela ou o nome dela.
        """
        return self.driver.switch_to.window(id_janela)

    def obter_cookie(self, nome):
        """
        Obtenha um único cookie por nome. 
        
        Retorna o cookie se encontrado, None se não for encontrado."""
        return self.driver.get_cookie(nome)

    def obter_cookies(self):
        """Retorna um conjunto de dicionários, correspondentes aos cookies visíveis na sessão atual."""
        return self.driver.get_cookies()
    
    def obter_logs(self, tipo_de_log):
        """
        Obtém o log de um determinado tipo de log.
        
        :param tipo_de_log: 
            - browser: Logs do Navegador
            - driver: Logs do Driver
        """
        if tipo_de_log == "browser":
            self.driver.get_log("browser")
        elif tipo_de_log == "driver":
            self.driver.get_log("driver")
        
    def obter_titulo_janela(self):
        """Retorna o titulo da janela atual."""
        return self.driver.title
    
    def clicar_elemento(
            self, 
            elemento, 
            duplo=False, 
            botao_direito=False, 
            pressionado=False
            ):
        """
        Clica no elemento.

        :param elemento: O elemento a ser clicado (WebElement).
        :type elemento: WebElement
        :param duplo: Clique duplo (bool).
        :type duplo: bool
        :param botao_direito: Executa o clique com o botão direito no elemento (bool).
        :type botao_direito: bool
        :param pressionado: Mantém pressionado o botão esquerdo do mouse em um elemento (bool).
        :type: bool
        """
        if duplo:
            self.action.double_click(elemento)
        elif botao_direito:
            self.action.context_click(elemento)
        elif pressionado:
            self.action.click_and_hold(elemento)
        else:
            self.action.click(elemento)
        self.action.perform()
    
    def mover_para_elemento(self, elemento):
        """Move o cursor do mouse para o meio do elemento."""
        return self.action.move_to_element(elemento).perform()

    def mover_cursor(self, x, y):
        """
        Move o cursor do mouse para uma coordenada específica

        Recebe o valor das coordenadas de x, y como parâmetros.
        """
        return self.action.move_by_offset(x, y).perform()

    def rolar_para_elemento(self, elemento):
        """
        Se o elemento estiver ora da visualização na Janela atual, role até a parte inferior do elemento.
        
        :param elemento: Rola até o elemento (WebElement)
        """
        return self.action.scroll_to_element(elemento).perform()

    def rolar_por_cordenada(self, x, y):
        """Role para os valores fornecidos com a origem no canto superior esquerdo da janela de visualização."""
        return self.action.scroll_by_amount(x, y).perform()

    def enviar_teclas(self, *teclas_a_enviar, espera_entre_as_teclas=0.1):
        """
        Envia chaves para o elemento atual em foco.
        
        :param teclas_a_enviar: As chaves a serem enviadas. As constantes das teclas modificadoras podem ser encontradas na classe 'Keys'.
        :param espera_entre_as_teclas: O tempo de espera entre cada teclada.
        """
        for i in teclas_a_enviar:
            self.action.send_keys(i).perform()
            sleep(espera_entre_as_teclas)
        return True

    def __del__(self):
        """Método de encerramento do Navegador."""
        print('\033[31mEncerrando..\033[0m')
        self.driver.quit()