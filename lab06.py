import heapq
import matplotlib.pyplot as plt
import networkx as nx
import math

def a_star_with_visualization(graph, start, goal, heuristic, pos):
   
    plt.figure(figsize=(12, 8))
    G = nx.Graph()
    
   
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    
    open_set_hash = {start}
    
   
    G.add_nodes_from(graph.keys())
    for node, edges in graph.items():
        for neighbor, cost in edges.items():
            G.add_edge(node, neighbor, weight=cost)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Paso 0: Grafo inicial")
    plt.show()
    
    step = 1
    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)
        
       
        plt.figure(figsize=(12, 8))
        node_colors = ['red' if node == current else 'lightblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title(f"Paso {step}: Explorando nodo {current} (f={f_score[current]:.1f}, g={g_score[current]:.1f}, h={heuristic(current, goal):.1f})")
        plt.show()
        step += 1
        
        if current == goal:
            
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            
           
            plt.figure(figsize=(12, 8))
            path_edges = list(zip(path[:-1], path[1:]))
            node_colors = ['green' if node in path else 'lightblue' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=2)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.title(f"Camino encontrado: {' -> '.join(path)} (Costo total: {g_score[goal]:.1f})")
            plt.show()
            
            return path
        
        for neighbor, cost in graph[current].items():
            tentative_g_score = g_score[current] + cost
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                
              
                plt.figure(figsize=(12, 8))
                node_colors = []
                for node in G.nodes():
                    if node == current:
                        node_colors.append('red')
                    elif node == neighbor:
                        node_colors.append('orange')
                    else:
                        node_colors.append('lightblue')
                
                nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
                plt.title(f"Actualizando nodo {neighbor} (g={g_score[neighbor]:.1f}, f={f_score[neighbor]:.1f})")
                plt.show()
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("No se encontró camino al objetivo")
    plt.show()
    return None


graph = {
    'A': {'B': 5, 'C': 10},
    'B': {'A': 5, 'D': 3, 'E': 8},
    'C': {'A': 10, 'F': 2, 'G': 4},
    'D': {'B': 3, 'H': 6},
    'E': {'B': 8, 'H': 1, 'I': 5},
    'F': {'C': 2, 'J': 7},
    'G': {'C': 4, 'J': 3},
    'H': {'D': 6, 'E': 1, 'K': 2},
    'I': {'E': 5, 'K': 4},
    'J': {'F': 7, 'G': 3, 'L': 5},
    'K': {'H': 2, 'I': 4, 'L': 6},
    'L': {'J': 5, 'K': 6}
}


pos = {
    'A': (0, 2), 'B': (2, 3), 'C': (2, 1),
    'D': (4, 4), 'E': (4, 2), 'F': (4, 0),
    'G': (6, 1), 'H': (6, 3), 'I': (6, 1.5),
    'J': (8, 0.5), 'K': (8, 2.5), 'L': (10, 1.5)
}


def heuristic(node, goal):
    x1, y1 = pos[node]
    x2, y2 = pos[goal]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


start = 'A'
goal = 'L'
path = a_star_with_visualization(graph, start, goal, heuristic, pos)
print(f"Camino encontrado de {start} a {goal}: {path}")