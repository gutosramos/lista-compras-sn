import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from styles import Styles

class Produtos:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=Styles.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Formulário de Cadastro
        form_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        form_frame.pack(fill=tk.X, pady=Styles.PADY)

        tk.Label(form_frame, text='Cadastrar Produto', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=0, column=0, columnspan=2, pady=Styles.PADY)

        tk.Label(form_frame, text='Código de Barras', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=1, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.codigo_barras = tk.Entry(form_frame, font=Styles.FONT)
        self.codigo_barras.grid(row=1, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.codigo_barras.insert(0, '')

        tk.Label(form_frame, text='Código Produto', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=2, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.codigo_produto = tk.Entry(form_frame, font=Styles.FONT)
        self.codigo_produto.grid(row=2, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.codigo_produto.insert(0, '')

        tk.Label(form_frame, text='Descrição', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=3, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.descricao = tk.Entry(form_frame, font=Styles.FONT)
        self.descricao.grid(row=3, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.descricao.insert(0, '')

        tk.Label(form_frame, text='Quantidade', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=4, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.quantidade = tk.Entry(form_frame, font=Styles.FONT)
        self.quantidade.grid(row=4, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.quantidade.insert(0, '')

        tk.Button(form_frame, text='Cadastrar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.cadastrar_produto).grid(row=5, column=0, pady=Styles.PADY)
        tk.Button(form_frame, text='Importar CSV', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.importar_csv).grid(row=5, column=1, pady=Styles.PADY)

        form_frame.columnconfigure(1, weight=1)

        # Tabela de Produtos com Scrollbar
        table_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=Styles.PADY)

        tk.Label(table_frame, text='Produtos Cadastrados', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        
        # Criar Treeview com Scrollbar
        self.tree = ttk.Treeview(table_frame, columns=('Código de Barras', 'Código Produto', 'Descrição', 'Quantidade'), show='headings', height=10)
        self.tree.heading('Código de Barras', text='Código de Barras')
        self.tree.heading('Código Produto', text='Código Produto')
        self.tree.heading('Descrição', text='Descrição')
        self.tree.heading('Quantidade', text='Quantidade')
        self.tree.column('Código de Barras', width=150)
        self.tree.column('Código Produto', width=100)
        self.tree.column('Descrição', width=200)
        self.tree.column('Quantidade', width=80)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botões de Ação
        action_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        action_frame.pack(fill=tk.X, pady=Styles.PADY)
        tk.Button(action_frame, text='Editar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.editar_produto).pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(action_frame, text='Excluir', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.excluir_produto).pack(side=tk.LEFT, padx=Styles.PADX)

    def load_data(self):
        self.carregar_produtos()

    def cadastrar_produto(self):
        codigo_barras = self.codigo_barras.get()
        codigo_produto = self.codigo_produto.get()
        descricao = self.descricao.get()
        quantidade = self.quantidade.get()

        if not all([codigo_barras, codigo_produto, descricao, quantidade]):
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showwarning('Atenção', 'Quantidade deve ser um número!')
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT codigo_barras FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
        if cursor.fetchone():
            messagebox.showwarning('Atenção', f'O código de barras {codigo_barras} já está cadastrado!')
            conn.close()
            return

        cursor.execute('INSERT INTO produtos (codigo_barras, codigo_produto, descricao, quantidade) VALUES (?, ?, ?, ?)', 
                       (codigo_barras, codigo_produto, descricao, quantidade))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Produto cadastrado com sucesso!')
        self.codigo_barras.delete(0, tk.END)
        self.codigo_produto.delete(0, tk.END)
        self.descricao.delete(0, tk.END)
        self.quantidade.delete(0, tk.END)
        self.carregar_produtos()

    def carregar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=(row[1], row[2], row[3], row[4]), tags=(row[0],))
        conn.close()

    def importar_csv(self):
        arquivo = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if not arquivo:
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        produtos_importados = 0
        codigos_duplicados = []

        try:
            with open(arquivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if not all(col in reader.fieldnames for col in ['codigo_barras', 'codigo_produto', 'descricao', 'quantidade']):
                    messagebox.showerror('Erro', 'O CSV deve conter as colunas: codigo_barras, codigo_produto, descricao, quantidade')
                    conn.close()
                    return

                for row in reader:
                    codigo_barras = row['codigo_barras'].strip()
                    codigo_produto = row['codigo_produto'].strip()
                    descricao = row['descricao'].strip()
                    quantidade = row['quantidade'].strip()

                    if not all([codigo_barras, codigo_produto, descricao, quantidade]):
                        codigos_duplicados.append(f'{codigo_barras} (campos incompletos)')
                        continue

                    try:
                        quantidade = int(quantidade)
                    except ValueError:
                        codigos_duplicados.append(f'{codigo_barras} (quantidade inválida)')
                        continue

                    cursor.execute('SELECT codigo_barras FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
                    if cursor.fetchone():
                        codigos_duplicados.append(codigo_barras)
                        continue

                    cursor.execute('INSERT INTO produtos (codigo_barras, codigo_produto, descricao, quantidade) VALUES (?, ?, ?, ?)',
                                   (codigo_barras, codigo_produto, descricao, quantidade))
                    produtos_importados += 1

            conn.commit()
            mensagem = f'{produtos_importados} produtos importados com sucesso!'
            if codigos_duplicados:
                mensagem += f'\nCódigos de barras duplicados ou inválidos ignorados: {", ".join(codigos_duplicados)}'
            messagebox.showinfo('Importação Concluída', mensagem)
        except Exception as e:
            conn.rollback()
            messagebox.showerror('Erro', f'Erro ao importar CSV: {str(e)}')
        finally:
            conn.close()
            self.carregar_produtos()

    def editar_produto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um produto para editar!')
            return
        item = self.tree.item(selected[0])
        produto_id = self.tree.item(selected[0], 'tags')[0]
        valores = item['values']

        popup = tk.Toplevel(self.parent)
        popup.title('Editar Produto')
        popup.configure(bg=Styles.BG_COLOR)
        popup.transient(self.parent)
        popup.grab_set()

        popup_width = 300
        popup_height = 250
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

        tk.Label(popup, text='Editar Produto', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        codigo_barras_edit = tk.Entry(popup, font=Styles.FONT)
        codigo_barras_edit.insert(0, valores[0])
        codigo_barras_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)
        codigo_produto_edit = tk.Entry(popup, font=Styles.FONT)
        codigo_produto_edit.insert(0, valores[1])
        codigo_produto_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)
        descricao_edit = tk.Entry(popup, font=Styles.FONT)
        descricao_edit.insert(0, valores[2])
        descricao_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)
        quantidade_edit = tk.Entry(popup, font=Styles.FONT)
        quantidade_edit.insert(0, valores[3])
        quantidade_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)

        tk.Button(popup, text='Salvar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.salvar_edicao_produto(produto_id, codigo_barras_edit.get(), codigo_produto_edit.get(), 
                                                             descricao_edit.get(), quantidade_edit.get(), popup)).pack(pady=Styles.PADY)

    def salvar_edicao_produto(self, produto_id, codigo_barras, codigo_produto, descricao, quantidade, popup):
        if not all([codigo_barras, codigo_produto, descricao, quantidade]):
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showwarning('Atenção', 'Quantidade deve ser um número!')
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT codigo_barras FROM produtos WHERE codigo_barras = ? AND id != ?', (codigo_barras, produto_id))
        if cursor.fetchone():
            messagebox.showwarning('Atenção', f'O código de barras {codigo_barras} já está cadastrado!')
            conn.close()
            return

        cursor.execute('UPDATE produtos SET codigo_barras = ?, codigo_produto = ?, descricao = ?, quantidade = ? WHERE id = ?', 
                       (codigo_barras, codigo_produto, descricao, quantidade, produto_id))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Produto atualizado com sucesso!')
        popup.destroy()
        self.carregar_produtos()

    def excluir_produto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um produto para excluir!')
            return
        produto_id = self.tree.item(selected[0], 'tags')[0]

        if not messagebox.askyesno('Confirmação', 'Tem certeza que deseja excluir este produto?'):
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Produto excluído com sucesso!')
        self.carregar_produtos()