import sqlite3
from package.planta import Planta
from package.animal import Animal
from package.fazenda import Fazenda

def conectar():
    return sqlite3.connect("fazenda.db")
    
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fazenda (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            dinheiro REAL,
            dia INTEGER,
            energia INTEGER,
            nivel INTEGER,
            xp INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            preco REAL
    )
""")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plantas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            crescida INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            produzido INTEGER
        )
    """)

    conn.commit()
    conn.close()

def salvar_fazenda(fazenda):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO fazenda (id, nome, dinheiro, dia, energia, nivel, xp)
        VALUES (1, ?, ?, ?, ?, ?, ?)
    """, (fazenda.nome, fazenda.dinheiro, fazenda.dia, fazenda.energia, fazenda.nivel, fazenda.xp))

    cursor.execute("DELETE FROM estoque")
    cursor.execute("DELETE FROM plantas")
    cursor.execute("DELETE FROM animais")

    for item in fazenda.estoque:
        nome = item.get("nome", "Desconhecido")
        quantidade = item.get("quantidade", 1)  
        preco = item.get("preco", 0)

        cursor.execute("""
            INSERT INTO estoque (nome, quantidade, preco)
            VALUES (?, ?, ?)
    """, (nome, quantidade, preco))



    for planta in fazenda.plantas:
        cursor.execute(
            "INSERT INTO plantas (nome, crescida) VALUES (?, ?)",
            (planta.nome, int(planta.crescida))
        )

    for animal in fazenda.animais:
        cursor.execute("""
            INSERT INTO animais (nome, produzido)
            VALUES (?, ?)
    """, (animal.nome, animal.produto))

    conn.commit()
    conn.close()

def carregar_fazenda():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fazenda WHERE id = 1")
    dados = cursor.fetchone()

    if not dados:
        conn.close()
        return None  

    fazenda = Fazenda(dados[1])
    fazenda.dinheiro = dados[2]
    fazenda.dia = dados[3]
    fazenda.energia = dados[4]
    fazenda.nivel = dados[5]
    fazenda.xp = dados[6] if len(dados) > 6 else 0
    fazenda.energia_maxima = fazenda.calcular_energia_maxima()

    cursor.execute("SELECT nome, quantidade, preco FROM estoque")
    for nome, qtd, preco in cursor.fetchall():
        fazenda.estoque.append({"nome": nome, "quantidade": qtd, "preco": preco})


    cursor.execute("SELECT nome, crescida FROM plantas")
    for nome, crescida in cursor.fetchall():
        planta = Planta(nome, custo=0)
        planta.crescida = bool(crescida)
        fazenda.plantas.append(planta)

    cursor.execute("SELECT nome, produzido FROM animais")
    for nome, produzido in cursor.fetchall():

        if nome.lower() == "galinha":
            dias_para_produzir = 1
        elif nome.lower() == "vaca":
            dias_para_produzir = 2
        elif nome.lower() == "ovelha":
            dias_para_produzir = 3
        elif nome.lower() == "porco":
            dias_para_produzir = 4
        else:
            dias_para_produzir = 2  

    animal = Animal(nome, preco=0, produto=produzido, dias_para_produzir=dias_para_produzir)
    fazenda.animais.append(animal)


    conn.close()
    return fazenda
