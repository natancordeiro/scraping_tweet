"""
Este módulo armazena a chamada principal da automação. 
"""

# Importação
from engine.automacao import Automacao
import os, time

banner = """\033[34m
   ____                  _             ______       _ __  __                
  / __/__________ ____  (_)__  ___ _  /_  __/    __(_) /_/ /__    _____ ____
 _\ \/ __/ __/ _ `/ _ \/ / _ \/ _ `/   / / | |/|/ / / __/ __/ |/|/ / -_) __/
/___/\__/_/  \_,_/ .__/_/_//_/\_, /   /_/  |__,__/_/\__/\__/|__,__/\__/_/   
                /_/          /___/                                          

\033[0m"""

def main():
    """Executa a função principal do código."""
    os.system('cls')
    print(banner)
    time.sleep(1)
    automacao = Automacao()
    automacao.raspar_Twitter()

if __name__ == "__main__":
    """Chama a função na inicialização do código."""
    main()
