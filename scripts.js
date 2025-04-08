const db = require('./database.js');
const nodemailer = require('nodemailer');
const XLSX = require('xlsx');

// Mostrar/Esconder seções
function showSection(sectionId) {
  document.querySelectorAll('section').forEach(section => {
    section.style.display = 'none';
  });
  document.getElementById(sectionId).style.display = 'block';
  if (sectionId === 'fornecedores') carregarFornecedores(); // Carrega fornecedores
  if (sectionId === 'lista-compras') carregarProdutos();   // Carrega produtos
  if (sectionId === 'listas-salvas') carregarListasSalvas(); // Carrega listas salvas
}

// Cadastrar Fornecedor
function cadastrarFornecedor() {
  const nome = document.getElementById('nome-fornecedor').value;
  const telefone = document.getElementById('telefone-fornecedor').value;
  const email = document.getElementById('email-fornecedor').value;
  const cnpj = document.getElementById('cnpj-fornecedor').value;

  db.run(
    `INSERT INTO fornecedores (nome, telefone, email, cnpj) VALUES (?, ?, ?, ?)`,
    [nome, telefone, email, cnpj],
    function (err) {
      if (err) {
        alert('Erro ao cadastrar fornecedor: ' + err.message);
      } else {
        alert('Fornecedor cadastrado com sucesso!');
        document.getElementById('nome-fornecedor').value = '';
        document.getElementById('telefone-fornecedor').value = '';
        document.getElementById('email-fornecedor').value = '';
        document.getElementById('cnpj-fornecedor').value = '';
        carregarFornecedores();
      }
    }
  );
}

// Carregar Fornecedores na Tabela
function carregarFornecedores() {
  const tbody = document.getElementById('fornecedores-cadastrados');
  tbody.innerHTML = '';
  db.all(`SELECT * FROM fornecedores`, (err, rows) => {
    if (err) {
      console.error('Erro ao carregar fornecedores:', err);
      return;
    }
    rows.forEach(fornecedor => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${fornecedor.nome}</td>
        <td>${fornecedor.telefone}</td>
        <td>${fornecedor.email}</td>
        <td>${fornecedor.cnpj}</td>
        <td>
          <button onclick="editarFornecedor(${fornecedor.id})">Editar</button>
          <button onclick="excluirFornecedor(${fornecedor.id})">Excluir</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  });
}

// Editar Fornecedor
function editarFornecedor(id) {
  db.get(`SELECT * FROM fornecedores WHERE id = ?`, [id], (err, fornecedor) => {
    if (err) {
      alert('Erro ao buscar fornecedor: ' + err.message);
      return;
    }
    const nome = prompt('Novo nome:', fornecedor.nome);
    const telefone = prompt('Novo telefone:', fornecedor.telefone);
    const email = prompt('Novo email:', fornecedor.email);
    const cnpj = prompt('Novo CNPJ:', fornecedor.cnpj);

    if (nome && telefone && email && cnpj) {
      db.run(
        `UPDATE fornecedores SET nome = ?, telefone = ?, email = ?, cnpj = ? WHERE id = ?`,
        [nome, telefone, email, cnpj, id],
        function (err) {
          if (err) {
            alert('Erro ao editar fornecedor: ' + err.message);
          } else {
            alert('Fornecedor atualizado com sucesso!');
            carregarFornecedores();
          }
        }
      );
    }
  });
}

// Excluir Fornecedor
function excluirFornecedor(id) {
  if (confirm('Tem certeza que deseja excluir este fornecedor?')) {
    db.run(`DELETE FROM fornecedores WHERE id = ?`, [id], function (err) {
      if (err) {
        alert('Erro ao excluir fornecedor: ' + err.message);
      } else {
        alert('Fornecedor excluído com sucesso!');
        carregarFornecedores();
      }
    });
  }
}

// Cadastrar Produto
function cadastrarProduto() {
  const codigoBarras = document.getElementById('codigo-barras').value;
  const codigoProduto = document.getElementById('codigo-produto').value;
  const descricao = document.getElementById('descricao').value;
  const quantidade = document.getElementById('quantidade').value;

  db.run(
    `INSERT INTO produtos (codigo_barras, codigo_produto, descricao, quantidade) VALUES (?, ?, ?, ?)`,
    [codigoBarras, codigoProduto, descricao, quantidade],
    () => alert('Produto cadastrado!')
  );
}

// Carregar Produtos na Lista
function carregarProdutos() {
  const tbody = document.getElementById('produtos-cadastrados');
  tbody.innerHTML = '';
  db.all(`SELECT * FROM produtos`, (err, rows) => {
    rows.forEach(produto => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${produto.codigo_produto}</td>
        <td>${produto.descricao}</td>
        <td><button onclick="adicionarProdutoLista(${produto.id})">+</button></td>
      `;
      tbody.appendChild(tr);
    });
  });

  // Pesquisa
  document.getElementById('pesquisa-produto').addEventListener('input', (e) => {
    const termo = e.target.value.toLowerCase();
    db.all(
      `SELECT * FROM produtos WHERE codigo_produto LIKE ? OR descricao LIKE ?`,
      [`%${termo}%`, `%${termo}%`],
      (err, rows) => {
        tbody.innerHTML = '';
        rows.forEach(produto => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${produto.codigo_produto}</td>
            <td>${produto.descricao}</td>
            <td><button onclick="adicionarProdutoLista(${produto.id})">+</button></td>
          `;
          tbody.appendChild(tr);
        });
      }
    );
  });
}

// Adicionar Produto à Lista Atual
let listaAtual = [];
function adicionarProdutoLista(produtoId) {
  const quantidade = prompt('Informe a quantidade:');
  if (quantidade) {
    db.get(`SELECT * FROM produtos WHERE id = ?`, [produtoId], (err, produto) => {
      listaAtual.push({
        produtoId,
        quantidade,
        descricao: produto.descricao,
        codigo: produto.codigo_produto
      });
      atualizarListaAtual();
    });
  }
}

function atualizarListaAtual() {
  const tbody = document.getElementById('lista-atual');
  tbody.innerHTML = '';
  listaAtual.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${item.codigo}</td>
      <td>${item.descricao}</td>
      <td>${item.quantidade}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Salvar Lista
function salvarLista() {
  const nomeLista = prompt('Nome da lista:');
  const dataCriacao = new Date().toISOString();
  db.run(`INSERT INTO listas (nome, data_criacao) VALUES (?, ?)`, [nomeLista, dataCriacao], function (err) {
    const listaId = this.lastID;
    listaAtual.forEach(item => {
      db.run(
        `INSERT INTO itens_lista (lista_id, produto_id, quantidade) VALUES (?, ?, ?)`,
        [listaId, item.produtoId, item.quantidade]
      );
    });
    alert('Lista salva!');
    listaAtual = [];
    atualizarListaAtual();
  });
}

// Carregar Listas Salvas
function carregarListasSalvas() {
  const tbody = document.getElementById('listas-salvas-tbody');
  tbody.innerHTML = '';
  db.all(`SELECT * FROM listas ORDER BY data_criacao DESC`, (err, listas) => {
    listas.forEach(lista => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${new Date(lista.data_criacao).toLocaleDateString()}</td>
        <td>${lista.nome}</td>
        <td>
          <button onclick="enviarEmail(${lista.id})">Enviar Email</button>
          <button onclick="baixarLista(${lista.id})">Baixar</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  });
}

// Enviar Email
function enviarEmail(listaId) {
  db.all(
    `SELECT * FROM itens_lista JOIN produtos ON itens_lista.produto_id = produtos.id WHERE lista_id = ?`,
    [listaId],
    (err, itens) => {
      const conteudo = itens.map(item => `${item.codigo_produto} - ${item.descricao} - ${item.quantidade}`).join('\n');
      const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: { user: 'seu-email@gmail.com', pass: 'sua-senha' }
      });
      db.all(`SELECT * FROM fornecedores`, (err, fornecedores) => {
        const emails = fornecedores.map(f => f.email).join(',');
        transporter.sendMail(
          {
            from: 'seu-email@gmail.com',
            to: emails,
            subject: 'Lista de Compras',
            text: conteudo,
            attachments: [{ filename: 'lista.xlsx', path: gerarExcel(itens) }]
          },
          () => alert('Email enviado!')
        );
      });
    }
  );
}

// Gerar Excel
function gerarExcel(itens) {
  const ws = XLSX.utils.json_to_sheet(
    itens.map(item => ({
      Código: item.codigo_produto,
      Descrição: item.descricao,
      Quantidade: item.quantidade
    }))
  );
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Lista');
  const caminho = `./lista-${Date.now()}.xlsx`;
  XLSX.writeFile(wb, caminho);
  return caminho;
}

// Baixar Lista
function baixarLista(listaId) {
  db.all(
    `SELECT * FROM itens_lista JOIN produtos ON itens_lista.produto_id = produtos.id WHERE lista_id = ?`,
    [listaId],
    (err, itens) => {
      gerarExcel(itens);
      alert('Lista baixada!');
    }
  );
}