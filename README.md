# Codigo de exemplo de geracao de mundo e execucao de caminho minimo 

Este repositório contém a implementação e simulação computacional desenvolvida para o artigo sobre otimização de *pathfinding* em jogos táticos. O projeto demonstra visual e estatisticamente a diferença de desempenho entre algoritmos de busca em tempo real (como Dijkstra/A*) e abordagens baseadas em dados pré-computados (Compressed Path Databases - CPD).

## 📋 Sobre o Projeto

O objetivo deste código é validar a hipótese de que a técnica CPD elimina o custo de "exploração de fronteira" durante a execução do jogo (*runtime*), transformando a complexidade de navegação para $O(1)$ por passo.

O script executa uma simulação em um mapa de grade de larga escala ($550 \times 550$ células), gerando métricas de tempo, uso de processamento e visualizações comparativas.

### Base Teórica
O projeto é baseado nos conceitos apresentados por:
> Botea, A. (2011). **Ultra-fast optimal pathfinding without runtime search**. *Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment*.

## 🚀 Funcionalidades

* **Geração Procedural de Mapas:** Criação de grids $N \times N$ com obstáculos aleatórios e garantia de solubilidade.
* **Implementação do Dijkstra:** Algoritmo clássico de busca de caminho mínimo com visualização da área explorada.
* **Simulação de Runtime CPD:** Emulação do comportamento de *lookup* (consulta direta) do CPD para comparação de performance.
* **Geração Automática de Gráficos:**
    * exploração (Dijkstra vs CPD).
    * Curva de escalabilidade (Tamanho do Mapa vs Tempo).
    * Gráfico de eficiência de nós visitados.
