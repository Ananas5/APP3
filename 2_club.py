import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

file=open("/home/jade/ESME/Advanced Algorithms (python)/APP3/club.txt","r")
lines=file.readlines()
dic={}

#Question 1 

file = open("/Users/Victoria/Desktop/club.txt", "r")
lines = file.readlines()
dic = {}

#create a dict a key and the values to which they are linked
for l in lines[1:]:  
    if "\n" in l:
        l = l[:-1] 
    line = l.split(",")
    if int(line[0]) not in dic:
        dic[int(line[0])] = [int(line[1])]
    else:
        dic[int(line[0])].append(int(line[1]))

#create adjacent matrix
def adjacency(dic):
    adj = np.zeros((34, 34), dtype=int)
    for key, values in dic.items():
        for value in values:
            adj[key-1][value-1] = 1  
            adj[value-1][key-1] = 1  
    return adj

#calculate the adjacent matrix 
adjacency_matrix = adjacency(dic)
print(adjacency_matrix)


#question 2
# Calculate the nodes importancy 
node_importance = in_degrees + out_degrees

#find the leaders
top_two_leaders = np.argsort(node_importance)[-2:][::-1] + 1
print( top_two_leaders)

# Find the top two leaders
top_two_leaders = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:2]
print("Top two leaders:", top_two_leaders)

#question 3
# Identify the best followers
all_nodes = set(dic.keys())
follower_candidates = all_nodes - set(top_two_leaders)
follower_degrees = {node: node_degrees[node - 1] for node in follower_candidates}
best_followers = sorted(follower_degrees, key=follower_degrees.get, reverse=True)
print("Best followers:", best_followers)

#question4
# Best path 
def bfs_shortest_path(adj_matrix, start, goal):
    queue = [(start, [start])]
    visited = set()
    while queue:
        (vertex, path) = queue.pop(0)
        if vertex in visited:
            continue
        for next in range(len(adj_matrix[vertex])):
            if adj_matrix[vertex][next] == 1:
                if next == goal:
                    return path + [next]
                else:
                    queue.append((next, path + [next]))
        visited.add(vertex)
    return None

#in case there is a 0 indexing

leader1, leader2 = top_two_leaders - 1
shortest_path = bfs_shortest_path(adjacency_matrix, leader1, leader2)
print("Shortest path between the two leaders:", [node + 1 for node in shortest_path])




#Question 5

G = nx.Graph()

# Add graph edges using the adjacency dictionary
for node, neighbors in dic.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)


# Degree calculation for each node
degree = nx.degree(G) """we can't use it"""

# Find the maximum degree
max_degree = max(degree, key=lambda x: x[1])[1]

# Identify the leaders 
leaders = [node for node, deg in degree if deg == max_degree]

# graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Positionnement des nœuds
nx.draw(G, pos, with_labels=True, node_color=['blue' if node in leaders else 'red' for node in G.nodes()])
plt.title('Graphe avec les leaders en bleu')
plt.show()
