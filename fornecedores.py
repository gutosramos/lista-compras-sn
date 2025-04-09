import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from styles import Styles

class Fornecedores:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=Styles.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Formulário de Cadastro
        form_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        form_frame.pack(fill=tk.X, pady=Styles.PADY)

        tk.Label(form_frame, text='Cadastrar Fornecedor', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=0, column=0, columnspan=2, pady=Styles.PADY)

        tk.Label(form_frame, text='Nome', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=1, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.nome_entry = tk.Entry(form_frame, font=Styles.FONT)
        self.nome_entry.grid(row=1, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.nome_entry.insert(0, '')

        tk.Label(form_frame, text='Telefone', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=2, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.telefone_entry = tk.Entry(form_frame, font=Styles.FONT)
        self.telefone_entry.grid(row=2, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.telefone_entry.insert(0, '')

        tk.Label(form_frame, text='Email', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=3, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.email_entry = tk.Entry(form_frame, font=Styles.FONT)
        self.email_entry.grid(row=3, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.email_entry.insert(0, '')

        tk.Label(form_frame, text='CNPJ', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).grid(row=4, column=0, padx=Styles.PADX, pady=Styles.PADY, sticky='e')
        self.cnpj_entry = tk.Entry(form_frame, font=Styles.FONT)
        self.cnpj_entry.grid(row=4, column=1, padx=Styles.PADX, pady=Styles.PADY, sticky='ew')
        self.cnpj_entry.insert(0, '')

        tk.Button(form_frame, text='Cadastrar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.cadastrar_fornecedor).grid(row=5, column=0, pady=Styles.PADY)
        tk.Button(form_frame, text='Importar CSV', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.importar_csv).grid(row=5, column=1, pady=Styles.PADY)

        form_frame.columnconfigure(1, weight=1)

        # Tabela de Fornecedores com Scrollbar
        table_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=Styles.PADY)

        tk.Label(table_frame, text='Fornecedores Cadastrados', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        
        # Criar Treeview com Scrollbar
        self.tree = ttk.Treeview(table_frame, columns=('Nome', 'Telefone', 'Email', 'CNPJ'), show='headings', height=10)
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('CNPJ', text='CNPJ')
        self.tree.column('Nome', width=150)
        self.tree.column('Telefone', width=100)
        self.tree.column('Email', width=150)
        self.tree.column('CNPJ', width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botões de Ação
        action_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        action_frame.pack(fill=tk.X, pady=Styles.PADY)
        tk.Button(action_frame, text='Editar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.editar_fornecedor).pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(action_frame, text='Excluir', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.excluir_fornecedor).pack(side=tk.LEFT, padx=Styles.PADX)

    def load_data(self):
        self.carregar_fornecedores()

    def cadastrar_fornecedor(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        cnpj = self.cnpj_entry.get()

        if not all([nome, telefone, email, cnpj]):
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM fornecedores WHERE email = ?', (email,))
        if cursor.fetchone():
            messagebox.showwarning('Atenção', f'O email {email} já está cadastrado!')
            conn.close()
            return

        cursor.execute('INSERT INTO fornecedores (nome, telefone, email, cnpj) VALUES (?, ?, ?, ?)', 
                       (nome, telefone, email, cnpj))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Fornecedor cadastrado com sucesso!')
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.cnpj_entry.delete(0, tk.END)
        self.carregar_fornecedores()

    def carregar_fornecedores(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM fornecedores')
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=(row[1], row[2], row[3], row[4]), tags=(row[0],))
        conn.close()

    def importar_csv(self):
        arquivo = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if not arquivo:
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        fornecedores_importados = 0
        emails_duplicados = []

        try:
            with open(arquivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if not all(col in reader.fieldnames for col in ['nome', 'telefone', 'email', 'cnpj']):
                    messagebox.showerror('Erro', 'O CSV deve conter as colunas: nome, telefone, email, cnpj')
                    conn.close()
                    return

                for row in reader:
                    nome = row['nome'].strip()
                    telefone = row['telefone'].strip()
                    email = row['email'].strip()
                    cnpj = row['cnpj'].strip()

                    if not all([nome, telefone, email, cnpj]):
                        emails_duplicados.append(f'{email} (campos incompletos)')
                        continue

                    cursor.execute('SELECT email FROM fornecedores WHERE email = ?', (email,))
                    if cursor.fetchone():
                        emails_duplicados.append(email)
                        continue

                    cursor.execute('INSERT INTO fornecedores (nome, telefone, email, cnpj) VALUES (?, ?, ?, ?)',
                                   (nome, telefone, email, cnpj))
                    fornecedores_importados += 1

            conn.commit()
            mensagem = f'{fornecedores_importados} fornecedores importados com sucesso!'
            if emails_duplicados:
                mensagem += f'\nEmails duplicados ou inválidos ignorados: {", ".join(emails_duplicados)}'
            messagebox.showinfo('Importação Concluída', mensagem)
        except Exception as e:
            conn.rollback()
            messagebox.showerror('Erro', f'Erro ao importar CSV: {str(e)}')
        finally:
            conn.close()
            self.carregar_fornecedores()

    def editar_fornecedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um fornecedor para editar!')
            return
        item = self.tree.item(selected[0])
        fornecedor_id = self.tree.item(selected[0], 'tags')[0]
        valores = item['values']

        popup = tk.Toplevel(self.parent)
        popup.title('Editar Fornecedor')
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

        tk.Label(popup, text='Editar Fornecedor', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)
        nome_edit = tk.Entry(popup, font=Styles.FONT)
        nome_edit.insert(0, valores[0])
        nome_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)
        telefone_edit = tk.Entry(popup, font=Styles.FONT)
        telefone_edit.insert(0, valores[1])
        telefone_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)
        email_edit = tk.Entry(popup, font=Styles.FONT)
        email_edit.insert(0, valores[2])
        email_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)
        cnpj_edit = tk.Entry(popup, font=Styles.FONT)
        cnpj_edit.insert(0, valores[3])
        cnpj_edit.pack(fill=tk.X, padx=Styles.PADX, pady=Styles.PADY)

        tk.Button(popup, text='Salvar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=lambda: self.salvar_edicao_fornecedor(fornecedor_id, nome_edit.get(), telefone_edit.get(), 
                                                                email_edit.get(), cnpj_edit.get(), popup)).pack(pady=Styles.PADY)

    def salvar_edicao_fornecedor(self, fornecedor_id, nome, telefone, email, cnpj, popup):
        if not all([nome, telefone, email, cnpj]):
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM fornecedores WHERE email = ? AND id != ?', (email, fornecedor_id))
        if cursor.fetchone():
            messagebox.showwarning('Atenção', f'O email {email} já está cadastrado!')
            conn.close()
            return

        cursor.execute('UPDATE fornecedores SET nome = ?, telefone = ?, email = ?, cnpj = ? WHERE id = ?', 
                       (nome, telefone, email, cnpj, fornecedor_id))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Fornecedor atualizado com sucesso!')
        popup.destroy()
        self.carregar_fornecedores()

    def excluir_fornecedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um fornecedor para excluir!')
            return
        fornecedor_id = self.tree.item(selected[0], 'tags')[0]

        if not messagebox.askyesno('Confirmação', 'Tem certeza que deseja excluir este fornecedor?'):
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM fornecedores WHERE id = ?', (fornecedor_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo('Sucesso', 'Fornecedor excluído com sucesso!')
        self.carregar_fornecedores()