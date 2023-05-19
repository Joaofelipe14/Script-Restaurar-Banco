
1. **create_backup.py**: Este arquivo é responsável por processar uma pasta contendo arquivos SQL de inserts e gerar um arquivo `create_backup.sql` com os comandos `CREATE TABLE` correspondentes a partir desses inserts.

   Funcionalidade:
   - Lê os arquivos SQL de inserts em uma pasta específica.
   - Verifica se cada arquivo está vazio e pula para o próximo, se necessário.
   - Extrai informações da primeira linha de cada arquivo para obter o nome da tabela e as colunas.
   - Gera o comando `CREATE TABLE` correspondente no arquivo `create_backup.sql`, com todas as colunas definidas como `VARCHAR(255)`.

   Como rodar:
   - Salve o código em um arquivo chamado `create_backup.py`.
   - Modifique a variável `diretorio` para o caminho da pasta contendo os arquivos SQL de inserts.
   - Execute o script em um ambiente Python compatível.

2. **insert_data.py**: Este arquivo é responsável por executar os comandos `CREATE TABLE` contidos no arquivo `create_backup.sql` e inserir os dados dos arquivos SQL de inserts nas tabelas correspondentes. Ele também registra uma auditoria em um arquivo de texto.

   Funcionalidade:
   - Estabelece uma conexão com um banco de dados MySQL usando as configurações fornecidas.
   - Lê os comandos `CREATE TABLE` do arquivo `create_backup.sql` e executa-os para criar as tabelas.
   - Lê os arquivos SQL de inserts e executa cada comando de inserção na tabela correspondente.
   - Registra uma auditoria, salvando o comando executado e o status de sucesso/falha em um arquivo de texto.
   - Exibe o progresso no terminal, mostrando o nome da tabela e uma barra de progresso.

   Como rodar:
   - Salve o código em um arquivo chamado `insert_data.py`.
   - Certifique-se de ter instalado o módulo `mysql-connector-python` e `tqdm`.
   - Modifique as configurações de conexão no dicionário `config` conforme necessário.
   - Execute o script em um ambiente Python compatível.


 `create_backup.py` e `insert_data.py`  autor "JOAO FELIPE".