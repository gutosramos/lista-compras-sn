import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from styles import Styles

class Perfil:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=Styles.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.init_perfil()

    def init_perfil(self):
        content_frame = tk.Frame(self.frame, bg=Styles.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=Styles.PADY)

        tk.Label(content_frame, text='Gerenciar Perfis', font=Styles.FONT_BOLD, bg=Styles.BG_COLOR).pack(pady=Styles.PADY)

        form_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        form_frame.pack(fill=tk.X, pady=Styles.PADY)

        tk.Label(form_frame, text='Nome:', font=Styles.FONT, bg=Styles.BG_COLOR).grid(row=0, column=0, padx=Styles.PADX, pady=Styles.PADY)
        self.nome_entry = tk.Entry(form_frame, font=Styles.FONT)
        self.nome_entry.grid(row=0, column=1, padx=Styles.PADX, pady=Styles.PADY)

        tk.Label(form_frame, text='Email:', font=Styles.FONT, bg=Styles.BG_COLOR).grid(row=1, column=0, padx=Styles.PADX, pady=Styles.PADY)
        self.email_entry = tk.Entry(form_frame, font=Styles.FONT)
        self.email_entry.grid(row=1, column=1, padx=Styles.PADX, pady=Styles.PADY)

        tk.Label(form_frame, text='Senha:', font=Styles.FONT, bg=Styles.BG_COLOR).grid(row=2, column=0, padx=Styles.PADX, pady=Styles.PADY)
        self.senha_entry = tk.Entry(form_frame, font=Styles.FONT, show='*')
        self.senha_entry.grid(row=2, column=1, padx=Styles.PADX, pady=Styles.PADY)

        button_frame = tk.Frame(content_frame, bg=Styles.BG_COLOR)
        button_frame.pack(pady=Styles.PADY)
        tk.Button(button_frame, text='Adicionar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.adicionar_perfil).pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(button_frame, text='Editar', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.editar_perfil).pack(side=tk.LEFT, padx=Styles.PADX)
        tk.Button(button_frame, text='Excluir', font=Styles.FONT, bg=Styles.BUTTON_COLOR, fg=Styles.BUTTON_FG,
                  command=self.excluir_perfil).pack(side=tk.LEFT, padx=Styles.PADX)

        self.perfil_tree = ttk.Treeview(content_frame, columns=('Nome', 'Email'), show='headings', height=10)
        self.perfil_tree.heading('Nome', text='Nome')
        self.perfil_tree.heading('Email', text='Email')
        self.perfil_tree.column('Nome', width=200)
        self.perfil_tree.column('Email', width=200)
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.perfil_tree.yview)
        self.perfil_tree.configure(yscrollcommand=scrollbar.set)
        self.perfil_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.perfil_tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_data(self):
        self.carregar_perfis()

    def carregar_perfis(self):
        for item in self.perfil_tree.get_children():
            self.perfil_tree.delete(item)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, email FROM perfil')
        for row in cursor.fetchall():
            self.perfil_tree.insert('', tk.END, values=(row[1], row[2]), tags=(row[0],))
        conn.close()

    def adicionar_perfil(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not nome or not email or not senha:
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO perfil (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Perfil adicionado com sucesso!')
            self.clear_entries()
            self.carregar_perfis()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'Este email já está cadastrado!')

    def editar_perfil(self):
        selected = self.perfil_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um perfil para editar!')
            return

        perfil_id = self.perfil_tree.item(selected[0], 'tags')[0]
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not nome or not email or not senha:
            messagebox.showwarning('Atenção', 'Preencha todos os campos!')
            return

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE perfil SET nome = ?, email = ?, senha = ? WHERE id = ?', (nome, email, senha, perfil_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Perfil atualizado com sucesso!')
            self.clear_entries()
            self.carregar_perfis()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'Este email já está cadastrado!')

    def excluir_perfil(self):
        selected = self.perfil_tree.selection()
        if not selected:
            messagebox.showwarning('Atenção', 'Selecione um perfil para excluir!')
            return

        perfil_id = self.perfil_tree.item(selected[0], 'tags')[0]
        if not messagebox.askyesno('Confirmação', 'Tem certeza que deseja excluir este perfil?'):
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM perfil WHERE id = ?', (perfil_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Perfil excluído com sucesso!')
        self.carregar_perfis()

    def on_select(self, event):
        selected = self.perfil_tree.selection()
        if selected:
            perfil_id = self.perfil_tree.item(selected[0], 'tags')[0]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT nome, email, senha FROM perfil WHERE id = ?', (perfil_id,))
            nome, email, senha = cursor.fetchone()
            conn.close()
            self.clear_entries()
            self.nome_entry.insert(0, nome)
            self.email_entry.insert(0, email)
            self.senha_entry.insert(0, senha)

    def clear_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)