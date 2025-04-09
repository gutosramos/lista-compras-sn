import tkinter as tk
from tkinter import ttk
from fornecedores import Fornecedores
from produtos import Produtos
from lista_compras import ListaCompras
from listas_salvas import ListasSalvas
from perfil import Perfil
from styles import Styles

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title('Gerenciamento de Listas de Compras')
        self.root.configure(bg=Styles.BG_COLOR)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=Styles.PADY)

        self.fornecedores_tab = tk.Frame(self.notebook, bg=Styles.BG_COLOR)
        self.produtos_tab = tk.Frame(self.notebook, bg=Styles.BG_COLOR)
        self.lista_compras_tab = tk.Frame(self.notebook, bg=Styles.BG_COLOR)
        self.listas_salvas_tab = tk.Frame(self.notebook, bg=Styles.BG_COLOR)
        self.perfil_tab = tk.Frame(self.notebook, bg=Styles.BG_COLOR)

        self.notebook.add(self.fornecedores_tab, text='Fornecedores')
        self.notebook.add(self.produtos_tab, text='Produtos')
        self.notebook.add(self.lista_compras_tab, text='Lista de Compras')
        self.notebook.add(self.listas_salvas_tab, text='Listas Salvas')
        self.notebook.add(self.perfil_tab, text='Perfil')

        self.fornecedores = Fornecedores(self.fornecedores_tab)
        self.produtos = Produtos(self.produtos_tab)
        self.lista_compras = ListaCompras(self.lista_compras_tab)
        self.listas_salvas = ListasSalvas(self.listas_salvas_tab)
        self.perfil = Perfil(self.perfil_tab)

        self.load_all_data()

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def load_all_data(self):
        self.fornecedores.load_data()
        self.produtos.load_data()
        self.lista_compras.load_data()
        self.listas_salvas.load_data()
        self.perfil.load_data()

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, 'text')
        if tab_text == 'Fornecedores':
            self.fornecedores.load_data()
        elif tab_text == 'Produtos':
            self.produtos.load_data()
        elif tab_text == 'Lista de Compras':
            self.lista_compras.load_data()
        elif tab_text == 'Listas Salvas':
            self.listas_salvas.load_data()
        elif tab_text == 'Perfil':
            self.perfil.load_data()