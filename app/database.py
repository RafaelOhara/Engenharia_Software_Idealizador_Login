import sqlite3

def criar_banco_de_dados():
    nome_do_arquivo_db = 'database.db'
    
    try:
        conexao = sqlite3.connect(nome_do_arquivo_db) # Conecta ao banco de dados
        cursor = conexao.cursor()  

        # Cria a tabela 'idealizador' se ela não existir.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS idealizador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nome_usuario TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL
            );
        """)

        conexao.commit()# Salva as alterações
        conexao.close()# fecha a conexão com o banco
        
        print(f"Banco de dados '{nome_do_arquivo_db}' criado/verificado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao criar o banco de dados: {e}")