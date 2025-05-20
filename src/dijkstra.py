# --- Algoritmo Dijkstra ---
def dijkstra(grafo, inicio, fin):
    nodos = list(grafo.keys())
    distancias = {n: float('inf') for n in nodos}
    distancias[inicio] = 0
    padres = {n: None for n in nodos}
    visitados = set()

    while nodos:
        min_nodo = None
        for nodo in nodos:
            if nodo not in visitados:
                if min_nodo is None or distancias[nodo] < distancias[min_nodo]:
                    min_nodo = nodo
        if min_nodo is None:
            break

        if min_nodo == fin:
            break

        visitados.add(min_nodo)
        nodos.remove(min_nodo)

        for vecino, peso in grafo[min_nodo].items():
            if vecino not in visitados:
                nueva_dist = distancias[min_nodo] + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    padres[vecino] = min_nodo

    camino = []
    actual = fin
    while actual:
        camino.insert(0, actual)
        actual = padres[actual]

    if distancias[fin] == float('inf'):
        return None, float('inf')
    return camino, distancias[fin]

# --- Uso de Dijkstra para enviar archivo con ruta óptima ---
def enviar_archivo_con_ruta(origen, destino, filepath):
    ruta, latencia_total = dijkstra(LATENCIAS, origen, destino)
    if not ruta:
        messagebox.showerror("Error", "No existe ruta entre origen y destino.")
        return

    confirmacion = messagebox.askyesno("Confirmar ruta",
                                       f"Ruta óptima encontrada:\n{' -> '.join(ruta)}\nLatencia total: {latencia_total} ms\n\n¿Enviar archivo?")
    if not confirmacion:
        return

    messagebox.showinfo("Envío iniciado", f"Enviando archivo por la ruta:\n{' -> '.join(ruta)}")

    temp_filepath = filepath
    for i in range(len(ruta) - 1):
        nodo_origen = ruta[i]
        nodo_destino = ruta[i+1]

        time.sleep(1)  # Simular retraso

        success = enviar_archivo_salto(nodo_origen, nodo_destino, temp_filepath)
        if not success:
            messagebox.showerror("Error", f"Error enviando de {nodo_origen} a {nodo_destino}. Transferencia abortada.")
            return

    messagebox.showinfo("Éxito", f"Archivo enviado exitosamente de {origen} a {destino} por la ruta óptima.")
