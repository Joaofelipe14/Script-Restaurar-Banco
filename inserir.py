import mysql.connector
import os
from tqdm import tqdm

# Configurações de conexão com o banco de dados
config = {
    'user': 'root',
    'password': 'joao1234',
    'host': 'localhost',
    'database': 'bckp_ranna',
    'raise_on_warnings': True
}

# Diretório contendo os arquivos com os inserts
diretorio = "C:/Users/jaofe/OneDrive/Área de Trabalho/teste"

# Nome do arquivo de auditoria
arquivo_auditoria = "auditoria.txt"

# Função para registrar a auditoria da inserção em um arquivo de texto
def registrar_auditoria(tabela, quantidade, sucesso, erro=None):
    with open(arquivo_auditoria, 'a') as arquivo:
        sucesso_str = "SUCESSO" if sucesso else "FALHA"
        arquivo.write(f"Tabela: {tabela}\nQuantidade de dados: {quantidade}\nStatus: {sucesso_str}\n")
        if erro:
            arquivo.write(f"Erro: {erro}\n")
        arquivo.write("\n")

# Função para executar os comandos de inserção e registrar a auditoria
def executar_insercoes():
    # Conectar ao banco de dados
    try:
        conexao = mysql.connector.connect(**config)
        cursor = conexao.cursor()
        print("Conexão com o banco de dados estabelecida.")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return
    
    # Obter a lista de arquivos no diretório
    arquivos = os.listdir(diretorio)

    # Filtrar apenas arquivos .sql
    arquivos_sql = [arquivo for arquivo in arquivos if arquivo.endswith(".sql")]
    
    # Ler e executar os comandos INSERT de cada arquivo
    for arquivo in arquivos_sql:
        arquivo_com_caminho = os.path.join(diretorio, arquivo)
        
        # Abrir o arquivo atual
        with open(arquivo_com_caminho, "r") as arquivo_atual:
            # Ler as linhas do arquivo
            linhas = arquivo_atual.readlines()
            # Verificar se o arquivo está vazio
            if not linhas:
                tqdm.write(f"Arquivo vazio: {arquivo}. Pulando para o próximo.")
                continue
            
            # Extrair informações da primeira linha
            primeira_linha = linhas[0].strip()
            tabela_inicio = primeira_linha.index("INTO") + len("INTO")
            tabela_fim = primeira_linha.index("(")
            nome_tabela = primeira_linha[tabela_inicio:tabela_fim].strip()
            
            colunas_inicio = primeira_linha.index("(") + 1
            colunas_fim = primeira_linha.index(")")
            colunas = primeira_linha[colunas_inicio:colunas_fim].split(",")
            
            # Remover espaços em branco e aspas das colunas
            colunas = [coluna.strip().replace("'", "") for coluna in colunas]
            
            # Contar a quantidade de dados a serem inseridos
            quantidade_dados = len(linhas) - 1  # Excluindo a primeira linha que contém o nome das colunas
            
            # Escrever o nome da tabela no terminal
            print(f"Tabela: {nome_tabela}")
            
            # Executar os comandos INSERT
            with tqdm(total=quantidade_dados, desc="Progresso") as progress:
                for linha in linhas[1:]:
                    linha = linha.strip()
                    if linha:
                        try:
                            cursor.execute(linha)
                            conexao.commit()
                            progress.update(1)
                        except mysql.connector.Error as err:
                            registrar_auditoria(nome_tabela, quantidade_dados, False, str(err))
                            print(f"Erro ao executar comando: {linha}\n{err}")
                            break
                else:
                    registrar_auditoria(nome_tabela, quantidade_dados, True)
                    print("Comandos de inserção executados com sucesso.")
    
    # Fechar a conexão
    cursor.close()
    conexao.close()
    print("Conexão com o banco de dados encerrada.")

# Função principal
def main():
    # Executar a função de inserção
    executar_insercoes()

if __name__ == "__main__":
    main()
