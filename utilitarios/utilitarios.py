"""
Este módulo é voltado para guardar os valores dos elementos que serão usados nas automações Web.

O objetivo deste código é simplificar a legibilidade do código, visto que muitos elementos tem XPATHs etensos, dificultando a leitura.
"""
import os

CREDENCIAIS = {
    'usuario_twitter': 'SEU_EMAIL_AQUI', # <- COLOQUE SEU E-MAIL DO FACEBOOK AQUI
    'senha_twitter': 'SUA_SENHA_AQUI' # <- COLOQUE SUA SENHA DO FACEBOOK AQUI
}

LINKS = {
    'base_twitter': 'https://twitter.com/',
    'login_twitter': 'https://twitter.com/login',
    'baixar_video': 'https://ssstwitter.com/'
}

PATH = {
    'arquivo_cache': os.getcwd() + '\cache',
    'saida': os.getcwd() + '\\resultados',
    }

XPATHS = {
    'posts': '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div/article',
    'texto': './div/div/div[2]/div[2]/div[2]/div',
    'link_data':  ".//a[contains(@href, '/status') and @role='link' and @dir='ltr']",
    'videos_download': '//*[@id="mainpicture"]/div',
    'fixado': './div/div/div[1]/div/div/div/div/div[2]/div/div/div/span',
    'login': '//a[@href="/login"]',
    'input_login': '//input[@name="text"]',
    'input_password': '//input[@name="password"]',
    'confirmar_usuario': '//span[text()="Digite seu número de celular ou nome de usuário"]',
}
