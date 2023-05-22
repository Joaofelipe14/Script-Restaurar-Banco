import os
from tqdm import tqdm

# Diretório contendo os arquivos com os inserts
diretorio = "C:/Users/jaofe/OneDrive/Área de Trabalho/EVOLUCAO"

# Nome do arquivo de saída
arquivo_saida = "create_backup.sql"

# Nome do arquivo de auditoria
arquivo_auditoria = "auditoria_create.txt"

# Definir todas as colunas como VARCHAR(255)
colunas_padrao = "VARCHAR(255)"

# Abrir o arquivo de auditoria para escrita
auditoria_sucesso = []
auditoria_falha = []
auditoria_vazio = []

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
            auditoria_vazio.append(arquivo)
            continue

        # Abrir o arquivo atual
        with open(arquivo_com_caminho, "r", encoding="utf-8", errors="ignore") as arquivo_atual:
            try:
                # Ler as linhas do arquivo
                linhas = arquivo_atual.readlines()

                # Verificar se o arquivo contém linhas
                if len(linhas) == 0:
                    tqdm.write(f"Arquivo sem linhas: {arquivo}. Pulando para o próximo.")
                    auditoria_vazio.append(arquivo)
                    continue

                # Extrair a primeira linha
                primeira_linha = linhas[0].strip()

                # Verificar se a primeira linha é um comando INSERT INTO válido
                if not primeira_linha.startswith("INSERT INTO") or "VALUES" not in primeira_linha:
                    tqdm.write(f"Comando inválido: {primeira_linha}. Pulando para o próximo.")
                    auditoria_falha.append(arquivo)
                    continue

                # Extrair o nome da tabela
                nome_tabela_inicio = primeira_linha.index("INSERT INTO") + len("INSERT INTO")
                nome_tabela_fim = primeira_linha.index("(")
                nome_tabela = primeira_linha[nome_tabela_inicio:nome_tabela_fim].strip()

                # Extrair as colunas
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

                # Adicionar o nome da tabela à auditoria de sucesso
                auditoria_sucesso.append(nome_tabela)

            except Exception as err:
                tqdm.write(f"Erro ao processar o arquivo: {arquivo}\n{err}")
                auditoria_falha.append(arquivo)

# Salvar a auditoria no arquivo
with open(arquivo_auditoria, "w") as arquivo_auditoria:
    arquivo_auditoria.write("=== Sucesso ===\n")
    arquivo_auditoria.write("\n".join(auditoria_sucesso))

    arquivo_auditoria.write("\n\n=== Falha ===\n")
    arquivo_auditoria.write("\n".join(auditoria_falha))

    arquivo_auditoria.write("\n\n=== Vazio ===\n")
    arquivo_auditoria.write("\n".join(auditoria_vazio))

# Exibir mensagem de conclusão
print("Processamento concluído!")
