# --- Algoritmo Kruskal para MST ---
def kruskal(grafo):
    aristas = []
    nodos = list(grafo.keys())
    for nodo in nodos:
        for vecino, peso in grafo[nodo].items():
            if (vecino, nodo, peso) not in aristas:
                aristas.append((nodo, vecino, peso))

    aristas.sort(key=lambda x: x[2])

    padre = {}
    rango = {}

    def find(n):
        while padre[n] != n:
            padre[n] = padre[padre[n]]
            n = padre[n]
        return n

    def union(n1, n2):
        r1 = find(n1)
        r2 = find(n2)
        if r1 != r2:
            if rango[r1] < rango[r2]:
                padre[r1] = r2
            elif rango[r1] > rango[r2]:
                padre[r2] = r1
            else:
                padre[r2] = r1
                rango[r1] += 1
            return True
        return False

    for nodo in nodos:
        padre[nodo] = nodo
        rango[nodo] = 0

    mst = {n: {} for n in nodos}

    for n1, n2, peso in aristas:
        if union(n1, n2):
            mst[n1][n2] = peso
            mst[n2][n1] = peso

    return mst