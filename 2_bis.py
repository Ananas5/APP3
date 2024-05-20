import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

#question 1 = adjacency matrix non-directed graph

file = open("club.txt", "r")
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


#question 2 = give the 2 best followers

def leaders(adj): 
    """dictionnary of the number of followers of the key node"""
    lead={}
    for i in range (len(adj)):
        lead[i+1]=sum(adj[i])
    return lead

def best_leaders(adj):
    lead=leaders(adj)
    best=[]
    max=0
    for i in lead:
        if max<=lead[i]:
            max=lead[i]
            best.insert(0,i)
        else:
            best.append(i)
    return best[:2]
print("The two best leaders are: ",best_leaders(adjacency_matrix))


#question 3 = identify the best followers
"""not a directed graph so leaders are also followers"""
def best_followers(adj,n=int(input("Number of best followers: "))):
    folo=leaders(adj)
    best=[]
    max=0
    for i in folo:
        if max<=folo[i]:
            max=folo[i]
            best.insert(0,i)
        else:
            best.append(i)
    return best[:n]
print("The n most important followers are: ", best_followers(adjacency_matrix))

#question4 = best path 
def folo (adj,node):
    folo=[]
    adj_folo=adj[node-1] #node-1 to have the index
    for i in range(len(adj_folo)):
        if adj_folo[i]==1:
            folo.append(i+1) #i+1 to have the node
    return folo

def BFS(adj, start, goal):
    to_study=[start]
    visited=[start]
    while to_study!=[]:
        s=to_study.pop(0)
        for v in folo(adj,s):
            if v==goal:
                visited.append(goal)
                return visited
            elif v not in visited: 
                to_study.append(v)
                visited.append(v)
    return None
#in case there is a 0 indexing

leader1, leader2 = best_leaders(adjacency_matrix)[0] , best_leaders(adjacency_matrix)[1]
shortest_path = BFS(adjacency_matrix, leader1, leader2)
print("Shortest path between the two leaders:", shortest_path)




#question 5

G = nx.Graph()

# Add graph edges using the adjacency dictionary
for node, neighbors in dic.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

leaders= best_leaders(adjacency_matrix)
# graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Positionnement des nœuds
nx.draw(G, pos, with_labels=True, node_color=['red' if node in leaders else 'cyan' for node in G.nodes()])
plt.title('Graphe avec les leaders en bleu')
plt.show()
