import sqlite3

def criar_banco_de_dados():
    nome_do_arquivo_db = 'database_login.db'
    
    try:
        # Conecta ao banco de dados
        conexao = sqlite3.connect(nome_do_arquivo_db) 
        cursor = conexao.cursor()

        # Cria a tabela 'usuarios' se ela não existir.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                nome_usuario TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                telefone TEXT
            );
        """)

        # Salva as alterações no banco de dados
        conexao.commit()
        # Fecha a conexão com o banco
        conexao.close()
        
        print(f"Banco de dados '{nome_do_arquivo_db}' e tabela 'usuarios' verificados/criados com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao criar o banco de dados: {e}")