const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./database.db');

// Criando tabelas
db.serialize(() => {
  // Tabela Fornecedores
  db.run(`
    CREATE TABLE IF NOT EXISTS fornecedores (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT,
      telefone TEXT,
      email TEXT,
      cnpj TEXT
    )
  `);

  // Tabela Produtos
  db.run(`
    CREATE TABLE IF NOT EXISTS produtos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      codigo_barras TEXT,
      codigo_produto TEXT,
      descricao TEXT,
      quantidade INTEGER
    )
  `);

  // Tabela Listas de Compras
  db.run(`
    CREATE TABLE IF NOT EXISTS listas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      data_criacao TEXT,
      nome TEXT
    )
  `);

  // Tabela Itens da Lista (relaciona listas com produtos)
  db.run(`
    CREATE TABLE IF NOT EXISTS itens_lista (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      lista_id INTEGER,
      produto_id INTEGER,
      quantidade INTEGER,
      FOREIGN KEY (lista_id) REFERENCES listas(id),
      FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
  `);
});

module.exports = db;