import os
from tqdm import tqdm

# Diretório contendo os arquivos com os inserts
diretorio = "C:/Users/jaofe/OneDrive/Área de Trabalho/teste"

# Nome do arquivo de saída
arquivo_saida = "create_backup.sql"

# Definir todas as colunas como VARCHAR(255)
colunas_padrao = "VARCHAR(255)"

# Obter a lista de arquivos no diretório
arquivos = os.listdir(diretorio)

# Filtrar apenas arquivos .sql
arquivos_sql = [arquivo for arquivo in arquivos if arquivo.endswith(".sql")]

# Contador de progresso
total_arquivos = len(arquivos_sql)

# Abrir o arquivo de saída para escrita
with open(arquivo_saida, "w") as arquivo_saida:
    # Iterar sobre os arquivos com a barra de progresso
    for arquivo in tqdm(arquivos_sql, desc="Processando arquivos", unit="arquivo"):
        arquivo_com_caminho = os.path.join(diretorio, arquivo)
        
        # Verificar se o arquivo está vazio
        if os.path.getsize(arquivo_com_caminho) == 0:
            tqdm.write(f"Arquivo vazio: {arquivo}. Pulando para o próximo.")
            continue
        
        # Abrir o arquivo atual
        with open(arquivo_com_caminho, "r") as arquivo_atual:
            # Ler a primeira linha
            primeira_linha = arquivo_atual.readline().strip()
            
            # Extrair o nome da tabela e as colunas
            tabela_inicio = primeira_linha.index("INTO") + len("INTO")
            tabela_fim = primeira_linha.index("(")
            nome_tabela = primeira_linha[tabela_inicio:tabela_fim].strip()
            
            colunas_inicio = primeira_linha.index("(") + 1
            colunas_fim = primeira_linha.index(")")
            colunas = primeira_linha[colunas_inicio:colunas_fim].split(",")
            
            # Remover espaços em branco e aspas das colunas
            colunas = [coluna.strip().replace("'", "") for coluna in colunas]
            
            # Escrever o comando CREATE TABLE no arquivo de saída
            arquivo_saida.write(f"CREATE TABLE {nome_tabela} (\n")
            
            # Escrever as colunas no arquivo de saída
            for i, coluna in enumerate(colunas):
                arquivo_saida.write(f"\t{coluna} {colunas_padrao}")
                
                # Verificar se é a última coluna
                if i < len(colunas) - 1:
                    arquivo_saida.write(",")
                    
                arquivo_saida.write("\n")
            
            arquivo_saida.write(");\n\n")
        
# Exibir mensagem de conclusão
print("Processamento concluído!")
