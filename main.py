# Função recursiva para achar o numero maximo de regioes (Sua lógica perfeita!)
def calcula_regioes(n):
    # Caso base
    if n == 0:
        return 1
    
    # Passo recursivo resolvendo as combinacoes
    comb3 = ((n - 1) * (n - 2) * (n - 3)) // 6
    comb1 = n - 1
    
    return calcula_regioes(n - 1) + comb3 + comb1

# Função para mostrar o resultado formatado usando while
def mostra_sequencia(m):
    print("=========================================")
    print(" Filtros dos Sonhos - Termos da Sequencia")
    print("=========================================")
    print("n     a(n)")
    print("-----------------------------------------")
    
    # Começamos com n = 1
    n = 1
    
    # O laço vai continuar rodando enquanto n for menor ou igual a m
    while n <= m:
        atual = calcula_regioes(n)
        print(f"{n}     {atual}")
        
        # IMPORTANTE: Avança para o próximo número para não ficar num laço infinito
        n = n + 1
        
    print("=========================================")

# --- Programa Principal ---
m = int(input("Digite quantos termos voce quer ver (m): "))

if m <= 0:
    print("Por favor, digite um numero maior que zero.")
else:
    mostra_sequencia(m)
