import sqlite3
from datetime import datetime

# ============================ CONEXÃO COM BANCO ============================

def conectar():
    return sqlite3.connect('banco.db')

# ============================ CRIAÇÃO DE TABELAS ============================

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()

    # Produtos
    c.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            categoria TEXT,
            validade TEXT,
            quantidade INTEGER,
            preco REAL,
            data_entrada TEXT
        )
    """)

    # Clientes
    c.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_tutor TEXT,
            whatsapp TEXT,
            endereco TEXT,
            sexo TEXT
        )
    """)

    # Pets
    c.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            nome TEXT,
            idade TEXT,
            peso TEXT,
            raca TEXT,
            especie TEXT,
            castrado TEXT,
            cor TEXT,
            sexo_pet TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    # Prontuário
    c.execute("""
        CREATE TABLE IF NOT EXISTS prontuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            data TEXT,
            anamnese TEXT,
            tratamento TEXT,
            exames TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    """)

    # Vendas
    c.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            data TEXT,
            forma_pagamento TEXT,
            status_pagamento TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    """)

    # Itens da venda
    c.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER,
            valor_unitario REAL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    conn.commit()
    conn.close()

# ============================ PRODUTOS ============================

def listar_produtos_estoque():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    resultado = c.fetchall()
    conn.close()
    return resultado

def buscar_produto(nome, categoria):
    conn = conectar()
    c = conn.cursor()
    if categoria == "Todas as categorias":
        c.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + nome + '%',))
    else:
        c.execute("SELECT * FROM produtos WHERE nome LIKE ? AND categoria = ?", ('%' + nome + '%', categoria))
    produtos = c.fetchall()
    conn.close()
    return produtos

def adicionar_produto(nome, categoria, validade, quantidade, preco, data_entrada):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        INSERT INTO produtos (nome, categoria, validade, quantidade, preco, data_entrada)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, categoria, validade, quantidade, preco, data_entrada))
    conn.commit()
    conn.close()

def editar_produto(produto_id, nome, categoria, validade, quantidade, preco, data_entrada):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        UPDATE produtos
        SET nome = ?, categoria = ?, validade = ?, quantidade = ?, preco = ?, data_entrada = ?
        WHERE id = ?
    """, (nome, categoria, validade, quantidade, preco, data_entrada, produto_id))
    conn.commit()
    conn.close()

def excluir_produto(produto_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

# ============================ CLIENTES ============================

def adicionar_cliente(nome_tutor, whatsapp, endereco, sexo):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        INSERT INTO clientes (nome_tutor, whatsapp, endereco, sexo)
        VALUES (?, ?, ?, ?)
    """, (nome_tutor, whatsapp, endereco, sexo))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()
    conn.close()
    return clientes

def buscar_clientes_por_nome(nome_tutor):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM clientes WHERE nome_tutor LIKE ?", ('%' + nome_tutor + '%',))
    clientes = c.fetchall()
    conn.close()
    return clientes

def editar_cliente(cliente_id, nome_tutor, whatsapp, endereco, sexo):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        UPDATE clientes
        SET nome_tutor = ?, whatsapp = ?, endereco = ?, sexo = ?
        WHERE id = ?
    """, (nome_tutor, whatsapp, endereco, sexo, cliente_id))
    conn.commit()
    conn.close()

def excluir_cliente(cliente_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

# ============================ PETS ============================

def adicionar_pet(cliente_id, nome, idade, peso, raca, especie, castrado, cor, sexo_pet):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        INSERT INTO pets (cliente_id, nome, idade, peso, raca, especie, castrado, cor, sexo_pet)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (cliente_id, nome, idade, peso, raca, especie, castrado, cor, sexo_pet))
    conn.commit()
    conn.close()

def listar_pets():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        SELECT pets.id, pets.nome, pets.idade, pets.peso, pets.raca, pets.especie, 
               pets.castrado, pets.cor, clientes.nome_tutor
        FROM pets
        INNER JOIN clientes ON pets.cliente_id = clientes.id
        ORDER BY pets.nome ASC
    """)
    pets = c.fetchall()
    conn.close()
    return pets

def listar_pets_por_cliente(cliente_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM pets WHERE cliente_id = ?", (cliente_id,))
    pets = c.fetchall()
    conn.close()
    return pets

def editar_pet(pet_id, nome, idade, peso, raca, especie, castrado, cor, sexo_pet):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        UPDATE pets
        SET nome = ?, idade = ?, peso = ?, raca = ?, especie = ?, castrado = ?, cor = ?, sexo_pet = ?
        WHERE id = ?
    """, (nome, idade, peso, raca, especie, castrado, cor, sexo_pet, pet_id))
    conn.commit()
    conn.close()

def excluir_pet(pet_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
    conn.commit()
    conn.close()

# ============================ PRONTUÁRIO ============================

def inserir_prontuario(pet_id, data, anamnese, tratamento, exames):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("""
            INSERT INTO prontuario (pet_id, data, anamnese, tratamento, exames)
            VALUES (?, ?, ?, ?, ?)
        """, (pet_id, data, anamnese, tratamento, exames))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir prontuário: {e}")
    finally:
        conn.close()

def listar_prontuarios_por_pet(pet_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, data, anamnese, tratamento, exames FROM prontuario WHERE pet_id = ? ORDER BY data DESC", (pet_id,))
    registros = c.fetchall()
    conn.close()
    return registros

def editar_prontuario(prontuario_id, data, anamnese, tratamento, exames):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT * FROM prontuario WHERE id = ?", (prontuario_id,))
        if c.fetchone() is None:
            raise ValueError("Prontuário não encontrado.")
        c.execute("""
            UPDATE prontuario
            SET data = ?, anamnese = ?, tratamento = ?, exames = ?
            WHERE id = ?
        """, (data, anamnese, tratamento, exames, prontuario_id))
        conn.commit()
    except Exception as e:
        print(f"Erro ao editar prontuário: {e}")
    finally:
        conn.close()

def excluir_prontuario(prontuario_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM prontuario WHERE id = ?", (prontuario_id,))
    conn.commit()
    conn.close()

# ============================ VENDAS ============================
def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def registrar_venda(pet_id, carrinho, forma_pagamento, status_pagamento):
    conn = conectar()
    c = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO vendas (pet_id, data, forma_pagamento, status_pagamento)
        VALUES (?, ?, ?, ?)
    """, (pet_id, data, forma_pagamento, status_pagamento))
    venda_id = c.lastrowid

    for item in carrinho:
        produto_id = item["id"]
        quantidade = item["quantidade"]
        preco = item["preco"]

        c.execute("""
            INSERT INTO itens_venda (venda_id, produto_id, quantidade, valor_unitario)
            VALUES (?, ?, ?, ?)
        """, (venda_id, produto_id, quantidade, preco))

        c.execute("""
            UPDATE produtos SET quantidade = quantidade - ?
            WHERE id = ?
        """, (quantidade, produto_id))

    conn.commit()
    conn.close()
    return venda_id

def listar_vendas():
    conn = conectar()
    c = conn.cursor()
    query = """
        SELECT 
            v.id AS venda_id,
            pets.nome AS pet_nome,
            clientes.nome_tutor AS cliente_nome,
            v.data,
            v.forma_pagamento,
            v.status_pagamento,
            GROUP_CONCAT(produtos.nome || ' x' || itens_venda.quantidade || ' (R$ ' || itens_venda.valor_unitario || ')', ', ') AS itens,
            SUM(itens_venda.quantidade * itens_venda.valor_unitario) AS total
        FROM vendas v
        INNER JOIN pets ON v.pet_id = pets.id
        INNER JOIN clientes ON pets.cliente_id = clientes.id
        INNER JOIN itens_venda ON v.id = itens_venda.venda_id
        INNER JOIN produtos ON itens_venda.produto_id = produtos.id
        GROUP BY v.id
        ORDER BY v.data DESC
    """
    c.execute(query)
    vendas = c.fetchall()
    conn.close()
    return vendas