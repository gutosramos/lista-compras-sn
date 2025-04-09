import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from styles import Styles
import openpyxl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

class ListasSalvas:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=Styles.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.init_listas_salvas()

    def init_listas_salvas(self):
        content_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=Styles.PADY)

        tk.Label(content_frame, text='Listas Salvas', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        
        self.listas_tree = ttk.Treeview(content_frame, columns=('Nome', 'Data Criação'), show='headings', height=15)
        self.listas_tree.heading('Nome', text='Nome')
        self.listas_tree.heading('Data Criação', text='Data Criação')
        self.listas_tree.column('Nome', width=200)
        self.listas_tree.column('Data Criação', width=150)
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.listas_tree.yview)
        self.listas_tree.configure(yscrollcommand=scrollbar.set)
        self.listas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        action_frame.pack(pady=Styles.PADY)
        tk.Button(action_frame, text='Enviar por Email', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.abrir_modal_email).pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(action_frame, text='Editar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.editar_lista).pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(action_frame, text='Excluir', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.excluir_lista).pack(side=tk.LEFT, padx=Styles.PADX)

    def load_data(self):
        self.carregar_listas_salvas()

    def carregar_listas_salvas(self):
        for item in self.listas_tree.get_children():
            self.listas_tree.delete(item)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, data_criacao FROM listas')
        for row in cursor.fetchall():
            nome_lista = row[1]  # Exemplo: lista_10_11_2024
            data_criacao = row[2]
            self.listas_tree.insert('', tk.END, values=(nome_lista, data_criacao), tags=(row[0],))
        conn.close()

    def abrir_modal_email(self):
        selected = self.listas_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione uma lista para enviar!')
            return

        lista_id = self.listas_tree.item(selected[0], 'tags')[0]
        lista_nome = self.listas_tree.item(selected[0], 'values')[0]

        modal = tk.Toplevel(self.parent)
        modal.title('Enviar Lista por Email')
        modal.configure(bg=Styles.BG_COLOR)
        modal.transient(self.parent)
        modal.grab_set()

        modal_width = 600
        modal_height = 550  # Aumentei a altura para acomodar o novo campo CC
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (modal_width // 2)
        y = (screen_height // 2) - (modal_height // 2)
        modal.geometry(f'{modal_width}x{modal_height}+{x}+{y}')

        tk.Label(modal, text='Enviar Lista por Email', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)

        tk.Label(modal, text='Enviar como:', font=Styles.FONT, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        perfil_combo = ttk.Combobox(modal, font=Styles.FONT, state='readonly')
        perfil_combo.pack(padx=Styles.PADX)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, email FROM perfil')
        perfis = cursor.fetchall()
        conn.close()

        if not perfis:
            messagebox.showwarning('Atenção', 'Nenhum perfil cadastrado! Cadastre um perfil primeiro.')
            modal.destroy()
            return

        perfil_dict = {f'{nome} <{email}>': id for id, nome, email in perfis}
        perfil_combo['values'] = list(perfil_dict.keys())
        perfil_combo.current(0)

        # Novo campo para emails em CC
        cc_frame = tk.Frame(modal, bg=Styles.BG_COLOR)
        cc_frame.pack(fill=tk.X, pady=Styles.PADY)
        tk.Label(cc_frame, text='CC (separe os emails por vírgula):', font=Styles.FONT, bg=Styles.BG_COLOR).pack(side=tk.LEFT, padx=Styles.PADX)
        cc_entry = tk.Entry(cc_frame, font=Styles.FONT)
        cc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        search_frame = tk.Frame(modal, bg=Styles.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=Styles.PADY)
        tk.Label(search_frame, text='Buscar Fornecedor:', font=Styles.FONT, bg=Styles.BG_COLOR).pack(side=tk.LEFT, padx=Styles.PADX)
        search_entry = tk.Entry(search_frame, font=Styles.FONT)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        fornecedores_frame = tk.Frame(modal, bg=Styles.BG_COLOR)
        fornecedores_frame.pack(fill=tk.BOTH, expand=True, padx=Styles.PADX)

        fornecedores_tree = ttk.Treeview(fornecedores_frame, columns=('Selecionar', 'Nome', 'Email'), show='headings', height=5)
        fornecedores_tree.heading('Selecionar', text='Enviar')
        fornecedores_tree.heading('Nome', text='Nome')
        fornecedores_tree.heading('Email', text='Email')
        fornecedores_tree.column('Selecionar', width=50, anchor='center')
        fornecedores_tree.column('Nome', width=150)
        fornecedores_tree.column('Email', width=200)
        
        scrollbar = ttk.Scrollbar(fornecedores_frame, orient=tk.VERTICAL, command=fornecedores_tree.yview)
        fornecedores_tree.configure(yscrollcommand=scrollbar.set)
        fornecedores_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.check_vars = {}

        def carregar_fornecedores(busca=''):
            for item in fornecedores_tree.get_children():
                fornecedores_tree.delete(item)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, nome, email FROM fornecedores WHERE nome LIKE ? OR email LIKE ?',
                           (f'%{busca}%', f'%{busca}%'))
            fornecedores = cursor.fetchall()
            conn.close()

            self.check_vars.clear()
            for id_fornecedor, nome, email in fornecedores:
                var = tk.BooleanVar(value=False)
                self.check_vars[(id_fornecedor, nome, email)] = var
                fornecedores_tree.insert('', tk.END, values=('☐' if not var.get() else '☑', nome, email))

        def atualizar_check(item):
            valores = fornecedores_tree.item(item, 'values')
            chave = next(k for k, v in self.check_vars.items() if k[1] == valores[1] and k[2] == valores[2])
            var = self.check_vars[chave]
            var.set(not var.get())
            fornecedores_tree.item(item, values=('☑' if var.get() else '☐', valores[1], valores[2]))
            atualizar_destinatarios()

        fornecedores_tree.bind('<Button-1>', lambda event: self.on_tree_click(event, fornecedores_tree, atualizar_check))
        search_entry.bind('<KeyRelease>', lambda event: carregar_fornecedores(search_entry.get().lower()))

        carregar_fornecedores()

        tk.Label(modal, text=f'Lista Selecionada: {lista_nome}', font=Styles.FONT, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        tk.Label(modal, text='Destinatários Selecionados:', font=Styles.FONT, bg=Styles.BG_COLOR).pack()
        
        self.destinatarios_listbox = tk.Listbox(modal, font=Styles.FONT, height=5)
        self.destinatarios_listbox.pack(fill=tk.X, padx=Styles.PADX)

        def atualizar_destinatarios():
            self.destinatarios_listbox.delete(0, tk.END)
            for (id_fornecedor, nome, email), var in self.check_vars.items():
                if var.get():
                    self.destinatarios_listbox.insert(tk.END, f'{nome} <{email}>')

        tk.Button(modal, text='Enviar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.enviar_email(lista_id, lista_nome, perfil_combo, perfil_dict, cc_entry, modal)).pack(pady=Styles.PADY)

    def on_tree_click(self, event, tree, callback):
        item = tree.identify_row(event.y)
        if item:
            column = tree.identify_column(event.x)
            if column == '#1':
                callback(item)

    def enviar_email(self, lista_id, lista_nome, perfil_combo, perfil_dict, cc_entry, modal):
        # Obter os fornecedores selecionados
        destinatarios = [(id_fornecedor, email) for (id_fornecedor, nome, email), var in self.check_vars.items() if var.get()]
        if not destinatarios:
            messagebox.showwarning('Atenção', 'Selecione pelo menos um fornecedor!')
            return

        # Obter os emails em CC
        cc_emails = [email.strip() for email in cc_entry.get().split(',') if email.strip()]
        # Validar emails em CC (opcional, mas recomendado)
        for email in cc_emails:
            if '@' not in email or '.' not in email:
                messagebox.showwarning('Atenção', f'Email em CC inválido: {email}')
                return

        perfil_selecionado = perfil_combo.get()
        perfil_id = perfil_dict[perfil_selecionado]

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email, senha FROM perfil WHERE id = ?', (perfil_id,))
        remetente, senha = cursor.fetchone()

        dominio = remetente.split('@')[1].lower()
        if dominio in ['gmail.com']:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        elif dominio in ['hotmail.com', 'outlook.com', 'live.com']:
            smtp_server = 'smtp.office365.com'
            smtp_port = 587
        else:
            messagebox.showerror('Erro', f'O domínio de email "{dominio}" não é suportado. Use um email do Gmail ou Hotmail/Outlook.')
            return

        lista_nome_safe = lista_nome.replace('/', '-')

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f'Lista_{lista_nome_safe}'
        ws.append(['Código Produto', 'Descrição', 'Quantidade'])

        cursor.execute('''
            SELECT p.codigo_produto, p.descricao, il.quantidade
            FROM itens_lista il
            JOIN produtos p ON il.produto_id = p.id
            WHERE il.lista_id = ?
        ''', (lista_id,))
        for row in cursor.fetchall():
            ws.append(row)

        excel_file = f'lista_{lista_nome_safe}.xlsx'
        wb.save(excel_file)

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = ', '.join([email for _, email in destinatarios])
        # Adicionar os emails em CC
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        # Definir o assunto como "Cotação {data atual no formato dd/mm/aaaa}"
        data_atual = datetime.now().strftime('%d/%m/%Y')
        msg['Subject'] = f'Cotação {data_atual}'

        with open(excel_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={excel_file}')
            msg.attach(part)

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(remetente, senha)
                # Enviar o email para os destinatários e os emails em CC
                server.send_message(msg)

            # Registrar o envio na tabela envios
            data_envio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            for fornecedor_id, _ in destinatarios:
                cursor.execute('INSERT INTO envios (lista_id, fornecedor_id, perfil_id, data_envio) VALUES (?, ?, ?, ?)',
                               (lista_id, fornecedor_id, perfil_id, data_envio))
            conn.commit()

            messagebox.showinfo('Sucesso', f'Email enviado para {len(destinatarios)} fornecedor(es)!')
            os.remove(excel_file)
            modal.destroy()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao enviar email: {str(e)}')
        finally:
            conn.close()

    def editar_lista(self):
        selected = self.listas_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione uma lista para editar!')
            return

        lista_id = self.listas_tree.item(selected[0], 'tags')[0]
        lista_nome = self.listas_tree.item(selected[0], 'values')[0]

        modal = tk.Toplevel(self.parent)
        modal.title(f'Editar Lista: {lista_nome}')
        modal.configure(bg=Styles.BG_COLOR)
        modal.transient(self.parent)
        modal.grab_set()

        modal_width = 600
        modal_height = 400
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (modal_width // 2)
        y = (screen_height // 2) - (modal_height // 2)
        modal.geometry(f'{modal_width}x{modal_height}+{x}+{y}')

        # Frame da esquerda (Produtos Cadastrados)
        left_frame = tk.Frame(modal, bg=Styles.BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Styles.PADX)

        tk.Label(left_frame, text='Produtos Cadastrados', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)

        # Campo de pesquisa para Produtos Cadastrados
        search_frame = tk.Frame(left_frame, bg=Styles.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, Styles.PADY))
        tk.Label(search_frame, text='Pesquisar Produtos:', font=Styles.FONT, bg=Styles.BG_COLOR).pack(side=tk.LEFT, padx=Styles.PADX)
        search_entry_produtos = tk.Entry(search_frame, font=Styles.FONT)
        search_entry_produtos.pack(side=tk.LEFT, fill=tk.X, expand=True)

        produtos_tree = ttk.Treeview(left_frame, columns=('Código Produto', 'Descrição'), show='headings', height=10)
        produtos_tree.heading('Código Produto', text='Código Produto')
        produtos_tree.heading('Descrição', text='Descrição')
        produtos_tree.column('Código Produto', width=100)
        produtos_tree.column('Descrição', width=150)
        
        scrollbar_produtos = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=produtos_tree.yview)
        produtos_tree.configure(yscrollcommand=scrollbar_produtos.set)
        produtos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_produtos.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista para armazenar todos os produtos (para pesquisa)
        produtos_lista = []

        # Carregar os produtos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT codigo_produto, descricao FROM produtos')
        for row in cursor.fetchall():
            produtos_lista.append(row)
            produtos_tree.insert('', tk.END, values=row)

        # Função para filtrar produtos
        def filtrar_produtos():
            termo = search_entry_produtos.get().lower()
            for item in produtos_tree.get_children():
                produtos_tree.delete(item)
            for valores in produtos_lista:
                if termo in valores[0].lower() or termo in valores[1].lower():
                    produtos_tree.insert('', tk.END, values=valores)

        # Vincular a pesquisa ao campo de entrada
        search_entry_produtos.bind('<KeyRelease>', lambda event: filtrar_produtos())

        # Frame do meio (Botões de Adicionar/Remover)
        middle_frame = tk.Frame(modal, bg=Styles.BG_COLOR)
        middle_frame.pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(middle_frame, text='Adicionar ->', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.adicionar_item_edit(produtos_tree, itens_tree)).pack(pady=Styles.PADY)
        tk.Button(middle_frame, text='<- Remover', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.remover_item_edit(itens_tree)).pack(pady=Styles.PADY)

        # Frame da direita (Itens da Lista)
        right_frame = tk.Frame(modal, bg=Styles.BG_COLOR)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Styles.PADX)

        tk.Label(right_frame, text='Itens da Lista', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        itens_tree = ttk.Treeview(right_frame, columns=('Código Produto', 'Descrição', 'Quantidade'), show='headings', height=10)
        itens_tree.heading('Código Produto', text='Código Produto')
        itens_tree.heading('Descrição', text='Descrição')
        itens_tree.heading('Quantidade', text='Quantidade')
        itens_tree.column('Código Produto', width=100)
        itens_tree.column('Descrição', width=150)
        itens_tree.column('Quantidade', width=50)
        
        scrollbar_itens = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=itens_tree.yview)
        itens_tree.configure(yscrollcommand=scrollbar_itens.set)
        itens_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_itens.pack(side=tk.RIGHT, fill=tk.Y)

        cursor.execute('''
            SELECT p.codigo_produto, p.descricao, il.quantidade
            FROM itens_lista il
            JOIN produtos p ON il.produto_id = p.id
            WHERE il.lista_id = ?
        ''', (lista_id,))
        for row in cursor.fetchall():
            itens_tree.insert('', tk.END, values=row)
        conn.close()

        tk.Button(modal, text='Salvar Alterações', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.salvar_edicao_lista(lista_id, itens_tree, modal)).pack(pady=Styles.PADY)

    def adicionar_item_edit(self, produtos_tree, itens_tree):
        selected = produtos_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um produto para adicionar!')
            return
        valores = produtos_tree.item(selected[0], 'values')
        itens_tree.insert('', tk.END, values=(valores[0], valores[1], 1))

    def remover_item_edit(self, itens_tree):
        selected = itens_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um item para remover!')
            return
        itens_tree.delete(selected[0])

    def salvar_edicao_lista(self, lista_id, itens_tree, modal):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM itens_lista WHERE lista_id = ?', (lista_id,))

        for item in itens_tree.get_children():
            valores = itens_tree.item(item, 'values')
            cursor.execute('SELECT id FROM produtos WHERE codigo_produto = ?', (valores[0],))
            produto_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO itens_lista (lista_id, produto_id, quantidade) VALUES (?, ?, ?)',
                           (lista_id, produto_id, valores[2]))

        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Lista atualizada com sucesso!')
        modal.destroy()
        self.carregar_listas_salvas()

    def excluir_lista(self):
        selected = self.listas_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione uma lista para excluir!')
            return

        lista_id = self.listas_tree.item(selected[0], 'tags')[0]
        if not messagebox.askyesno('Confirmação', 'Tem certeza que deseja excluir esta lista?'):
            return

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            # Excluir registros associados em itens_lista
            cursor.execute('DELETE FROM itens_lista WHERE lista_id = ?', (lista_id,))
            # Verificar se a tabela envios existe antes de tentar excluir
            cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='envios' ''')
            if cursor.fetchone()[0] == 1:
                cursor.execute('DELETE FROM envios WHERE lista_id = ?', (lista_id,))
            # Excluir a lista
            cursor.execute('DELETE FROM listas WHERE id = ?', (lista_id,))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Lista excluída com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao excluir a lista: {str(e)}')
        finally:
            conn.close()

        self.carregar_listas_salvas()