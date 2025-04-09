import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from styles import Styles
from datetime import datetime

class ListaCompras:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=Styles.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.init_lista_compras()

    def init_lista_compras(self):
        content_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=Styles.PADY)

        tk.Label(content_frame, text='Lista de Compras', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)

        # Frame da esquerda (Produtos Cadastrados)
        left_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Styles.PADX)

        tk.Label(left_frame, text='Produtos Cadastrados', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)

        # Campo de pesquisa para Produtos Cadastrados
        search_frame = tk.Frame(left_frame, bg=Styles.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, Styles.PADY))
        tk.Label(search_frame, text='Pesquisar Produtos:', font=Styles.FONT, bg=Styles.BG_COLOR).pack(side=tk.LEFT, padx=Styles.PADX)
        self.search_entry_produtos = tk.Entry(search_frame, font=Styles.FONT)
        self.search_entry_produtos.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.produtos_tree = ttk.Treeview(left_frame, columns=('Código Produto', 'Descrição'), show='headings', height=10)
        self.produtos_tree.heading('Código Produto', text='Código Produto')
        self.produtos_tree.heading('Descrição', text='Descrição')
        self.produtos_tree.column('Código Produto', width=100)
        self.produtos_tree.column('Descrição', width=150)
        
        scrollbar_produtos = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.produtos_tree.yview)
        self.produtos_tree.configure(yscrollcommand=scrollbar_produtos.set)
        self.produtos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_produtos.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista para armazenar todos os produtos (para pesquisa)
        self.produtos_lista = []

        # Vincular a pesquisa ao campo de entrada
        self.search_entry_produtos.bind('<KeyRelease>', lambda event: self.filtrar_produtos())

        # Frame do meio (Botões de Adicionar/Remover)
        middle_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        middle_frame.pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(middle_frame, text='Adicionar ->', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.adicionar_item(self.produtos_tree, self.itens_tree)).pack(pady=Styles.PADY)
        tk.Button(middle_frame, text='<- Remover', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.remover_item(self.itens_tree)).pack(pady=Styles.PADY)

        # Frame da direita (Itens da Lista)
        right_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Styles.PADX)

        tk.Label(right_frame, text='Itens da Lista', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        self.itens_tree = ttk.Treeview(right_frame, columns=('Código Produto', 'Descrição', 'Quantidade'), show='headings', height=10)
        self.itens_tree.heading('Código Produto', text='Código Produto')
        self.itens_tree.heading('Descrição', text='Descrição')
        self.itens_tree.heading('Quantidade', text='Quantidade')
        self.itens_tree.column('Código Produto', width=100)
        self.itens_tree.column('Descrição', width=150)
        self.itens_tree.column('Quantidade', width=50)
        
        scrollbar_itens = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.itens_tree.yview)
        self.itens_tree.configure(yscrollcommand=scrollbar_itens.set)
        self.itens_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_itens.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame inferior (Botão Salvar)
        bottom_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        bottom_frame.pack(fill=tk.X, pady=Styles.PADY)

        # Subframe para organizar o botão verticalmente
        input_frame = tk.Frame(bottom_frame, bg=Styles.BG_COLOR)
        input_frame.pack(pady=Styles.PADY)

        tk.Button(input_frame, text='Salvar Lista', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.salvar_lista).pack()

    def load_data(self):
        self.carregar_produtos()

    def carregar_produtos(self):
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        self.produtos_lista.clear()  # Limpar a lista de produtos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT codigo_produto, descricao FROM produtos')
        for row in cursor.fetchall():
            self.produtos_lista.append(row)
            self.produtos_tree.insert('', tk.END, values=row)
        conn.close()

    def filtrar_produtos(self):
        termo = self.search_entry_produtos.get().lower()
        # Limpar a tabela
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        # Filtrar e exibir os produtos
        for valores in self.produtos_lista:
            if termo in valores[0].lower() or termo in valores[1].lower():
                self.produtos_tree.insert('', tk.END, values=valores)

    def adicionar_item(self, produtos_tree, itens_tree):
        selected = produtos_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um produto para adicionar!')
            return
        valores = produtos_tree.item(selected[0], 'values')
        itens_tree.insert('', tk.END, values=(valores[0], valores[1], 1))

    def remover_item(self, itens_tree):
        selected = itens_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um item para remover!')
            return
        itens_tree.delete(selected[0])

    def salvar_lista(self):
        itens = self.itens_tree.get_children()
        if not itens:
            messagebox.showwarning('Atenção', 'Adicione pelo menos um item à lista!')
            return

        # Gerar o nome da lista no formato lista_dd_mm_aaaa
        data_atual = datetime.now()
        nome_lista = f'{data_atual.strftime("%d_%m_%Y")}'
        data_criacao = data_atual.strftime('%d/%m/%Y %H:%M:%S')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO listas (nome, data_criacao) VALUES (?, ?)', (nome_lista, data_criacao))
        lista_id = cursor.lastrowid

        for item in self.itens_tree.get_children():
            valores = self.itens_tree.item(item, 'values')
            cursor.execute('SELECT id FROM produtos WHERE codigo_produto = ?', (valores[0],))
            produto_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO itens_lista (lista_id, produto_id, quantidade) VALUES (?, ?, ?)',
                           (lista_id, produto_id, valores[2]))

        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Lista salva com sucesso!')
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        self.search_entry_produtos.delete(0, tk.END)
        self.filtrar_produtos()  # Atualizar a tabela de produtos após limpar a pesquisa