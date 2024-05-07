import numpy as np
file=open("/home/jade/ESME/Advanced Algorithms (python)/APP3/club.txt","r")
lines=file.readlines()
dic={}

#create a dict a key and the values to which they are inked
for l in lines[1:]: # to except the tittles
    if "\n" in l: 
        l=l[:-1] # to except the 'to the line'
    line=l.split(",")
    if int(line[0]) not in dic:
        dic[int(line[0])]=[int(line[1])]
    else:
        dic[int(line[0])].append(int(line[1]))
        
def adjacency(dic): # make the adjacent matrix (undirected)
    adj=np.zeros((34,34),dtype=int)
    for i in lines[1:]:
        for j in range (l):
            if adj[i][j]==1:
                lead[j]+= 1
    
    #for key in dic:
        #for val in dic[key]:
            #adj[key-1][val-1]=1
    return adj

print(adjacency(dic))

'''
def bfs(G, s):
    color = dict()
    for x in G:
        color[x] = 'white'
    path = []
    color[s] = 'grey'
    history = [s]
    while history != []:
        current_vertex = history[0]
        path.append(current_vertex)
        for neighbor in G[current_vertex]:
            if color[neighbor] == 'white':
                color[neighbor] = 'grey'
                history.append(neighbor)
        history.pop(0)
        color[current_vertex] = 'black'
    return path

print(bfs(dic, 'B'))
'''



Question1 et 2 

file = open("/Users/Victoria/Desktop/club.txt", "r")
lines = file.readlines()
dic = {}

#create a dict a key and the values to which they are inked (no changes from jade)
for l in lines[1:]:  
    if "\n" in l:
        l = l[:-1] 
    line = l.split(",")
    if int(line[0]) not in dic:
        dic[int(line[0])] = [int(line[1])]
    else:
        dic[int(line[0])].append(int(line[1]))

#create adjacent matrix => changes a little from jade bc it did not work 
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

# Calculate the nodes importancy 
node_importance = in_degrees + out_degrees

#find the leaders 
top_two_leaders = np.argsort(node_importance)[-2:][::-1] + 1
print( top_two_leaders)

Question 5

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

# Add graph edges using the adjacency dictionary
for node, neighbors in dic.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Degree calculation for each node
degree = nx.degree(G)

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