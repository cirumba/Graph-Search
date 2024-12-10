from typing import Iterable, Set, Tuple
import heapq
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

estado_inicial = "2_3541687"
nodo_raiz = Nodo(estado=estado_inicial, pai=None, acao=None, custo=0)

nodos_sucessores = expande(nodo_raiz)

for nodo in nodos_sucessores:
    print(nodo)


def astar_hamming(estado:str)->list[str]:
    def hamming_distance(estado: str) -> int:
        objetivo = "12345678_"
        return sum(1 for i, c in enumerate(estado) if c != objetivo[i] and c != '_')

    def reconstruct_path(nodo: Nodo) -> list[str]:
        path = []
        while nodo.pai is not None:
            path.append(nodo.acao)
            nodo = nodo.pai
        return path[::-1]

    
    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = [(hamming_distance(estado), nodo_inicial)]
    explorados = set()

    while fronteira:
        _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == objetivo:
            return reconstruct_path(nodo_atual)

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_estimado = nodo_sucessor.custo + hamming_distance(nodo_sucessor.estado)
                heapq.heappush(fronteira, (custo_estimado, nodo_sucessor))

    return None


def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
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

    objetivo = "12345678_"
    nodo_inicial = Nodo(estado=estado, pai=None, acao=None, custo=0)
    fronteira = [(manhattan_distance(estado), nodo_inicial)]
    explorados = set()

    while fronteira:
        _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado == objetivo:
            return reconstruct_path(nodo_atual)

        explorados.add(nodo_atual.estado)

        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_estimado = nodo_sucessor.custo + manhattan_distance(nodo_sucessor.estado)
                heapq.heappush(fronteira, (custo_estimado, nodo_sucessor))

    return None

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    def reconstruct_path(nodo: Nodo) -> list[str]:
        path = []
        while nodo.pai is not None:
            path.append(nodo.acao)
            nodo = nodo.pai
        return path[::-1]

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
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    def reconstruct_path(nodo: Nodo) -> list[str]:
        path = []
        while nodo.pai is not None:
            path.append(nodo.acao)
            nodo = nodo.pai
        return path[::-1]

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
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    def new_heuristic(estado: str) -> int:
        # Implement your new heuristic here
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
