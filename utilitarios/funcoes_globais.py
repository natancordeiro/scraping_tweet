"""
Este Módulo tras algumas funções gerais, voltados para depuração do código, e gravação de Logs.
"""

# Importações do Python
import sys
import time
import builtins
from datetime import datetime

class GeneralFuncs:
    """
    Classe responsável por guardar algumas funções internas
    """
    
    def display_error() -> str:
        """ Mostrar mensagem de erro com detalhes """

        exctp, exc, exctb = sys.exc_info()
        print(
            f'\n\033[033mtraceback\033[0m:\033[031m{exc}\033[0m' +
            f'{exctb.tb_frame.f_code.co_name}:{exctb.tb_lineno}:{exctp}:'
        )

    def measure_time(func):
        """ Operador para calcular quanto tempo uma funcao leva para iniciar e terminar """

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            total_time = end_time - start_time
            hours, rem = divmod(total_time, 3600)
            minutes, seconds = divmod(rem, 60)

            if hours > 0:
                print(f"Function '{func.__name__}' took {int(hours)} hours, {int(minutes)} minutes, e {seconds:.2f} seconds to execute.")
            elif minutes > 0:
                print(f"Function '{func.__name__}' took {int(minutes)} minutes, e {seconds:.2f} seconds to execute.")
            else:
                print(f"Function '{func.__name__}' took {total_time:.2f} seconds to execute.")
            return result
        return wrapper
    
    def set_output():
        """ Printar datetime atual e funcao onde esta o print """
        
        original_print = builtins.print
        def costumized_output(*args, **kwargs):
            current_time = datetime.now().strftime("%H:%M:%S")
            frame = sys._getframe()
            output_msg = f'\033[95m[{current_time}]:\033[0m \033[94m{frame.f_back.f_code.co_name}:\033[0m'
            original_print(output_msg, *args, **kwargs)
        builtins.print = costumized_output