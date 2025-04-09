import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_produto TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL
        )
    ''')

    # Tabela de fornecedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Tabela de perfil
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de listas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_criacao TEXT NOT NULL
        )
    ''')

    # Tabela de itens_lista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_lista (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lista_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER,
            FOREIGN KEY (lista_id) REFERENCES listas(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')

    # Tabela de envios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lista_id INTEGER,
            fornecedor_id INTEGER,
            perfil_id INTEGER,
            data_envio TEXT NOT NULL,
            FOREIGN KEY (lista_id) REFERENCES listas(id),
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
            FOREIGN KEY (perfil_id) REFERENCES perfil(id)
        )
    ''')

    conn.commit()
    conn.close()