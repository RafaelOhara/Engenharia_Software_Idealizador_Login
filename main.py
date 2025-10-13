from app.database import criar_banco_de_dados

if __name__ == '__main__':
    print("Iniciando a criação do banco de dados...")
    criar_banco_de_dados()
    print("Processo finalizado. Verifique a pasta 'instance'.")