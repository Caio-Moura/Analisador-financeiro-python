import sqlite3
import matplotlib.pyplot as plt

# Define o caminho para o banco de dados como uma constante
DB_PATH = 'meu_projeto.db'

def executar_consulta(sql_query):
    """
    Função para conectar ao banco de dados, executar uma consulta e retornar os resultados.
    Recebe uma string com a consulta SQL como argumento.
    """
    results = [] # Inicia a lista de resultados vazia
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        print("Executando a consulta...")
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print("Consulta executada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
    finally:
        if connection:
            connection.close()
    
    return results # Retorna a lista de resultados

# --- A partir daqui, nosso programa principal começa ---

# 1. Definimos a consulta que queremos fazer
consulta_todas = "SELECT * FROM transacoes ORDER BY data DESC;"

# 2. Chamamos nossa função para executar a consulta
transacoes = executar_consulta(consulta_todas)

# 3. Imprimimos os resultados formatados
print("\n--- Relatório de Transações (Mais Recentes Primeiro) ---")
if transacoes: # Verifica se a lista de transações não está vazia
    for transacao in transacoes:
        id_t, tipo_t, origem_t, destino_t, data_t, _, _, valor_t = transacao # Desempacotamento de tupla
        
        print(f"ID: {id_t} | Data: {data_t} | Origem: {origem_t} | Tipo: {tipo_t} | Valor: R$ {valor_t:.2f}")
else:
    print("Nenhuma transação encontrada.")

    # --- analise 2: encontra a transiçao mais cara ---
    # 1. Definimos a nova consulta 
    consulta_mais_cara = "SELECT * FROM transacoes ORDER BY valor DESC LIMIT 1;"
    transicao_cara = executar_consulta(consulta_mais_cara)
    print("\n--- Transação Mais Cara ---")
    if transicao_cara: 
        # como limit 1 so retona uma linha, podemos pegar o primeiro item (indice 0)
        unica_transacao = transicao_cara[0]
        id_t, tipo_t, origem_t, destino_t, data_t, _, _, valor_t = unica_transacao 
        print(f"A transação mais cara foi de R$ {valor_t:.2f}, feita por '{origem_t}' em {data_t} para '{destino_t}'.")
    else:
        print("Não foi possível encontrar a transação mais cara.")

        # --- Análise 3: Calcular o Valor Total por Tipo de Transação ---

# 1. Definimos a consulta de agregação
consulta_por_tipo = "SELECT tipo_transacao, SUM(valor) FROM transacoes GROUP BY tipo_transacao;"

# 2. Reutilizamos nossa função
totais_por_tipo = executar_consulta(consulta_por_tipo)

# 3. Imprimimos o resultado desta análise
print("\n--- Valor Total por Tipo de Transação ---")
if totais_por_tipo:
    for tipo in totais_por_tipo:
        # A tupla agora só tem 2 valores: o tipo (índice 0) e a soma (índice 1)
        nome_tipo = tipo[0]
        soma_valor = tipo[1]
        
        print(f"Tipo: {nome_tipo} | Total Gasto: R$ {soma_valor:.2f}")
else:
    print("Não foi possível calcular os totais por tipo.")
    # --- Análise 4: Gerar um Gráfico de Barras ---

print("\n--- Gerando Gráfico de Gastos por Tipo ---")
if totais_por_tipo:
    # 1. Preparar os dados para o gráfico
    tipos = []
    valores = []
    for tipo in totais_por_tipo:
        tipos.append(tipo[0]) # Pega o nome do tipo (Pix, TED, DOC)
        valores.append(tipo[1]) # Pega o valor total
        
    # 2. Criar o gráfico
    plt.figure(figsize=(8, 5)) # Define o tamanho da figura (largura, altura)
    plt.bar(tipos, valores, color=['#1f77b4', '#ff7f0e', '#2ca02c']) # Cria as barras
    
    # 3. Adicionar títulos e rótulos
    plt.title('Valor Total Gasto por Tipo de Transação')
    plt.xlabel('Tipo de Transação')
    plt.ylabel('Valor Total (R$)')
    plt.grid(axis='y', linestyle='--', alpha=0.7) # Adiciona uma grade horizontal para facilitar a leitura
    
    # 4. Mostrar o gráfico
    print("Gráfico gerado! Feche a janela do gráfico para finalizar o script.")
    plt.show()

else:
    print("Não há dados para gerar o gráfico.")