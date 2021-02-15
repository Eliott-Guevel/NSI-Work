import heapq
import collections

def Dijkstra(graph, sommet_depart):
    """
    Cette fonction renvoie la distance la plus courte d'un sommet de
    départ vers tous les autres sommets d'un graphe pondéré.
    """
    distances = {sommet: float('infinity') for sommet in graph}
    # La distance du sommet de départ à lui-même est évidemment 0
    distances[sommet_depart] = 0

    liste = [(0, sommet_depart)]
    while len(liste) > 0:
        distance_actuelle, sommet_actuel = heapq.heappop(liste)

        # Permet de comparer plusieurs fois des distances pour un même sommet
        if distance_actuelle > distances[sommet_actuel]:
            continue
        # .items renvoie clés et valeurs du dictionnaire graph
        for voisin, poids in graph[sommet_actuel].items():
            plus_courte_distance = distance_actuelle + poids

            # Nouveau chemin uniquement pris s'il est meilleur que les précédents
            if plus_courte_distance < distances[voisin]:
                distances[voisin] = plus_courte_distance
                heapq.heappush(liste, (plus_courte_distance, voisin))

    # Permet d'obtenir un dictionnaire ordonné selon les clés
    # Tri obtenu avec lambda, où la valeur 0 indique les clés
    distances = collections.OrderedDict(sorted(distances.items(), key=lambda t: t[0]))
    return distances

Graph = {'A':{'B':1, 'C':2},
        'B':{'A':1, 'D':2, 'F':3},
        'C':{'A':2, 'D':3, 'E':4},
        'D':{'B':2, 'C':3, 'E':2, 'F':3, 'G':3},
        'E':{'C':4, 'D':2, 'G':5},
        'F':{'B':3, 'D':3, 'G':4},
        'G':{'D':3, 'E':5, 'F':4}}

print(Dijkstra(Graph, 'G'))