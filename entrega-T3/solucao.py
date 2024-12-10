from typing import Iterable, Set, Tuple
import heapq
import time 
from collections import deque

class Nodo:
    def __init__(self, estado:str, pai:'Nodo', acao:str, custo:int):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.sucessores = []

    def __eq__(self, other):
        if isinstance(other, Nodo):
            return self.estado == other.estado
        return False

    def __hash__(self):
        return hash(self.estado)
    
    def __lt__(self, other):
        return self.custo < other.custo
    
    def adiciona_sucessor(self, nodo_sucessor:'Nodo'):
        self.sucessores.append(nodo_sucessor)


def sucessor(estado:str)->Set[Tuple[str,str]]:

    def trocar(s, i, j):
        lst = list(s)
        lst[i], lst[j] = lst[j], lst[i]
        return ''.join(lst)

    movimentos = {
        'acima': -3,
        'abaixo': 3,
        'esquerda': -1,
        'direita': 1
    }
    
    pos_vazia = estado.index('_')
    acoes_possiveis = set()

    for acao, deslocamento in movimentos.items():
        nova_pos = pos_vazia + deslocamento
        if 0 <= nova_pos < 9:
            if acao == 'esquerda' and pos_vazia % 3 == 0:
                continue
            if acao == 'direita' and pos_vazia % 3 == 2:
                continue
            novo_estado = trocar(estado, pos_vazia, nova_pos)
            acoes_possiveis.add((acao, novo_estado))

    return acoes_possiveis


def expande(nodo:Nodo)->Set[Nodo]:
    sucessores = sucessor(nodo.estado)
    novos_nodos = set()

    for acao, estado_sucessor in sucessores:
        novo_nodo = Nodo(
            estado=estado_sucessor,
            pai=nodo,         
            acao=acao,        
            custo=nodo.custo + 1  
        )
        novos_nodos.add(novo_nodo)
        nodo.adiciona_sucessor(novo_nodo)
    
    return novos_nodos


def hamming_distance(estado: str) -> int:
    objetivo = "12345678_"
    return sum(1 for i, c in enumerate(estado) if c != objetivo[i] and c != '_')

def manhattan_distance(estado: str) -> int:
    objetivo = "12345678_"
    distancia = 0
    for i, c in enumerate(estado):
        if c != '_' and c != objetivo[i]:
            objetivo_index = objetivo.index(c)
            distancia += abs(i // 3 - objetivo_index // 3) + abs(i % 3 - objetivo_index % 3)
    return distancia

def reconstruct_path(nodo: Nodo) -> list[str]:
    path = []
    while nodo.pai is not None:
        path.append(nodo.acao)
        nodo = nodo.pai
    return path[::-1]

def astar_hamming(estado:str)->list[str]:
    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = [(hamming_distance(estado), nodo_inicial)]
    explorados = set()
    #nos_expandidos = 0

    #start_time = time.time()

    while fronteira:
        _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == objetivo:
            #end_time = time.time()
            return reconstruct_path(nodo_atual)#, nos_expandidos, end_time - start_time

        explorados.add(nodo_atual.estado)
        #nos_expandidos += 1

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_estimado = nodo_sucessor.custo + hamming_distance(nodo_sucessor.estado)
                heapq.heappush(fronteira, (custo_estimado, nodo_sucessor))

    return None#, nos_expandidos, time.time() - start_time



def astar_manhattan(estado:str)->list[str]:
    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = [(manhattan_distance(estado), nodo_inicial)]
    explorados = set()
    #nos_expandidos = 0

    #start_time = time.time()

    while fronteira:
        _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == objetivo:
            #end_time = time.time()
            return reconstruct_path(nodo_atual)#, nos_expandidos, end_time - start_time

        explorados.add(nodo_atual.estado)
        #nos_expandidos += 1

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_estimado = nodo_sucessor.custo + manhattan_distance(nodo_sucessor.estado)
                heapq.heappush(fronteira, (custo_estimado, nodo_sucessor))

    return None#, nos_expandidos, time.time() - start_time
 

def bfs(estado:str)->list[str]:
    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = deque([nodo_inicial])
    explorados = set()

    while fronteira:
        nodo_atual = fronteira.popleft()

        if nodo_atual.estado == objetivo:
            return reconstruct_path(nodo_atual)

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados and nodo_sucessor not in fronteira:
                fronteira.append(nodo_sucessor)

    return None

#opcional,extra
def dfs(estado:str)->list[str]:
    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = [nodo_inicial]
    explorados = set()

    while fronteira:
        nodo_atual = fronteira.pop()

        if nodo_atual.estado == objetivo:
            return reconstruct_path(nodo_atual)

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados and nodo_sucessor not in fronteira:
                fronteira.append(nodo_sucessor)

    return None

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    def new_heuristic(estado: str) -> int:
        objetivo = "12345678_"
        distancia = 0
        for i, c in enumerate(estado):
            if c != '_' and c != objetivo[i]:
                objetivo_index = objetivo.index(c)
                distancia += abs(i // 3 - objetivo_index // 3) + abs(i % 3 - objetivo_index % 3)
        return distancia

    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = [(new_heuristic(estado), nodo_inicial)]
    explorados = set()

    while fronteira:
        _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == objetivo:
            return reconstruct_path(nodo_atual)

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_estimado = nodo_sucessor.custo + new_heuristic(nodo_sucessor.estado)
                heapq.heappush(fronteira, (custo_estimado, nodo_sucessor))

    return None

'''estado_inicial = "2_3541687"

# A* com distância de Hamming
solucao_hamming, nos_expandidos_hamming, tempo_hamming = astar_hamming(estado_inicial)
custo_hamming = len(solucao_hamming) if solucao_hamming else None

print(f"A* com distância de Hamming:")
print(f"Nós expandidos: {nos_expandidos_hamming}")
print(f"Tempo decorrido: {tempo_hamming:.2f} segundos")
print(f"Custo da solução: {custo_hamming}")

# A* com distância de Manhattan
solucao_manhattan, nos_expandidos_manhattan, tempo_manhattan = astar_manhattan(estado_inicial)
custo_manhattan = len(solucao_manhattan) if solucao_manhattan else None

print(f"A* com distância de Manhattan:")
print(f"Nós expandidos: {nos_expandidos_manhattan}")
print(f"Tempo decorrido: {tempo_manhattan:.2f} segundos")
print(f"Custo da solução: {custo_manhattan}")'''