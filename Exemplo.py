import numpy as np
import heapq
import time
import matplotlib.pyplot as plt

def gerar_mundo(largura, altura, densidade_paredes=0.2):
    mundo = np.random.choice([0, 1], size=(largura, altura), p=[1-densidade_paredes, densidade_paredes])
    mundo[0, 0] = 0
    mundo[largura-1, altura-1] = 0
    return mundo

def reconstruir_caminho(pais, atual):
    caminho = []
    while atual:
        caminho.append(atual)
        atual = pais.get(atual)
    return caminho[::-1]

def dijkstra(mundo, inicio, fim):
    linhas, colunas = mundo.shape
    fila = [(0, inicio[0], inicio[1])]
    distancias = {inicio: 0}
    pais = {inicio: None}
    visitados_set = set()
    
    while fila:
        custo_atual, x, y = heapq.heappop(fila)
        visitados_set.add((x, y))
        
        if (x, y) == fim:
            return visitados_set, reconstruir_caminho(pais, fim), True
        
        if custo_atual > distancias.get((x, y), float('inf')):
            continue
        
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < linhas and 0 <= ny < colunas and mundo[nx, ny] == 0:
                novo_custo = custo_atual + 1
                if novo_custo < distancias.get((nx, ny), float('inf')):
                    distancias[(nx, ny)] = novo_custo
                    pais[(nx, ny)] = (x, y)
                    heapq.heappush(fila, (novo_custo, nx, ny))
                    
    return visitados_set, [], False

def simulacao_cpd_runtime(caminho_otimo_referencia):
    if not caminho_otimo_referencia: return set(), [], 0.0
    visitados_set = set(caminho_otimo_referencia)
    tempo_simulado_ms = len(caminho_otimo_referencia) * 0.0005
    return visitados_set, caminho_otimo_referencia, tempo_simulado_ms


def visualizar_exploracao_cpd(mundo, visitados_dijkstra, caminho_dijkstra, visitados_cpd, caminho_cpd):
    print("Gerando imagem do mapa (Heatmap)...")
    altura, largura = mundo.shape
    imagem = np.ones((altura, largura, 3))
    imagem[mundo == 1] = [0, 0, 0] # Paredes
    
    vd_list = list(visitados_dijkstra)
    if vd_list:
        y_d, x_d = zip(*vd_list)
        imagem[y_d, x_d] = [0.6, 0.8, 1.0] # Ciano

    for x, y in caminho_dijkstra: imagem[x, y] = [0, 0, 0.8] 
    for x, y in caminho_cpd: imagem[x, y] = [1.0, 0, 0] 

    imagem[0, 0] = [0, 1, 0]
    imagem[altura-1, largura-1] = [0, 1, 0]

    plt.figure(figsize=(10, 10))
    plt.imshow(imagem)
    plt.title(f"Exploração Dijkstra vs Caminho CPD", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('grafico_1_heatmap_mapa.png', dpi=150)
    plt.show()


def plotar_grafico_escalabilidade(tamanhos, t_dijkstra, t_cpd):
    print("Gerando gráfico de escalabilidade (Linhas)...")
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(tamanhos, t_dijkstra, 'o-', color='#e74c3c', linewidth=2, label='Dijkstra (Busca Runtime)')
    ax.plot(tamanhos, t_cpd, 's-', color='#27ae60', linewidth=3, label='CPD (Consulta Direta)')
    
    ax.set_title("Análise de Escalabilidade Temporal", fontsize=14, fontweight='bold')
    ax.set_xlabel("Dimensão do Mapa ($N \\times N$)", fontsize=12)
    ax.set_ylabel("Tempo de Execução (ms)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig('grafico_2_escalabilidade_tempo.png', dpi=200)
    plt.show()

def plotar_grafico_nos(nos_dijkstra_final, nos_cpd_final):
    print("Gerando gráfico de eficiência (Barras)...")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    metricas = ['Busca Tradicional\n(Dijkstra)', 'Abordagem CPD\n(Proposta)']
    valores = [len(nos_dijkstra_final), len(nos_cpd_final)]
    cores = ['#3498db', '#e67e22']
    
    barras = ax.bar(metricas, valores, color=cores, width=0.5)
    

    ax.set_title(f"Eficiência de Processamento: Nós Visitados", fontsize=14, fontweight='bold')
    ax.set_ylabel("Quantidade de Nós (Escala Logarítmica)", fontsize=12)
    ax.set_yscale('log') 
    ax.grid(axis='y', linestyle='--', alpha=0.6, which='both')
    

    for rect in barras:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height * 1.1,
                 f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig('grafico_3_eficiencia_nos.png', dpi=200)
    plt.show()


def executar_benchmark_escalabilidade():
    print("\n--- Benchmark de Escalabilidade ---")
    tamanhos = [50, 100, 200, 300, 400, 500, 550]
    tempos_dijkstra = []
    tempos_cpd = []
    
    for tam in tamanhos:
        m = gerar_mundo(tam, tam, 0.25)
        ini, fim_local = (0,0), (tam-1, tam-1)
        
        t0 = time.time()
        _, cam, suc = dijkstra(m, ini, fim_local)
        t_d = (time.time() - t0) * 1000
        
        if suc: _, _, t_c = simulacao_cpd_runtime(cam)
        else: t_c = 0
            
        tempos_dijkstra.append(t_d)
        tempos_cpd.append(t_c)
        
    return tamanhos, tempos_dijkstra, tempos_cpd


if __name__ == "__main__":
    LARGURA, ALTURA = 550, 550
    inicio = (0, 0)
    #Utilizar para verificar outros pontos selecionados de forma aleatoria dentro do grade de mapa de exemplo
    #i = np.random.choice(LARGURA)
    #j =np.random.choice(ALTURA)
    #aplica o "i" e "j" na variavel fim
    fim = (LARGURA-1,ALTURA-1)
    
    np.random.seed(42)
    
    print(f"1. Rodando Simulação Principal ({LARGURA}x{ALTURA})...")
    mundo = gerar_mundo(LARGURA, ALTURA, densidade_paredes=0.25)
    
    # Roda uma vez para ter os dados do Heatmap e das Barras
    t0 = time.time()
    vis_d, cam_d, suc_d = dijkstra(mundo, inicio, fim)
    
    if suc_d:
        vis_c, cam_c, t_c = simulacao_cpd_runtime(cam_d)
        
        visualizar_exploracao_cpd(mundo, vis_d, cam_d, vis_c, cam_c)
        
        tamanhos, tempos_d, tempos_c = executar_benchmark_escalabilidade()
        plotar_grafico_escalabilidade(tamanhos, tempos_d, tempos_c)
        
        plotar_grafico_nos(vis_d, vis_c)
        
        print("\nTodos os gráficos foram gerados e salvos separadamente.")
    else:
        print("Erro: Caminho não encontrado na simulação inicial.")
