Estrutura Geral do Projeto
    Tecnologias:
        Electron: Para criar a interface desktop.
        JavaScript: Lógica principal.
        SQLite: Banco de dados leve para armazenar fornecedores, produtos e listas.
        HTML/CSS: Interface gráfica.
    Bibliotecas adicionais:
        sqlite3 (para Node.js): Integração com SQLite.
        nodemailer (opcional): Para envio de emails.
        xlsx: Para gerar arquivos Excel.

Estrutura de Pastas:
    meu-projeto/
    ├── main.js           # Arquivo principal do Electron
    ├── index.html        # Interface inicial
    ├── styles.css        # Estilos
    ├── scripts.js        # Lógica da interface
    ├── database.js       # Conexão e consultas ao SQLite
    └── package.json      # Dependências