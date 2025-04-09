import tkinter as tk
from interface import Interface
from database import init_db
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Aplicação iniciada.')
if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    root = tk.Tk()
    
    # Centraliza a janela na tela com tamanho original
    largura = 1200
    altura = 800
    tela_largura = root.winfo_screenwidth()
    tela_altura = root.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')
    root.minsize(600, 400)  # Tamanho mínimo para garantir visibilidade
    
    app = Interface(root)
    root.mainloop()
    #tdwu ptnu tjhd afrt